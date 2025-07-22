# analysis.py
import time
from transformers import pipeline
from langchain import LLMChain, PromptTemplate
from langchain.llms import HuggingFacePipeline
from langchain_community.llms import Ollama

PROMPT = "Explain how plants respond to disease."

# 1) Hugging Face pipeline (e.g. GPT2)
hf_pipe = pipeline('text-generation', model='gpt2')
start = time.time()
hf_out = hf_pipe(PROMPT, max_length=50)
hf_time = time.time() - start

# 2) LangChain + Hugging Face Pipeline
template = PromptTemplate.from_template("Question: {question}\nAnswer:")
llm_hf = HuggingFacePipeline(pipeline=hf_pipe)
chain = LLMChain(llm=llm_hf, prompt=template)
start = time.time()
lc_out = chain.run(question=PROMPT)
lc_time = time.time() - start

# 3) Ollama Mistral
ol = Ollama(model='mistral', temperature=0.7)
start = time.time()
ol_out = ol.chat(PROMPT)
ol_time = time.time() - start

# Display
print("=== Benchmark Results ===")
print(f"HF pipeline:   {hf_time:.2f}s | {hf_out[0]['generated_text']}\n")
print(f"LangChain-HF: {lc_time:.2f}s | {lc_out}\n")
print(f"Ollama Mistral:{ol_time:.2f}s | {ol_out}\n")