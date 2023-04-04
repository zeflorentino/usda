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





def escreve(mes, ano, produto):
  if mes == "01":
    mes2 = "12"
    ano2 = int(ano) - 1
  else:
    mes2 = int(mes) - 1
    ano2 = ano

  tabela1 = pd.read_csv(f"https://www.usda.gov/sites/default/files/documents/oce-wasde-report-data-{ano}-{mes}.csv")
  tabela2 = pd.read_csv(f"https://www.usda.gov/sites/default/files/documents/oce-wasde-report-data-{ano2}-0{mes2}.csv")
  tabela = tabela1.merge(tabela2, on=list(tabela1.columns), how='outer')

  projecoes = ['Production', 'Domestic Total', 'Exports', 'Ending Stocks']

  if produto == "algodao":
    reporte = 'World Cotton Supply and Use'
    paises = ['World', 'United States', 'Brazil', 'India', 'China']
    head = "Algodão:"
    projecoes = ['Production', 'Domestic Use', 'Exports', 'Ending Stocks']
  elif produto == 'soja':
    reporte = 'World Soybean Supply and Use'
    paises = ['World', 'United States', 'Brazil', 'Argentina']
    head = "Soja:"
  elif produto == 'milho':
    reporte = 'World Corn Supply and Use'
    paises = ['World', 'United States', 'Brazil', 'Argentina', 'Ukraine']
    head = "Milho:"
  elif produto == 'trigo':
    reporte = 'World Wheat Supply and Use'
    paises = ['World', 'United States', 'Brazil', 'Argentina', 'Russia', 'Ukraine']
    head = "Trigo:"
  else:
    mensagem_final = "O relatório ainda não está disponível!"

  tabela = tabela.query('MarketYear	== "2022/23" and ReportTitle == @reporte')  
  tabela = tabela.loc[:, ['Commodity', 'Region', 'Attribute', 'Value']] 

  mensagem_final = f""

  contador_termo = 1

  for pais in paises:
    tabela_nova = tabela.query('Region == @pais')  
    for projecao in projecoes:
      tabela_projecao = tabela_nova.query('Attribute == @projecao')
      tabela_projecao = tabela_projecao.reset_index(drop=True)
      
      projecoes_usda = {'Production' : 'produção', 
                        'Domestic Total' : 'demanda', 
                        'Exports' : 'exportação', 
                        'Ending Stocks' : 
                        'estoque final'}
      paises = {'World': 'mundial', 
                'United States' : 'nos EUA', 
                'Brazil' : 'no Brasil', 
                'Argentina' : 'na Argentina', 
                'Ukraine' : 'na Ucrânia', 
                'India' : 'na Índia', 
                'Russia' : 'na Rússia', 
                'China' : 'na China'}

      pais_corrigir = pais
      for chave, valor in paises.items():
        pais_corrigir = pais_corrigir.replace(chave, valor)

      projecao_corrigir = projecao     
      for chave, valor in projecoes_usda.items():
        projecao_corrigir = projecao_corrigir.replace(chave, valor)

      if produto == "algodao":
        valor = tabela_projecao['Value'].iloc[0] * 0.21772433
      else:
        valor = tabela_projecao['Value'].iloc[0] 
    
      if not tabela_projecao['Value'].empty:
        
          if valor >= 1000.0:
            valor = valor / 1000
            valor = ponto_para_virgula(valor)
            unidade = "bilhão de"
          elif valor > 2:
            unidade = "milhões de"
            valor = ponto_para_virgula(valor)
          elif valor > 1:
            unidade = "milhão de"
            valor = ponto_para_virgula(valor)
          else:
            unidade = "mil"
            valor = ponto_para_virgula(valor)

      variacao_percentual = ((tabela_projecao['Value'].iloc[0]  - tabela_projecao['Value'].iloc[1]) / tabela_projecao['Value'].iloc[1]) * 100
      percentual = ponto_para_virgula(round(abs(variacao_percentual), 1))

      if variacao_percentual == 0:
        movimento = "mantém"
        complemento = " em"
        varia = ''

      elif variacao_percentual >= 0:
        movimento = "eleva"
        complemento = ", para"
        varia = f' em {percentual}%'

      else:
        movimento = "reduz"
        complemento = ", para"
        varia = f' em {percentual}%'  

      if contador_termo == 1:
        termo = "estimativa"
        contador_termo += 1
      elif contador_termo == 2:
        termo = "projeção"
        contador_termo += 1
      elif contador_termo == 3:
        termo = "previsão"
        contador_termo += 1
      else:
        termo = "perspectiva"
        contador_termo = 1
          
      mensagem_final += f'{head} USDA {movimento} {termo} de {projecao_corrigir} {pais_corrigir} na safra 2022/23{varia}{complemento} {valor} {unidade} de toneladas <br><br>'
  return mensagem_final






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
  
  
  
  
  
      
def cabeca(mes, ano):
  if mes == "01":
    mes2 = "12"
    ano2 = int(ano) - 1
  else:
    mes2 = int(mes) - 1
    ano2 = ano

  tabela1 = pd.read_csv(f"https://www.usda.gov/sites/default/files/documents/oce-wasde-report-data-{ano}-{mes}.csv")
  tabela2 = pd.read_csv(f"https://www.usda.gov/sites/default/files/documents/oce-wasde-report-data-{ano2}-0{mes2}.csv")
  tabela = tabela1.merge(tabela2, on=list(tabela1.columns), how='outer')

  projecoes = ['Production', 'Domestic Total', 'Exports', 'Ending Stocks']
  paises = ['World', 'United States', 'Brazil', 'Argentina', 'Ukraine']
  head = "Milho:"

  tabela = tabela.query('MarketYear	== "2022/23" and ReportTitle == "World Corn Supply and Use"')  
  tabela = tabela.loc[:, ['Commodity', 'Region', 'Attribute', 'Value']] 

  mensagem_final = f""

  contador_termo = 1

  for pais in paises:
    tabela_nova = tabela.query('Region == @pais')  
    for projecao in projecoes:
      tabela_projecao = tabela_nova.query('Attribute == @projecao')
      tabela_projecao = tabela_projecao.reset_index(drop=True)
      
      projecoes_usda = {'Production' : 'produção', 
                        'Domestic Total' : 'demanda', 
                        'Exports' : 'exportação', 
                        'Ending Stocks' : 
                        'estoque final'}

      paises = {'World': 'mundial', 
                'United States' : 'nos EUA', 
                'Brazil' : 'no Brasil', 
                'Argentina' : 'na Argentina', 
                'Ukraine' : 'na Ucrânia', 
                'India' : 'na Índia', 
                'Russia' : 'na Rússia', 
                'China' : 'na China'}

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
            unidade = "bilhão de"
          elif valor > 2:
            unidade = "milhões de"
            valor = ponto_para_virgula(valor)
          elif valor > 1:
            unidade = "milhão de"
            valor = ponto_para_virgula(valor)
          else:
            unidade = "mil"
            valor = ponto_para_virgula(valor)

      variacao_percentual = ((tabela_projecao['Value'].iloc[0]  - tabela_projecao['Value'].iloc[1]) / tabela_projecao['Value'].iloc[1]) * 100
      percentual = ponto_para_virgula(round(abs(variacao_percentual), 1))

      if variacao_percentual == 0:
        movimento = "mantém"
        complemento = " em"
        varia = ''

      elif variacao_percentual >= 0:
        movimento = "eleva"
        complemento = ", para"
        varia = f' em {percentual}%'

      else:
        movimento = "reduz"
        complemento = ", para"
        varia = f' em {percentual}%'  

      if contador_termo == 1:
        termo = "estimativa"
        contador_termo += 1
      elif contador_termo == 2:
        termo = "projeção"
        contador_termo += 1
      elif contador_termo == 3:
        termo = "previsão"
        contador_termo += 1
      else:
        termo = "perspectiva"
        contador_termo = 1
          
      mensagem_final += f'{head} USDA {movimento} {termo} de {projecao_corrigir} {pais_corrigir} na safra 2022/23{varia}{complemento} {valor} {unidade} de toneladas <br><br>'
  return mensagem_final
