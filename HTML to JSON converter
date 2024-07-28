#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import json
import re


# In[25]:


def fetch_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extrect el titol de l'article
    title = soup.find('h1', class_='entry-title').text.strip()
    
    # Extrect el contingut de l'article
    content_div = soup.find('div', class_='entry-content')
    elements = content_div.find_all(['h2', 'p'])
    
    # Organitzo el contingut per capitols
    article_content = {}
    current_chapter = "Introduction"  # Default chapter for any text before the first H2
    article_content[current_chapter] = []
    
    for element in elements:
        if element.name == 'h2':
            current_chapter = element.text.strip()
            article_content[current_chapter] = []
        elif element.name == 'p':
            article_content[current_chapter].append(element.text.strip())
    
    # Preparo l'estructura del JSON
    article_json = {
        "title": title,
        "url": url,
        "content": article_content
    }
    
    return article_json
    
def extract_last_non_empty_word(url):
    # Utilitzar una expressió regular per trobar totes les paraules entre les barres invertides
    matches = re.findall(r'/([^/]*)', url)
    
    # Filtrar les coincidències per eliminar les buides
    non_empty_matches = [match for match in matches if match]
    
    # Retornar l'última paraula no buida o None si no hi ha coincidències
    return non_empty_matches[-1] if non_empty_matches else None


# In[27]:


def save_article_to_json(article_json, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(article_json, f, ensure_ascii=False, indent=4)
    print(f"Article saved to {file_path}")


# In[29]:


# URL of the article
urls = [
    "https://arnaudunjo.com/ca/2024/07/07/creacio-dun-chatgpt-personalitzat-agent-gpt/",
    "https://arnaudunjo.com/ca/2023/01/31/generant-codi-amb-gpt-3/",
    "https://arnaudunjo.com/ca/2021/10/04/alarma-domestica-amb-raspberry-pi/",
    "https://arnaudunjo.com/ca/2021/04/25/introduccio-al-machine-learning-aprenentatge-automatic/",
    "https://arnaudunjo.com/ca/2021/04/25/machine-learning-model-classificador-de-textos-en-python/",
    "https://arnaudunjo.com/ca/2021/02/11/millorant-la-seguretat-i-la-privacitat-en-les-comunicacions-amb-raspberry-pi/",
    "https://arnaudunjo.com/ca/2021/01/13/opinio-moonlander-mk1/",
    "https://arnaudunjo.com/ca/2020/12/17/desenvolupament-duna-aplicacio-blockchain-desde-0-amb-python/"
]

for url in urls: 
    last_word = extract_last_non_empty_word(url)
    
    # Fetch the article and create JSON structure
    article_json = fetch_article(url)
    
    # Save the article JSON to a file
    file_path = last_word + ".json"
    save_article_to_json(article_json, file_path)


# In[ ]:




