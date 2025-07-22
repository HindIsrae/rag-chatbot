# rag_chain.py
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# 1. Load index and create retriever
vector_store = FAISS.load_local(
    "faiss_index.pkl",                # index path
    HuggingFaceEmbeddings(),          # embeddings instance
    allow_dangerous_deserialization=True
)

retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# 2. Configure Ollama LLM with sampling
llm = Ollama(
    model="mistral",
    temperature=0.7,
    top_k=50,
    top_p=0.9,
)

# 3. Prompt template
prompt = """
1. Use the following context to answer the question.
2. If you don't know, say \"I don't know\"—do not hallucinate.
3. Keep it crisp (3–4 sentences).

Context:
{context}

Question:
{question}

Answer:
"""
template = PromptTemplate.from_template(prompt)

# 4. Build RetrievalQA chain
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=False,
    chain_type_kwargs={"prompt": template}
)

def answer(question: str) -> str:
    return qa.run(question)