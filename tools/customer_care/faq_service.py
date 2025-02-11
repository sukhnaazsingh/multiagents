from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()

# Load FAQ Data
faq_loader = TextLoader("tools/customer_care/FAQ_Paketverlust.txt")
faq_documents = faq_loader.load()

# Split Text into Chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
faq_texts = text_splitter.split_documents(faq_documents)

# Create Embeddings & Vector Store
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(faq_texts, embeddings)
vectorstore.persist()

# Create Retriever
retriever = vectorstore.as_retriever()

# Create RAG Pipeline
qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(), retriever=retriever, return_source_documents=True)

@tool
def answer_faq(question: str) -> str:
    """Answers customer questions based on the FAQ document."""
    result = qa_chain.invoke({"query": question})
    print("RAG RESULT: ", result)
    return result
