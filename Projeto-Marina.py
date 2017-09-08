
# coding: utf-8

# In[ ]:

get_ipython().system('pip install tqdm pymongo')


# In[ ]:

import json
import requests
import datetime
import urllib.parse
import pandas as pd
from tqdm import tqdm
from pprint import pprint
from pymongo import MongoClient


# In[ ]:

'''
site: https://painelhost.uol.com.br/myProducts.html
email: reis.marina@gmail.com
senha: moranGO21
user do banco: rider
senha do banco:mor@nGO21
'''

MONGO = {
    'database': 'bike',
    'username': 'rider',
    'password': 'mor@nGO21',
    'host': 'bike.mongodb.uhserver.com'
}
client = MongoClient(
    'mongodb://{}:{}@{}/{}'.format(urllib.parse.quote(MONGO['username']), urllib.parse.quote(MONGO['password']), MONGO['host'], MONGO['database']))

db = client.bike
table_horarios = db.horarios


# In[ ]:

def teste(data):
    arrStacao = []
    for estacao in data["network"]["stations"]:
        dictSituacao = {
            "free_bikes" : estacao["free_bikes"],
            "empty_slots" : estacao["empty_slots"],
            "dia" : estacao["timestamp"][0:10],
            "hora" : estacao["timestamp"][11:19]
        }
        
        if(estacao["empty_slots"] == None):
            estacao["empty_slots"] = 0
        if(estacao["free_bikes"] == None):
            estacao["free_bikes"] = 0
            
        dictEstacao = {
            "lat" : estacao["latitude"],
            "lng" : estacao["longitude"],
            "nomeEstacao" : estacao["name"],
            "capacidade" : int(estacao["empty_slots"]) + int(estacao["free_bikes"]),
            "id" : estacao["id"],
            "situacao" : dictSituacao
        }
        arrStacao.append(dictEstacao)
    try:
        sistema = {
            "nomedoSistema": data["network"]["name"],
            "referencia": data["network"]["href"],
            "cidade": data["network"]["location"]["city"],
            "pais": data["network"]["location"]["country"],
            "operador": data["network"]["company"],
            "estacao": arrStacao
        }
    finally:
        return sistema
    #print (sistema)


# In[ ]:

while True:
    with open('bike-new-age.json') as data_file:    
        linksAll = json.load(data_file)

    listAll = []
    for i, href in zip(tqdm(range(len(linksAll["networks"]))), linksAll["networks"]):
        responseSistema = requests.get("https://api.citybik.es"+href["href"])
        data = responseSistema.json()
        saveData = teste(data)
        table_horarios.insert_one(saveData)
        listAll.append(saveData)
        #print(listAll)
        #break

