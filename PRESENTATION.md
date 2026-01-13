# Ayodeji: The Multimodal AI Course Rep

## Project Overview
**Ayodeji** is an intelligent, multimodal Telegram bot designed to serve as a "Course Representative" for Nigerian university students. Unlike standard chatbots, Ayodeji embodies a witty, relatable persona that mimics a helpful student leader. He bridges the gap between students and academic resources by offering:

1.  **Multilingual Support**: Fluently speaks English, Nigerian Pidgin, Yoruba, Igbo, and Hausa.
2.  **RAG (Retrieval-Augmented Generation)**: "Digests" PDF handouts and answers questions based *only* on the provided material.
3.  **Voice Interaction**: Transcribes voice notes (using Groq/Whisper) and replies with text.
4.  **Privacy**: Adheres to strict data handling policies (NDPR compliant principles).

---

## Technical Architecture

### Tech Stack
*   **Backend**: Python, FastAPI (for Webhooks)
*   **AI/LLM**: Google Gemini 1.5 Flash (Generation & Embeddings), Groq (Audio Transcription)
*   **Database**: ChromaDB (Vector Store for PDFs)
*   **Messaging**: Python-Telegram-Bot (Frontend interface)
*   **Deployment**: Docker on Render.com

### Workflow
1.  **Input**: User sends Text, Voice, or PDF via Telegram.
2.  **Processing**:
    *   *Text* -> Direct LLM query or RAG retrieval.
    *   *Voice* -> Transcribed to text -> Processed as text.
    *   *PDF* -> Chunked -> Embedded -> Stored in ChromaDB.
3.  **Response**: Ayodeji generates a response in the user's language and style.

---

## Key Features & Code Highlights

### 1. The "Witty" Persona & Multilingual Brain
Ayodeji doesn't just answer; he *relates*. The system prompt enforces a specific character.

**File:** `brain.py`
```python
template = """
You are Ayodeji, a witty and efficient Nigerian University Course Rep.
You act like a fellow student but very responsible.
You are Multilingual. You speak "Clean English", "Nigerian Pidgin", "Yoruba", "Igbo", and "Hausa".
ALWAYS reply in the same language the user speaks to you.

If the user speaks Pidgin, reply in Pidgin (e.g., "I don run am", "No wahala").
If the user speaks Yoruba, reply in Yoruba (e.g., "Bawo ni", "Mo ti gbo").

Context: {context}
Question: {question}
"""
```

### 2. The "Brain" (RAG Implementation)
How Ayodeji reads PDFs and remembers them. We use ChromaDB to store vector embeddings of documents.

**File:** `brain.py`
```python
def digest_pdf(file_path: str):
    # Load PDF
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    
    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = text_splitter.split_documents(docs)
    
    # Store in Vector DB
    vector_store.add_documents(documents=splits)
    return "I don digest that PDF directly into my brain. Ask me anything about am!"
```

### 3. The "Ears" (Voice Processing)
Using Groq's fast inference for Whisper-large to transcribe audio instantly.

**File:** `ears.py`
```python
def process_audio(file_path: str):
    with open(file_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(file_path, file.read()),
            model="whisper-large-v3",
            response_format="json",
            language="en", 
            temperature=0.0
        )
    return transcription.text
```

### 4. Robust Deployment (FastAPI Webhook)
Instead of polling, we use a Webhook to receive updates from Telegram, making it scalable on serverless platforms like Render.

**File:** `main.py`
```python
@app.post("/webhook")
async def telegram_webhook(request: Request):
    """
    Handle incoming Telegram updates
    """
    data = await request.json()
    update = Update.de_json(data, ptb_app.bot)
    await ptb_app.process_update(update)
    return {"status": "ok"}
```

---

## Why This Matters
*   **Accessibility**: Voice notes help students who prefer speaking over typing.
*   **Inclusivity**: Local language support breaks down language barriers in education.
*   **Efficiency**: Instant answers from 100+ page handouts save hours of reading time.
