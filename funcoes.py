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
      head = "Algodão:"
    elif produto == 'Soja':
      paises = ['World  2/', 'United States', 'Brazil', 'Argentina']
      head = "Soja:"
    elif produto == 'Milho':
      paises = ['World  3/', 'United States', 'Brazil', 'Argentina', 'Ukraine']
      head = "Milho:"
    elif produto == 'Trigo':
      paises = ['World  3/', 'United States', 'Brazil', 'Argentina', 'Russia', 'Ukraine' ]
      head = "Trigo:"
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
          movimento = "mantém"
          complemento = " em"
          varia = ''

        elif tabela_pais[f'variacao_{coluna}'].iloc[1] >= 0:
                movimento = "eleva"
                complemento = ", para"
                varia = f' em {percentual}%'

        else:
          movimento = "reduz"
          complemento = ", para"
          varia = f' em {percentual}%'

        if numero >= 1000.0:
          numero = numero / 1000
          numero = ponto_para_virgula(numero)
          unidade = 'bilhão'
            
        elif numero > 2:
          unidade = "milhões"
          numero = ponto_para_virgula(numero)
        
        elif numero > 1:
          unidade = "milhão"
          numero = ponto_para_virgula(numero)  

        else:
          unidade = "mil"
          numero = numero * 100
          numero = ponto_para_virgula(numero)  
              

        if coluna == 'producao':
          mensagem = f'Agro: Produção {str_pais} de {produto} {movimento} {varia}, {complemento} {numero} {unidade} t <br><br>'

        elif coluna == 'demanda':
          mensagem = f'Agro: Demanda {str_pais} de {produto} {movimento} {varia}, {complemento} {numero} {unidade} t  <br><br>'
              
        elif coluna == 'exportacao':
          mensagem = f'Agro: Produção {str_pais} de {produto} {movimento} {varia}, {complemento} {numero} {unidade} t  <br><br>'

        else:
          mensagem = f'Agro: Produção {str_pais} de {produto} {movimento} {varia}, {complemento} {numero} {unidade} t  <br><br>'

        texto += mensagem

  except:
    texto = "O relatório ainda não está disponível!"      
  
  return texto

def historico(link, produto, safra):
  link = link
  produto = produto
  safra = safra
  if produto == 'soja':
    reporte = 'World Soybean Supply and Use'
    paises = ['World', 'United States', 'Brazil', 'Argentina']
    head = "Soja:"
  else:
    reporte = 'World Corn Supply and Use'
    paises = ['World', 'United States', 'Brazil', 'Argentina', 'Ukraine']
    head = "Milho:"
  
  tabela = pd.read_csv(link)
  tabela = tabela.query('MarketYear	== @safra and ReportTitle == @reporte')  
  tabela = tabela.loc[:, ['Commodity', 'Region', 'Attribute', 'Value']] 
  
  mensagem_final = f""
  
  projecoes = ['Production', 'Domestic Total', 'Exports', 'Ending Stocks']
  
  for pais in paises:
    tabela_nova = tabela.query('Region == @pais')  
    for projecao in projecoes:
      tabela_projecao = tabela_nova.query('Attribute == @projecao')
      tabela_projecao = tabela_projecao.reset_index(drop=True)
      projecoes_usda = {'Production' : 'produção', 'Domestic Total' : 'demanda', 'Exports' : 'exportação', 'Ending Stocks' : 'estoques finais'}

      paises = {'World': 'mundial', 'United States' : 'nos EUA', 'Brazil' : 'no Brasil', 'Argentina' : 'na Argentina', 'Ukraine' : 'na Ucrânia'}
        
      pais_corrigir = pais
      for chave, valor in paises.items():
        pais_corrigir = pais_corrigir.replace(chave, valor)    

      projecao_corrigir = projecao     
      for chave, valor in projecoes_usda.items():
        projecao_corrigir = projecao_corrigir.replace(chave, valor)
      
      valor = tabela_projecao['Value'].iloc[0]

      if not tabela_projecao['Value'].empty:
        
        if valor >= 1000.0:
          valor = valor / 1000
          valor = ponto_para_virgula(valor)
          complemento = "bilhão"
        elif valor > 2:
          complemento = "milhões"
          valor = ponto_para_virgula(valor)
        else:
          complemento = "milhão"
          valor = ponto_para_virgula(valor)
        
      mensagem_final += f'{head} USDA estimava {projecao_corrigir} {pais_corrigir} na safra {safra} em {valor} {complemento} de toneladas.<br><br>'
        
      
  return mensagem_final
      
      
def texto_cabeca(data):
  try: 
    download = requests.get(f'https://www.usda.gov/oce/commodity/wasde/wasde{data}.xls')

    tabela_milho = pd.read_excel(download.content, sheet_name = 16, skiprows=7)

    tabela_milho.columns = ['local', 'mes', 'estoques_iniciais', 'producao', 'importacao', 'uso_domestico', 'uso_total', 'exportacao', 'estoques_finais']

    tabela_milho = tabela_milho[2:]

    tabela_milho['local'].fillna(method='pad', inplace=True)

    tabela_milho = tabela_milho.reset_index()

    tabela_milho = tabela_milho.drop(columns = ['index'])

    tabela_milho['local'] = tabela_milho['local'].str.strip()

    tabela_milho['mes'] = tabela_milho['mes'].str.strip()

    tabela_mundo = tabela_milho.query('local == "World  3/"')

    colunas = ['producao', 'uso_total', 'exportacao', 'estoques_finais']

    texto_mundo = f""

    for coluna in colunas:
      if coluna == 'producao':
        numero = tabela_mundo[coluna].iloc[1] / 1000
        numero = ponto_para_virgula(numero)
      elif coluna == 'uso_total':
        numero = tabela_mundo[coluna].iloc[1] / 1000
        numero = ponto_para_virgula(numero)
      else:
        numero = tabela_mundo[coluna].iloc[1]
        numero = ponto_para_virgula(numero)

      if coluna == 'producao':
        mensagem = f'O Departamento de Agricultura dos Estados Unidos estimou hoje que a produção mundial de milho na safra 2022/23 chegará a {numero} bilhão de toneladas. '

      elif coluna == 'uso_total':
        mensagem = f'Já a previsão de demanda global é de {numero} bilhão de toneladas. '

      elif coluna == 'exportacao':
        mensagem = f'Desse total, cerca de {numero} milhões de toneladas devem ser exportadas entre as nações. '
      else:
        mensagem = f'Ao final da temporada, o órgão americano projeta que haverão {numero} milhões de toneladas estocadas.'

      texto_mundo = texto_mundo + mensagem
  except:
     texto_mundo = "Ainda não há relatório."

  return texto_mundo
