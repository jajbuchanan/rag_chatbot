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
