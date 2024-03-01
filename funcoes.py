import os
import requests
from datetime import datetime, timedelta
import pandas as pd


def ponto_para_virgula(numero):
  numero = float(numero)
  numero = round(numero, 2)
  if numero.is_integer():
    numero = str(numero)
    numero = numero.replace('.0', '')
  else:
    numero = str(numero)
    numero = numero.replace('.', ',')
  return numero

def exibe_texto(data, produto):
  try:
    download = requests.get(f'https://www.usda.gov/oce/commodity/wasde/wasde{data}.xls')

    if produto == 'Algodão':
      sheet = 'Page 27'
      pular = 9
      colunas = ['local', 'mes', 'estoques_iniciais', 'producao', 'importacao', 'demanda', 'exportacao', 'perdas', 'estoques_finais']
    elif produto == 'Milho':
      sheet = 16
      pular = 7
      colunas = ['local', 'mes', 'estoques_iniciais', 'producao', 'importacao', 'uso_domestico', 'demanda', 'exportacao', 'estoques_finais']
    elif produto == 'Soja':
      sheet = 'Page 28'
      pular = 40
      colunas = ['local', 'mes', 'estoques_iniciais', 'producao', 'importacao', 'esmagamento', 'demanda', 'exportacao', 'estoques_finais']
    elif produto == 'Trigo':
      sheet = 'Page 19'
      pular = 9
      colunas = ['local', 'mes', 'estoques_iniciais', 'producao', 'importacao', 'esmagamento', 'demanda', 'exportacao', 'estoques_finais']

    tabela = pd.read_excel(download.content, sheet_name = sheet, skiprows = pular)

    tabela.columns = colunas

    tabela.dropna(subset=['mes'], inplace = True)

    tabela['local'].fillna(method = 'pad', inplace = True)

    tabela = tabela.reset_index(drop = True)

    tabela['local'] = tabela['local'].str.strip()

    tabela['mes'] = tabela['mes'].str.strip()

  except:
    tabela = "Não tem"

  try:
    colunas = ['producao', 'demanda', 'exportacao', 'estoques_finais']

    if produto == "Algodão":
      paises = ['World', 'United States', 'Brazil', 'India', 'China',]
      head = "algodão"
    elif produto == 'Soja':
      paises = ['World  2/', 'United States', 'Brazil', 'Argentina']
      head = "soja"
    elif produto == 'Milho':
      paises = ['World  3/', 'United States', 'Brazil', 'Argentina', 'Ukraine']
      head = "milho"
    elif produto == 'Trigo':
      paises = ['World  3/', 'United States', 'Brazil', 'Argentina', 'Russia', 'Ukraine' ]
      head = "trigo"
    else:
      mensagem_final = "O relatório ainda não está disponível!"

    texto = f""

    for pais in paises:
      tabela_pais = tabela.query('local == @pais')
        
        
      for coluna in colunas:
        tabela_pais[f'variacao_' + coluna] = float(tabela_pais[coluna].iloc[1]) / float(tabela_pais[coluna].iloc[0]) * 100 - 100
        tabela_pais[f'variacao_' + coluna] = round(tabela_pais[f'variacao_' + coluna], 1)

      for coluna in colunas:
        if produto == 'Algodão':
          numero = tabela_pais[coluna].iloc[1] * 0.21772433
        else:
          numero = tabela_pais[coluna].iloc[1]
      
        paises = {'World': 'mundial',
                  'World  3/' : 'mundial',
                  'World  2/': 'mundial',
                      'United States' : 'nos EUA', 
                      'Brazil' : 'no Brasil', 
                      'Argentina' : 'na Argentina', 
                      'Ukraine' : 'na Ucrânia', 
                      'India' : 'na Índia', 
                      'Russia' : 'na Rússia', 
                      'China' : 'na China'}

        str_pais = pais
        for chave, valor in paises.items():
          str_pais = str_pais.replace(chave, valor)
          str_pais = str_pais.replace("  3/", "")
          str_pais = str_pais.replace("  2/", "")
      
        percentual = ponto_para_virgula(abs(tabela_pais[f'variacao_{coluna}'].iloc[1]))

        if tabela_pais[f'variacao_{coluna}'].iloc[1] == 0:
          movimento = "se mantém"
          complemento = " em"
          varia = ''

        elif tabela_pais[f'variacao_{coluna}'].iloc[1] >= 0:
                movimento = "sobe"
                complemento = ", para"
                varia = f' em {percentual}%'

        else:
          movimento = "cai"
          complemento = ", para"
          varia = f' em {percentual}%'

        if numero >= 1000.0:
          numero = numero / 1000
          numero = ponto_para_virgula(numero)
          unidade = 'bilhão de'
            
        elif numero > 2:
          unidade = "milhões de"
          numero = ponto_para_virgula(numero)
        
        elif numero > 1:
          unidade = "milhão de"
          numero = ponto_para_virgula(numero)  

        else:
          unidade = "mil"
          numero = numero * 100
          numero = ponto_para_virgula(numero)  
              

        if coluna == 'producao':
          mensagem = f'Agro: Produção {str_pais} de {head} {movimento} {varia}{complemento} {numero} {unidade} t <br><br>'

        elif coluna == 'demanda':
          mensagem = f'Agro: Demanda {str_pais} de {head} {movimento} {varia}{complemento} {numero} {unidade} t  <br><br>'
              
        elif coluna == 'exportacao':
          mensagem = f'Agro: Produção {str_pais} de {head} {movimento} {varia}{complemento} {numero} {unidade} t  <br><br>'

        else:
          mensagem = f'Agro: Produção {str_pais} de {head} {movimento} {varia}{complemento} {numero} {unidade} t  <br><br>'

        texto += mensagem

  except:
    texto = "O relatório ainda não está disponível!"      
  
  return texto


