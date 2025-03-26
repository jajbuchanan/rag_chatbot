## 📁 Project: RAG Chatbot for Army Doctrine

# This starter template includes:
# - Text extraction from cleaned .txt files
# - Chunking and embedding
# - Vector store with FAISS
# - Query function using OpenAI API (GPT-4 Turbo)
# - Streamlit chatbot UI

## Folder Structure (suggested)
# rag_chatbot_doctrine/
# ├── extracted/             # Cleaned text files
# ├── vectorstore/           # FAISS index files
# ├── app.py                 # Streamlit UI
# ├── embed.py               # Chunk + embed text
# ├── query.py               # Retrieve + generate answer
# ├── utils.py               # Helper functions
# ├── requirements.txt       # Python dependencies

# ✅ Step 1: Chunking & Embedding from Text Files (embed.py)

import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

TXT_DIR = "./extracted"
VECTOR_DIR = "./vectorstore"
MODEL = "text-embedding-3-small"


def load_txt_files(txt_dir):
    documents = []
    for filename in os.listdir(txt_dir):
        if filename.endswith(".txt"):
            path = os.path.join(txt_dir, filename)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
                documents.append(
                    Document(page_content=text, metadata={"source": filename})
                )
    return documents


def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)
    return chunks


def embed_chunks(chunks):
    embeddings = OpenAIEmbeddings(model=MODEL)
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(VECTOR_DIR)
    print(f"✅ Saved vectorstore to {VECTOR_DIR}")


if __name__ == "__main__":
    docs = load_txt_files(TXT_DIR)
    chunks = chunk_documents(docs)
    embed_chunks(chunks)

# ✅ Step 2: Querying (query.py)

from langchain.vectorstores import FAISS
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings

MODEL = "text-embedding-3-small"
VECTOR_DIR = "./vectorstore"


def run_query(question):
    embeddings = OpenAIEmbeddings(model=MODEL)
    db = FAISS.load_local(VECTOR_DIR, embeddings)
    retriever = db.as_retriever()
    docs = retriever.get_relevant_documents(question)

    llm = ChatOpenAI(model_name="gpt-4-turbo")
    chain = load_qa_with_sources_chain(llm, chain_type="stuff")
    result = chain(
        {"input_documents": docs, "question": question}, return_only_outputs=True
    )
    return result["output_text"]


# ✅ Step 3: Streamlit App (app.py)

import streamlit as st
from query import run_query

st.title("DoctrineBot: Ask UK/NATO Military Doctrine")
query = st.text_input(
    "Enter your question:", "What is UK doctrine on counterinsurgency?"
)

if st.button("Ask"):
    with st.spinner("Thinking..."):
        answer = run_query(query)
        st.markdown(answer)

# ✅ requirements.txt
# streamlit
# openai
# langchain
# faiss-cpu

# 📌 To run:
# 1. Put cleaned .txt files in /extracted
# 2. Run embed.py once to build vector DB
# 3. Launch: `streamlit run app.py`
# 4. Ask questions!

# ✅ Next Steps:
# - Improve citation formatting
# - Add PDF viewer for source
# - Add multilingual doc support
# - Log queries for insight
