#from qdrant_client import QdrantClient
#qdrant = QdrantClient(":memory:") # Create in-memory Qdrant instance, for testing, CI/CD
#client = QdrantClient(path="vs_db.bin")  # Persists changes to disk, fast prototyping

import shutil
from langchain.vectorstores import Qdrant
from langchain.embeddings import HuggingFaceEmbeddings, SentenceTransformerEmbeddings
import qdrant_client

from splitter import get_documents, split_documents

def get_embeddings(name='all-MiniLM-L6-v2'):
    embeddings = HuggingFaceEmbeddings(model_name=name)
    return embeddings

def get_vectorstore(path="vs_db.bin/kvadrat", recreate=True, doc_limit=-1):
    embeddings = get_embeddings()
    if recreate:
        shutil.rmtree(path, ignore_errors=True)
        documents = list(get_documents(limit=doc_limit))
        docs = split_documents(documents)
        qdrant = Qdrant.from_documents(
            docs, embeddings,
            path=path,
            collection_name=path.split('/')[-1],
        )
    else:
        client = qdrant_client.QdrantClient(
            path=path, prefer_grpc=True
        )
        qdrant = Qdrant(
            client=client, collection_name=path.split('/')[-1],
            embeddings=embeddings
        )
    return qdrant

def get_retriever(**args):
    vs = get_vectorstore(**args)
    return vs.as_retriever()


if __name__ == '__main__':
    embeddings = get_embeddings()
    #print(embeddings.embed_documents([d for d in get_documents(limit=10)]).shape)
    retriever = get_retriever(doc_limit=10)
    print(retriever.get_relevant_documents('Vilka undersökningar har kvadrat genomfört?'))
