import os
import asyncio
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from orchestrator import Orchestrator

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

orchestrator = Orchestrator()


#text splitting for longer msg
def split_text(text, max_length=3900):
    parts = []
    while len(text) > max_length:
        split_at = text.rfind("\n", 0, max_length)
        if split_at == -1:
            split_at = max_length
        parts.append(text[:split_at])
        text = text[split_at:]
    parts.append(text)
    return parts


#starting 
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Agentic Research System.\n\n"
        "Send me a research topic and I will:\n"
        "• Draft a paper\n"
        "• Send it to Professor Agent\n"
        "• Revise if needed\n"
        "• Return final approved version\n"
    )


#to handle topic , run orchestrator 
async def handle_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):

    topic = update.message.text.strip()

    
    await update.message.reply_text("🧠 Researching topic...")
    await asyncio.sleep(4)

    
    trace = orchestrator.run(topic)

    await asyncio.sleep(1)

    #draft 1 , review 1
    await update.message.reply_text("✍️ Draft prepared. Sending to Professor...")
    await asyncio.sleep(2)

    if trace["feedback_round_1"]:
        parts = split_text(trace["feedback_round_1"])
        for part in parts:
            await update.message.reply_text(
                "👨‍🏫 Professor Review (Round 1):\n\n" + part,
                parse_mode=None
            )
            await asyncio.sleep(0.5)

    
    if trace["feedback_round_2"]:
        await asyncio.sleep(2)
        await update.message.reply_text("🔁 Student revising draft...")
        await asyncio.sleep(2)

        parts = split_text(trace["feedback_round_2"])
        for part in parts:
            await update.message.reply_text(
                "👨‍🏫 Professor Review (Round 2):\n\n" + part,
                parse_mode=None
            )
            await asyncio.sleep(0.5)

    #summary of execution
    await asyncio.sleep(1)

    summary_text = (
        "📊 Execution Summary\n\n"
        f"Rounds Used: {trace['execution_metadata']['rounds_used']}\n"
        f"Quality Score: {trace['execution_metadata']['quality_score']}\n"
        f"Execution Time: {trace['execution_metadata']['execution_time_seconds']} seconds\n"
        f"Model Used: {trace['execution_metadata']['model']}"
    )

    await update.message.reply_text(summary_text, parse_mode=None)

    #final paper
    await asyncio.sleep(1)
    status = trace["execution_metadata"].get("approval_status")

    if status == "APPROVED":
        await update.message.reply_text("✅ Final Approved Paper:\n")
    else:
        await update.message.reply_text(
            "⚠️ Max revisions reached — delivering best available draft:\n"
        )

    final_parts = split_text(trace["final_paper"])

    for i, part in enumerate(final_parts):
        await update.message.reply_text(
            f"Part {i+1}/{len(final_parts)}\n\n{part}",
            parse_mode=None
        )
        await asyncio.sleep(0.5)


#to run bot
def run_bot():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_topic))

    print("🚀 Telegram Bot Running...")
    app.run_polling()


if __name__ == "__main__":
    run_bot()