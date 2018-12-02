from crawler import getDisciplina
from bs4 import BeautifulSoup
import requests
import json

def getTodasAsSiglasPoli():
    url = "https://uspdigital.usp.br/jupiterweb/jupDisciplinaLista?codcg=3&letra=A-Z&tipo=D"
    dados = requests.get(url)
    texto = dados.text
    soup = BeautifulSoup(texto, features="html.parser")
    contador = 0
    siglas = []
    for span in soup.findAll('span', {'class': 'txt_arial_8pt_gray'}):
        if contador % 4 == 0:
            sigla = str(span.string)
            siglas.append(sigla[-7:])
    
    siglas_filtradas = []
    for i in range(0, len(siglas)):
        if i % 4 == 0:
            siglas_filtradas.append(siglas[i])

    return siglas_filtradas



todas_as_siglas = getTodasAsSiglasPoli()
for i in range(0, len(todas_as_siglas)):
    getDisciplina(todas_as_siglas[i], 130)
