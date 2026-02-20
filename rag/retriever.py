from langchain_chroma import Chroma
from rag.embeddings import get_embeddings


CHROMA_PATH = "rag/chroma_store"


def get_retriever():
    vectorstore = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=get_embeddings()
    )

    return vectorstore.as_retriever(search_kwargs={"k": 3})


def retrieve_examples(question):
    retriever = get_retriever()

    vectorstore = retriever.vectorstore
    print("Collection count:", vectorstore._collection.count())
    docs = retriever.invoke(question)
    

    return "\n\n".join([doc.page_content for doc in docs])
