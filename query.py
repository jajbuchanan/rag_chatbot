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
