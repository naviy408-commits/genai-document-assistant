import requests
import json


OLLAMA_MODEL = "tinyllama"
OLLAMA_URL = "http://localhost:11434/api/generate"


def build_rag_chain(vector_store):
    print("RAG chain ready!")
    return {"vector_store": vector_store}


def ask_question(chain_dict, question):
    print(f"\n--- Question: {question} ---")
    
    vector_store = chain_dict["vector_store"]
    
    # Step 1: Get relevant chunks from FAISS
    print("Searching FAISS...")
    docs = vector_store.similarity_search(question, k=3)
    print(f"Found {len(docs)} chunks")
    
    # Step 2: Build context from chunks
    context = ""
    for doc in docs:
        page = doc.metadata.get("page", "?")
        context += f"[Page {page}]\n{doc.page_content}\n\n"
    
    print(f"Context length: {len(context)} chars")
    
    # Step 3: Build prompt
    prompt = f"""Answer the question using only the context below.
Be brief and direct. Include page numbers.

Context:
{context}

Question: {question}

Answer:"""

    # Step 4: Call Ollama directly via HTTP
    print("Calling Ollama...")
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )
        
        print(f"Ollama status: {response.status_code}")
        
        if response.status_code == 200:
            answer = response.json().get("response", "No response from model")
            print(f"Answer: {answer[:100]}...")
        else:
            answer = f"Error from Ollama: {response.status_code}"
            print(answer)
            
    except requests.exceptions.Timeout:
        answer = "Request timed out. Ollama is taking too long. Try a shorter question."
        print("TIMEOUT!")
    except requests.exceptions.ConnectionError:
        answer = "Cannot connect to Ollama. Make sure 'ollama serve' is running."
        print("CONNECTION ERROR!")
    except Exception as e:
        answer = f"Error: {str(e)}"
        print(f"ERROR: {e}")

    # Step 5: Build sources
    sources = []
    seen_pages = set()
    for doc in docs:
        page = doc.metadata.get("page", "?")
        if page not in seen_pages:
            seen_pages.add(page)
            sources.append({
                "page": page,
                "content": doc.page_content[:300] + "..."
                           if len(doc.page_content) > 300
                           else doc.page_content,
            })

    return {"answer": answer, "sources": sources}