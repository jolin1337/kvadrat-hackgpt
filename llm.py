from langchain.llms import GPT4All
from vectorstore import get_retriever

def get_llm(name='ggml-gpt4all-j-v1.3-groovy'):
    llm = GPT4All(model="ggml-gpt4all-j-v1.3-groovy")
    return llm

if __name__ == '__main__':
    llm = get_llm()
    retrieval = get_retriever()
    query = 'Vem har kompetens inom utveckling och programmering inom programmeringsspråket Python på kvadrat?'
    docs = ' '.join(retrieval.get_relevant_documents(query))
    print(docs)
    #llm.

