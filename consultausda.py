import zipfile
import pandas as pd
import requests
import io

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

def historico(link, produto, safra):
  link = link
  produto = produto.lower()
  safra = safra
  elif produto == 'milho':
    reporte = 'World Corn Supply and Use'
    paises = ['World', 'United States', 'Brazil', 'Argentina', 'Ukraine']
    head = "Milho:"
  elif produto == 'algodão':
    reporte = 'World and U.S. Supply and Use for Cotton'
    paises = ['World', 'United States', 'Brazil', 'India', 'China',]
    head = "Algodão:"
  elif produto == 'trigo':
    reporte = 'World Wheat Supply and Use'
    paises = ['World', 'United States', 'Brazil', 'Argentina', 'Russia', 'Ukraine' ]
    head = "Trigo:"
  else:
    return
  
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

def baixa_tabela(link):
  download = requests.get(link)
  arquivo = zipfile.ZipFile(io.BytesIO(download.content))
  conteudo = arquivo.namelist()
  conteudo = str(conteudo[0])
  tabela = pd.read_csv(arquivo.open((conteudo)))
  return tabela

def historico_antigo(tabela, produto, safra, ano, mes):
  produto = produto.lower()
  safra = safra
  if produto == 'soja':
    reporte = 'World Soybean Supply and Use'
    paises = ['World', 'United States', 'Brazil', 'Argentina']
    head = "Soja:"
  elif produto == 'milho':
    reporte = 'World Corn Supply and Use'
    paises = ['World', 'United States', 'Brazil', 'Argentina', 'Ukraine']
    head = "Milho:"
  elif produto == 'algodão':
    reporte = 'World and U.S. Supply and Use for Cotton'
    paises = ['World', 'United States', 'Brazil', 'India', 'China',]
    head = "Algodão:"
  elif produto == 'trigo':
    reporte = 'World Wheat Supply and Use'
    paises = ['World', 'United States', 'Brazil', 'Argentina', 'Russia', 'Ukraine' ]
    head = "Trigo:"
  else:
    return
  
  tabela = tabela.query('ForecastYear == @ano and ForecastMonth == @mes and MarketYear == @safra and ReportTitle == @reporte')

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
      
