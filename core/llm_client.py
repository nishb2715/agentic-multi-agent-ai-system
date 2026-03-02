from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME, MAX_TOKENS, TEMPERATURE

client = Groq(api_key=GROQ_API_KEY)


def call_llm(prompt, model=MODEL_NAME):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS
    )

    return response.choices[0].message.content