import os
import warnings
from operator import itemgetter

import bs4
import streamlit as st
from langchain import hub
from langchain.docstore.document import Document
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.llms import Together
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_together import TogetherEmbeddings

from load import load_and_clean_html_texts
from store import download_10k

company_ticker = st.sidebar.text_area("Company Ticker")
download_10k(company_ticker)

docs = load_and_clean_html_texts(company_ticker)
final_docs = []

for doc in docs:
    f = Document(page_content=doc, metadata={"source": "local"})
    final_docs.append(f)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(final_docs)
warnings.filterwarnings("ignore")

vectorstore = FAISS.from_texts(
    [x.page_content for x in splits],
    TogetherEmbeddings(model="togethercomputer/m2-bert-80M-8k-retrieval"),
)

print("Indexing Done")

retriever = vectorstore.as_retriever()

model = Together(model="mistralai/Mixtral-8x7B-Instruct-v0.1")

# Provide a template following the LLM's original chat template.
template = """<s>[INST] Answer the question in a simple sentence based only on the following context:
{context}

Question: {question} [/INST] 
"""
prompt = ChatPromptTemplate.from_template(template)

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

input_query = "What are some insights that you can draw from the 10-K filings? What do the products, financial situation, future outlook of the company look like?"
output = chain.invoke(input_query)

st.write(output)
