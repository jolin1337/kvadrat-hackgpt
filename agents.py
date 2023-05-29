from langchain.agents import initialize_agent, Tool, AgentType
from langchain.chains import RetrievalQA
from langchain.agents.agent_toolkits import (
    create_vectorstore_agent,
    VectorStoreToolkit,
    VectorStoreInfo,
)
from langchain.agents.react.base import DocstoreExplorer
from vectorstore import get_vectorstore, get_documents, get_retriever
from llm import get_llm


def get_tools():
    vs = get_vectorstore(doc_limit=100)
    docstore=DocstoreExplorer(vs)
    #retriever = get_retriever(doc_limit=100)
    #llm = get_llm()
    #tool = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    tools = [
        #Tool(
        #    name="Kvadrat konsult firmas QA system",
        #    description="användbar när du behöver svara på frågor gällande vem som har vilken kompetens på kvadrat samt andra saker om kvadrat. ",
        #    func=tool.run,
        #),

        Tool(
            name="Search",
            func=docstore.search,
            description="useful for when you need to ask with search"
        ),
        Tool(
            name="Lookup",
            func=docstore.lookup,
            description="useful for when you need to ask with lookup"
        )
    ]
    return tools

def get_agent():
    tools = get_tools()
    llm = get_llm()
    agent = initialize_agent(tools, llm, agent=AgentType.REACT_DOCSTORE, verbose=True)
    return agent

if __name__ == '__main__':
    agent = get_agent()
    print(agent.run('What is happiness?'))
    print(agent.run('Vem har kompetens inom utveckling och programmering inom programmeringsspråket Python på kvadrat?'))
