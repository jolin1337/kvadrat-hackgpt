from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain, LLMChain

from vectorstore import get_retriever
from llm import get_llm
from time import time

qa_prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {english_translation}
Answer:"""
_qa_prompt_template = """Använd följande delar av ett kontext för att svara på frågan i slutet. Om du inte vet svaret, svara bara att du inte vet, försök inte att komma på ett eget svar.

{context}

Fråga: {english_translation}
Svar:"""
PROMPT = PromptTemplate(
    template=qa_prompt_template, input_variables=["context", "english_translation"]
)
times ={}
print(str(SequentialChain))
def time_it(method, *vargs, **kargs):
    global times
    times[str(method)] = time()
    ret = method(*vargs, **kargs)
    times[str(method)] = time() - times[str(method)]
    print(f"Time for {str(method)}(*{vargs}, **{kargs}): {times[str(method)]}")
    return ret

def translate_chain(llm, language, input_variable='input'):
    answer = '{' + input_variable + '}'
    translate_template = f"""You are a translator and should translate this document as accurate as possible to {language}.

    Document:
    {answer}
    Translation in {language}:"""
    prompt_template = PromptTemplate(input_variables=[input_variable], template=translate_template)
    translate_chain = LLMChain(llm=llm, prompt=prompt_template, output_key=f'{language.lower()}_translation')
    return translate_chain
if __name__ == '__main__':
    llm = time_it(get_llm)
    qa_chain = load_qa_chain(llm, chain_type="stuff", prompt=PROMPT, output_key='answer')
    chain = SequentialChain(
        chains=[
            #translate_chain(llm, 'English', input_variable='question'), 
            qa_chain, 
            #translate_chain(llm, 'Swedish', input_variable='answer'),
        ],
        input_variables=["english_translation", "input_documents"],
        #output_variables=["answer", "swedish_translation"],
        verbose=False)
    retriever = time_it(get_retriever, doc_limit=500)
    print("Starting...")
    
    questions = [
        {'swe': 'Vad är lycka?', 'eng': 'Who knows Java programming?'},
        {'swe': 'Vem kan programmera Java?', 'eng': 'Who knows Java programming?'},
        {'swe': 'Vilka rapporter och undersökningar har genomförts?', 'eng': 'What surveys and investigations has been conducted?' },
        {'swe': 'Vilka utbildningar finns det?', 'eng': 'What education courses can I take?'},
    ]
    for query in questions:
        print("Question:", query['swe'])
        docs = time_it(retriever.get_relevant_documents, query['swe']) 
        #print("Sources:", docs)
        #print("len docs", len(docs), "len words", ' '.join([d.page_content for d in docs]).count(' ') + 1)
        print("Answer:")
        answer = time_it(chain, {"input_documents": docs, "english_translation": query['eng']})
        print(answer['answer'])
        print("Sources:", '- ' + ' - '.join([d.page_content for d in docs]))
        print()
        print()
