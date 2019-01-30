import xlsxwriter
from crawler import getDisciplina
from bs4 import BeautifulSoup
#from crawler import escreverExcel
import requests
import json

wb = xlsxwriter.Workbook('faltas_disciplina_ecausp.xlsx')
ws = wb.add_worksheet()

row = 0
col = 0

def getTodasAsSiglasPoli():
    url = "http://www3.eca.usp.br/ctr/disciplinas"
    dados = requests.get(url)
    texto = dados.text
    soup = BeautifulSoup(texto, features="html.parser")
    contador = 0
    siglas = []
    for a in soup.findAll('a', {'title': 'no Júpiter'}):
        nome_materia = str(a.string)
        print(nome_materia[1:8])
        sigla_materia = nome_materia[1:8]
        siglas.append(sigla_materia)

    
    print('LEN DE SIGLAS')
    print(len(siglas))
    print(siglas)


    return siglas

faltas = []
todas_as_siglas = getTodasAsSiglasPoli()

for i in range(0, len(todas_as_siglas)):
    falta = getDisciplina(todas_as_siglas[i], 130)
    
    ws.write(row, col, todas_as_siglas[i])
    ws.write(row, col + 1, falta)

    row += 1

wb.close()

