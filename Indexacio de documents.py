#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install numpy pandas scikit-learn tensorflow torch whoosh openai')


# In[104]:


from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT
from whoosh.writing import AsyncWriter
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh.query import Or
import os


# In[106]:


# Esquema per indexar els documents. Els documents a indexar nomes tenen dos camps a indexar el titol i el text
schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True))


# In[108]:


# Crear directori per emmagatzemar l'índex si no existeix
index_dir = "indexdir"
if not os.path.exists(index_dir):
    os.mkdir(index_dir)


# In[110]:


# Crear l'índex
ix = create_in("indexdir", schema)


# In[112]:


# Indexar tots els documents de la carpeta
def index_documents(documents_folder):
    writer = AsyncWriter(ix)
    for filename in os.listdir(documents_folder):
        if filename.endswith(".json"):  # Considerar només els fitxers .txt
            path = os.path.join(documents_folder, filename)
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
                title = str(data.get("title", "Unknown Title"))  # Obtenir el títol del JSON, amb un valor per defecte
                content = str(data.get("content", ""))  # Obtenir el contingut del JSON, amb un valor per defecte
                content = content + ". Font: " + str(data.get("url", ""))
                writer.add_document(title=title, content=content)
    writer.commit()

# Funció per buscar documents rellevants
def search_documents(query_terms):
    ix = open_dir("indexdir")
    with ix.searcher() as s:
        # Crea una consulta combinant termes amb OR
        qp = QueryParser("content", schema=ix.schema)
        queries = [qp.parse(term) for term in query_terms]
        combined_query = Or(queries)
        results = s.search(combined_query, limit=1)
        return [result['content'] for result in results]


def inspect_index(index_dir):
    ix = open_dir(index_dir)
    with ix.searcher() as searcher:
        # Imprimeix els documents a l'índex
        for hit in searcher.all_stored_fields():
            print(f"Document: {hit}")


# In[114]:


# Camí de la carpeta amb els documents
documents_folder = "C:/Users/Naudor/prova_chatgpt"

try:
    index_documents(documents_folder)
except Exception as e:
    print(f"Error indexant documents: {e}")


# In[116]:


#pregunta = "Quina opinió tinc del teclat Moonlander MK1?"
pregunta = "Quina es eficàcia general que vaig obtenir del model de classificació de textos?"
words = pregunta.split()


# In[118]:


# Cercar documents rellevants
documents_rellevants = search_documents(words)
print(f"Documents rellevants trobats: {len(documents_rellevants)}")
for doc in documents_rellevants:
    print(doc)


# In[120]:


# Crear el context
context = ""
for document in documents_rellevants:
    context += f"Document: {document}\n\n"

print(context)


# In[122]:


# Limitar la longitud del context si cal
context = "\n\n".join(documents_rellevants)
max_context_length = 20000  # Ajusta aquest valor segons el límit de tokens de GPT-4 Mini
if len(context) > max_context_length:
    context = context[:max_context_length]
    
prompt = f"{context}\nPregunta: {pregunta}\n\nResposta:"
print(prompt)


# In[124]:


from openai import OpenAI

client = OpenAI(
  api_key='your API key',
)

response = client.chat.completions.create(
    model="gpt-4o-mini",  # Model que farem servir
    messages=[
        {"role": "system", "content": "Ets un assistent que ajuda a respondre preguntes basades en documents facilitats. Sempre has d'informar de la font de l'article"},
        {"role": "user", "content": prompt}
    ],
    max_tokens=350
)



# In[125]:


print(response.choices[0].message.content)


# In[ ]:




