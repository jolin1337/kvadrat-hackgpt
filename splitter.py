import glob
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredFileLoader

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 400,
    chunk_overlap  = 50,
)
def get_documents(path='./contents/*', limit=-1):
    for i, fname in enumerate(glob.glob(path)):
        if limit >= 0 and limit <= i:
            break
        if fname.strip('.').count('.') <= 1:
            yield open(fname, mode='r').read()
        #yield UnstructuredFileLoader(fname).load()

def split_documents(docs):
    return text_splitter.create_documents(docs)

if __name__ == '__main__':
    docs = list(get_documents(limit=10))
    texts = split_documents(docs)
    print(texts[:4], len(texts), len(docs))
