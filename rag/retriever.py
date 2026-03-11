import arxiv
import chromadb
from sentence_transformers import SentenceTransformer
import hashlib

# Free local embedding model
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Local ChromaDB instance
client = chromadb.PersistentClient(path="./rag/chroma_db")
collection = client.get_or_create_collection("research_papers")

def fetch_and_store_papers(topic: str, max_results: int = 5):
    """Fetch real papers from ArXiv and store in vector DB"""
    
    search = arxiv.Search(
        query=topic,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )
    
    papers = []
    for result in search.results():
        paper = {
            "title": result.title,
            "abstract": result.summary,
            "authors": ", ".join(str(a) for a in result.authors[:3]),
            "year": str(result.published.year),
            "url": result.entry_id
        }
        papers.append(paper)
        
        # Store in ChromaDB
        doc_id = hashlib.md5(result.entry_id.encode()).hexdigest()
        embedding = embedder.encode(result.summary).tolist()
        
        collection.upsert(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[result.summary],
            metadatas=[{
                "title": paper["title"],
                "authors": paper["authors"],
                "year": paper["year"],
                "url": paper["url"]
            }]
        )
    
    return papers

def retrieve_relevant_context(topic: str, n_results: int = 3) -> str:
    """Retrieve most relevant papers for a topic"""
    
    query_embedding = embedder.encode(topic).tolist()
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    context = ""
    citations = []
    
    for i, (doc, meta) in enumerate(zip(
        results['documents'][0], 
        results['metadatas'][0]
    )):
        context += f"\n[{i+1}] {meta['title']} ({meta['year']})\n"
        context += f"Authors: {meta['authors']}\n"
        context += f"Abstract: {doc[:500]}\n"
        context += f"Source: {meta['url']}\n\n"
        
        citations.append(
            f"[{i+1}] {meta['authors']} ({meta['year']}). "
            f"{meta['title']}. ArXiv: {meta['url']}"
        )
    
    return context, citations

def fetch_and_store_papers(topic: str, max_results: int = 5):
    # Check if we already have papers for this topic
    query_embedding = embedder.encode(topic).tolist()
    existing = collection.query(
        query_embeddings=[query_embedding],
        n_results=1
    )
    
    # If we already have relevant papers, skip fetching
    if existing['documents'][0]:
        print("📚 Using cached papers from vector DB")
        return
    
    # Otherwise fetch fresh from ArXiv
    ...