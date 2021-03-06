from bs4 import BeautifulSoup
import xlsxwriter
import requests
import json

wb = xlsxwriter.Workbook('faltas_disciplina.xlsx')
ws = wb.add_worksheet()

row = 0
col = 0

def escreverExcel(sigla, falta, r, c):
    global ws
    siglas_e_faltas = (
        [sigla, falta],
    )
    for sigla, falta in siglas_e_faltas:
        ws.write(r, c, sigla)
        ws.write(r, c + 1, falta)

        r += 1
    
    wb.close()


    

def getDisciplina(sigla, minutos_de_aula):
    dicionario = {}
    creditos = ['Credito Aula', 'Creditos Trabalho', 'Carga Horaria Total']
    nomes = ['Instituto', 'Curso', '', 'Em ingles']
    if(sigla):
        #url do jupiter com as informações da disciplina em questao
        url = "https://uspdigital.usp.br/jupiterweb/obterDisciplina?sgldis=" + sigla  + "&nomdis="  
        try:
            dados = requests.get(url)
        except:
            return None

    texto = dados.text

    #lib que varre o source-code da pagina e pega as infos
    soup = BeautifulSoup(texto, features="html.parser")

    contador = 0
    for span in soup.findAll('span', {'class' : 'txt_arial_10pt_black'}):
        if contador == 2:
            textcontent = span.b.string
            dicionario[nomes[contador]] = (str(textcontent))
        else:
            textcontent = span.string
            dicionario[nomes[contador]] = (str(textcontent))
        contador += 1
    
    contador = 0
    dicionario['creditos'] = {}
    for span in soup.findAll('span', {'class' : 'txt_arial_8pt_gray'}):
        if contador < 3:
            textcontent = span.string
            dicionario['creditos'][creditos[contador]] = str(textcontent).rstrip('\r\n\t')
        if contador == 5:
            textcontent = span.string
            dicionario['Objetivo'] = str(textcontent).rstrip('\r\n\t')
            break 

        contador += 1

    
    #salvando arquivo com as informações num .txt na pasta disciplinas
    arquivo = open("disciplinas_ecausp/" + sigla + ".txt", "w+")

    for key in dicionario:
        if key == 'creditos':
            for other_key in dicionario[key]:
                arquivo.write('\n')
                arquivo.write(other_key)
                arquivo.write(dicionario[key][other_key])
                arquivo.write('\n')
        else:
            arquivo.write('\n')
            arquivo.write(key)
            arquivo.write(dicionario[key])
            arquivo.write('\n')
    carga_ = []
    try:
        carga_horaria_total = str(dicionario['creditos']['Carga Horaria Total'])
        print(carga_horaria_total)
    except:
        pass
    for i in carga_horaria_total:
        try:
            carga_.append(int(i))
        except:
            pass

    print(carga_)

    if len(carga_) == 2:
        carga_total = 10 * carga_[0] + carga_[1]
    else:
        carga_total = 100 * carga_[0] + 10 * carga_[1] + carga_[2]

    print(carga_total)
    numero_de_aulas = carga_total * 60 / int(minutos_de_aula)
    #calculando 30% de falta que pode ter
    faltas = numero_de_aulas * 0.3
    arquivo.write('\n Voce pode faltar: %s' % int(faltas - 1))
    return faltas


sigla = input('Digite a sigla da matéria: ')
minutos_de_aula = input("Digite a duracao da aula em minutos: ")


faltas = getDisciplina(sigla, minutos_de_aula)
escreverExcel(sigla, faltas, row, col)
if faltas != None:

    #tirando 1 das faltas só pra ficar safe :)
    print('\nVoce pode faltar: %s' % int(faltas - 1))
    print('Para mais informaçoes da disciplina, acesse "disciplinas/<sigla_da_disciplina>.txt"')

else:
    print ("Error")








