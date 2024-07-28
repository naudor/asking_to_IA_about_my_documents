

get_ipython().system('pip install PyPDF2')
get_ipython().system('pip install openai')
get_ipython().system('pip install langchain')
get_ipython().system('pip install llama-index')



import os
import openai
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.core.llms import LLM
from llama_index.llms.openai import OpenAI

import textwrap
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader


os.environ["OPENAI_API_KEY"] = "escriu aqui el teu token API chatGPT"

# Defineix el camí de la carpeta que vols verificar
directory_path = "./storage"

# Utilitza os.path.exists() per comprovar si el camí existeix
if os.path.exists(directory_path):
    # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir=directory_path)
    # load index
    index = load_index_from_storage(storage_context)
else:
    documents = SimpleDirectoryReader("documents").load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist()



# In[5]:


# Defineix el motor de consultes amb el model escollit
llm = OpenAI(model="gpt-4o-mini") 
query_engine = index.as_query_engine(llm=llm)
#query_engine = index.as_query_engine()

context = "Respon sempre en català."
pregunta = "Quina eficiencia global tenia l'algoritme de Machine Learning que vaig desenvolupar?"
prompt = context + pregunta
resposta = query_engine.query(prompt)
print (resposta)


# In[ ]:




