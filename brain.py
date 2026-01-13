import os
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA

# Configuration
PERSIST_DIRECTORY = os.getenv("CHROMA_DB_PATH", "chroma_db")
# Ensure the directory exists
os.makedirs(PERSIST_DIRECTORY, exist_ok=True)

# Initialize Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=GEMINI_API_KEY)
llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", google_api_key=GEMINI_API_KEY, temperature=0.7)

# Initialize Chroma Vector Store
vector_store = Chroma(
    persist_directory=PERSIST_DIRECTORY,
    embedding_function=embeddings
)

def digest_pdf(file_path: str):
    """
    Chunks and embeds a local PDF file into ChromaDB.
    """
    try:
        # Load and Split
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        splits = text_splitter.split_documents(docs)
        
        # Add to Vector Store
        vector_store.add_documents(documents=splits)
        # Chroma automatically persists in newer versions, but explicit if needed
        
        return "I don digest that PDF directly into my brain. Ask me anything about am!"
        
    except Exception as e:
        print(f"Error digesting PDF: {e}")
        return "Omo, I struggle to read that file. Send am again properly."

def ask_ayodeji(query: str) -> str:
    """
    RAG retrieval + Generation with Persona.
    """
    try:
        # System Prompt
        template = """
        You are Ayodeji, a witty and efficient Nigerian University Course Rep. 
        You act like a fellow student but very responsible.
        You are Multilingual. You speak "Clean English", "Nigerian Pidgin", "Yoruba", "Igbo", and "Hausa".
        ALWAYS reply in the same language the user speaks to you. 
        If the user speaks Pidgin, reply in Pidgin (e.g., "I don run am", "No wahala").
        If the user speaks Yoruba, reply in Yoruba (e.g., "Bawo ni", "Mo ti gbo").
        If the user speaks Igbo, reply in Igbo (e.g., "Kedu", "O di mma").
        If the user speaks Hausa, reply in Hausa (e.g., "Sannu", "Nagode").
        
        Use the following pieces of context to answer the question at the end.
        If you don't know the answer, say "Oga, that one no dey inside handout" or "I never update my brain for that one". 
        Don't try to make up an answer.
        
        Context: {context}
        
        Question: {question}
        
        Ayodeji's Answer:
        """
        
        QA_CHAIN_PROMPT = PromptTemplate.from_template(template)
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=False,
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
        )
        
        try:
            result = qa_chain.invoke({"query": query})
            return result["result"]
        except Exception as e:
            print(f"RAG failed (likely embedding quota): {e}. Falling back to pure LLM.")
            # Fallback: Just ask the LLM without context
            fallback_prompt = template.replace("{context}", "No external context available (Quota exhausted).").replace("{question}", query)
            response = llm.invoke(fallback_prompt)
            return response.content
        
    except Exception as e:
        print(f"Error in ask_ayodeji: {e}")
        import traceback
        traceback.print_exc()
        return "My brain dey network failure small. Ask me again."

