from langchain.llms import GPT4All
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from splitter import get_documents, split_documents

llm = GPT4All(model="ggml-gpt4all-j-v1.3-groovy")
documents = get_documents(limit=100)

# Split your docs into texts
texts = split_documents(list(documents))

# There is a lot of complexity hidden in this one line. I encourage you to check out the video above for more detail
chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=True)
chain.run(texts)
