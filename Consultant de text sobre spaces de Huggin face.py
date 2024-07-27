#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install gradio_client')


# In[1]:


import os
import json
import requests
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from gradio_client import Client

# Defineix la teva clau d'API de Hugging Face
api_key = "escriu_aqui_el_token_de_huggin_Face"


# In[2]:


# Carrega els documents des d'un directori de fitxers JSON
def load_json_documents(directory_path):
    documents = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            with open(os.path.join(directory_path, filename), 'r', encoding='utf-8') as file:
                content = json.load(file)
                text = ""
                for section in content.get('content', {}).values():
                    if isinstance(section, list):
                        text += "\n".join(section)
                    else:
                        text += section
                documents.append(Document(page_content=text, metadata={"title": content.get("title"), "url": content.get("url")}))
    return documents

# Vectoritza els documents
def vectorize_documents(documents):
    embeddings = HuggingFaceEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore

# Crea un prompt basat en els vectors i la pregunta
def create_prompt_from_vectors(vectorstore, question):
    docs = vectorstore.similarity_search(question, k=5)
    combined_docs = "\n".join([doc.page_content for doc in docs])
    prompt = f"{combined_docs}\n\nPregunta: {question}\nResposta:"
    return prompt


# In[5]:


# Ruta al directori dels teus documents JSON
document_directory = "C:\\Users\\Naudor\\prova_chatgpt\\documents\\Telefonica"

# Carrega i vectoritza els documents
documents = load_json_documents(document_directory)
vectorstore = vectorize_documents(documents)


# In[6]:


# Pregunta que vols fer
question = "Quina opinió tinc de Moonlander MK1?"

# Genera el prompt a partir dels vectors i envia la sol·licitud a l'API
prompt = create_prompt_from_vectors(vectorstore, question)

client = Client("vilarin/Llama-3.1-8B-Instruct")
result = client.predict(
		message=prompt,
		system_prompt="Constesta sempre en català. Estas contestant en base a articles que he escrit jo",
		temperature=0.8,
		max_new_tokens=4096,
		top_p=1,
		top_k=20,
	penalty=1.2,
	api_name="/chat"
)

print(result)




# In[ ]:




