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



def texto_milho(data):
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

    paises = ['World  3/', 'United States', 'Brazil', 'Argentina', 'Ukraine']

    texto = f""

    for pais in paises:
      tabela_pais = tabela_milho.query('local == @pais')
      
      colunas = ['producao', 'uso_total', 'exportacao', 'estoques_finais']
      for coluna in colunas:
        tabela_pais[f'variacao_' + coluna] = float(tabela_pais[coluna].iloc[1]) / float(tabela_pais[coluna].iloc[0]) * 100 - 100
        tabela_pais[f'variacao_' + coluna] = round(tabela_pais[f'variacao_' + coluna], 1)

      for coluna in colunas:
        numero = tabela_pais[coluna].iloc[1]
 
        lista_paises = {'World  3/': 'no mundo', 
                        'United States' : 'nos EUA',
                        'Brazil' : 'no Brasil',
                        'Argentina' : 'na Argentina',
                        'Ukraine' : 'na Ucrânia'}
        str_pais = pais
        for chave, valor in lista_paises.items():
          str_pais = str_pais.replace(chave, valor)

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
        else:
          unidade = "milhão"
          numero = ponto_para_virgula(numero)  

        if coluna == 'producao':
          mensagem = f'<strong>Milho:</strong> USDA {movimento} estimativa de produção {str_pais} na safra 2022/23{varia}{complemento} {numero} {unidade} de toneladas <br><br>'

        elif coluna == 'uso_total':
          mensagem = f'<strong>Milho:</strong> USDA {movimento} previsão de demanda {str_pais} na safra 2022/23{varia}{complemento} {numero}  {unidade} de toneladas <br><br>'
          
        elif coluna == 'exportacao':
          mensagem = f'<strong>Milho:</strong> USDA {movimento} projeção de exportações {str_pais} na safra 2022/23{varia}{complemento} {numero}  {unidade} de toneladas <br><br>'

        else:
          mensagem = f'<strong>Milho:</strong> USDA {movimento} perspectiva de estoques finais {str_pais} na safra 2022/23{varia}{complemento} {numero}  {unidade} de toneladas <br><br>'

        texto += mensagem

  except:
    texto = "O relatório ainda não está disponível!"      
  
  return texto





def texto_soja(data):
  try: 

    download = requests.get(f'https://www.usda.gov/oce/commodity/wasde/wasde{data}.xls')

    tabela_soja = pd.read_excel(download.content, sheet_name = "Page 28", skiprows=40)

    tabela_soja.columns = ['local', 'mes', 'estoques_iniciais', 'producao', 'importacao', 'esmagamento', 'uso_total', 'exportacao', 'estoques_finais']

    tabela_soja['local'].fillna(method='pad', inplace=True)

    tabela_soja = tabela_soja.reset_index()

    tabela_soja = tabela_soja.drop(columns = ['index'])

    tabela_soja['local'] = tabela_soja['local'].str.strip()

    tabela_soja['mes'] = tabela_soja['mes'].str.strip()
    
    texto_final = f''

    paises = ['World  2/', 'United States', 'Brazil', 'Argentina']

    colunas = ['producao', 'uso_total', 'exportacao', 'estoques_finais']

    for pais in paises:
      tabela_pais = tabela_soja.query('local == @pais')
      for coluna in colunas:
        tabela_pais[f'variacao_' + coluna] = float(tabela_pais[coluna].iloc[1]) / float(tabela_pais[coluna].iloc[0]) * 100 - 100
        tabela_pais[f'variacao_' + coluna] = round(tabela_pais[f'variacao_' + coluna], 1)

      for coluna in colunas:
        numero = tabela_pais[coluna].iloc[1]
        
        lista_paises = {'World  2/' : 'mundial',
                        'United States' : 'nos EUA',
                        'Brazil' : 'no Brasil',
                        'Argentina' : 'na Argentina',
                        'Ukraine' : 'na Ucrânia'}

        str_pais = pais

        for chave, valor in lista_paises.items():
          str_pais = str_pais.replace(chave, valor)

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
        else:
          unidade = "milhão"
          numero = ponto_para_virgula(numero)  

        if coluna == 'producao':
          mensagem = f'Soja: USDA {movimento} estimativa de produção {str_pais} na safra 2022/23{varia}{complemento} {numero} {unidade} de toneladas<br><br>'

        elif coluna == 'uso_total':
          mensagem = f'Soja: USDA {movimento} previsão de demanda {str_pais} na safra 2022/23{varia}{complemento} {numero} {unidade} de toneladas<br><br>'

        elif coluna == 'exportacao':
          mensagem = f'Soja: USDA {movimento} projeção de exportações {str_pais} na safra 2022/23{varia}{complemento} {numero} {unidade} de toneladas<br><br>'

        else:
          mensagem = f'Soja: USDA {movimento} perspectiva de estoques finais {str_pais} na safra 2022/23{varia}{complemento} {numero} {unidade} de toneladas<br><br>'

        texto_final = texto_final + mensagem
  except:
    texto_final = "O relatório ainda não está disponível!"   
  return texto_final





def texto_trigo(data):
  try:
    download = requests.get(f'https://www.usda.gov/oce/commodity/wasde/wasde{data}.xls')

    tabela_trigo = pd.read_excel(download.content, sheet_name = "Page 19", skiprows=9)

    tabela_trigo.columns = ['local', 'mes', 'estoques_iniciais', 'producao', 'importacao', 'uso_domestico', 'uso_total', 'exportacao', 'estoques_finais']

    tabela_trigo['local'].fillna(method='pad', inplace=True)

    tabela_trigo = tabela_trigo.reset_index()

    tabela_trigo = tabela_trigo.drop(columns = ['index'])

    tabela_trigo['local'] = tabela_trigo['local'].str.strip()

    tabela_trigo['mes'] = tabela_trigo['mes'].str.strip()
        
    paises = ['World  3/', 'United States', 'Brazil', 'Argentina', 'Russia', 'Ukraine' ]

    colunas = ['producao', 'uso_total', 'exportacao', 'estoques_finais']

    texto_final = f''

    for pais in paises:
      tabela_pais = tabela_trigo.query('local == @pais')
      for coluna in colunas:
        tabela_pais[f'variacao_' + coluna] = float(tabela_pais[coluna].iloc[1]) / float(tabela_pais[coluna].iloc[0]) * 100 - 100
        tabela_pais[f'variacao_' + coluna] = round(tabela_pais[f'variacao_' + coluna], 1)

      for coluna in colunas:
        numero = tabela_pais[coluna].iloc[1]
              
        lista_paises = {'World  3/' : 'mundial',
                        'United States' : 'nos EUA',
                        'Brazil' : 'no Brasil',
                        'Argentina' : 'na Argentina',
                        'Russia' : 'na Rússia',
                        'Ukraine' : 'na Ucrânia'}

        str_pais = pais

        for chave, valor in lista_paises.items():
          str_pais = str_pais.replace(chave, valor)

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

        if numero > 2:
          unidade = "milhões"
          numero = ponto_para_virgula(numero)
      
        else:
          unidade = "milhão"
          numero = ponto_para_virgula(numero) 

        if coluna == 'producao':
          mensagem = f'Trigo: USDA {movimento} estimativa de produção {str_pais} na safra 2022/23{varia}{complemento} {numero} {unidade} de toneladas<br><br>'

        elif coluna == 'uso_total':
          mensagem = f'Trigo: USDA {movimento} previsão de demanda {str_pais} na safra 2022/23{varia}{complemento} {numero} {unidade} de toneladas<br><br>'

        elif coluna == 'exportacao':
          mensagem = f'Trigo: USDA {movimento} projeção de exportações {str_pais} na safra 2022/23{varia}{complemento} {numero} {unidade} de toneladas<br><br>'

        else:
          mensagem = f'Trigo: USDA {movimento} perspectiva de estoques finais {str_pais} na safra 2022/23{varia}{complemento} {numero} {unidade} de toneladas<br><br>'

        texto_final = texto_final + mensagem  

  except:
    texto_final = "O relatório ainda não está disponível!"   
  return texto_final




def texto_algodao(data):
  try: 

    download = requests.get(f'https://www.usda.gov/oce/commodity/wasde/wasde0323.xls')

    tabela_algodao = pd.read_excel(download.content, sheet_name = "Page 27", skiprows=9)

    tabela_algodao.columns = ['local', 'mes', 'estoques_iniciais', 'producao', 'importacao', 'uso_domestico', 'exportacao', 'perdas', 'estoques_finais']

    tabela_algodao.dropna(subset=['mes'], inplace=True)

    tabela_algodao['local'].fillna(method='pad', inplace=True)

    tabela_algodao = tabela_algodao.reset_index()

    tabela_algodao = tabela_algodao.drop(columns = ['index'])

    tabela_algodao['local'] = tabela_algodao['local'].str.strip()

    tabela_algodao['mes'] = tabela_algodao['mes'].str.strip()
    
    texto_final = f''

    paises = ['World', 'United States', 'Brazil', 'India', 'China',]

    colunas = ['producao', 'uso_domestico', 'exportacao', 'estoques_finais']

    for pais in paises:
      tabela_pais = tabela_algodao.query('local == @pais')
      for coluna in colunas:
        tabela_pais[f'variacao_' + coluna] = float(tabela_pais[coluna].iloc[1]) / float(tabela_pais[coluna].iloc[0]) * 100 - 100
        tabela_pais[f'variacao_' + coluna] = round(tabela_pais[f'variacao_' + coluna], 1)

      for coluna in colunas:
        numero = tabela_pais[coluna].iloc[1] * 0.21772433

        lista_paises = {'World' : 'mundial',
                        'United States' : 'nos EUA',
                        'Brazil' : 'no Brasil',
                        'Argentina' : 'na Argentina',
                        'India' : 'na Índia',
                        'China' : 'na China'}

        str_pais = pais

        for chave, valor in lista_paises.items():
          str_pais = str_pais.replace(chave, valor)

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

        if numero >= 2:
          numero = ponto_para_virgula(numero)
          unidade = 'milhões de'
        
        elif numero > 1:
          unidade = "milhão de"
          numero = ponto_para_virgula(numero)
        else:
          numero = numero * 100
          unidade = "mil"
          numero = ponto_para_virgula(numero)  

        if coluna == 'producao':
          mensagem = f'Algodão: USDA {movimento} estimativa de produção {str_pais} na safra 2022/23{varia}{complemento} {numero} {unidade} toneladas<br><br>'

        elif coluna == 'uso_total':
          mensagem = f'Algodão: USDA {movimento} previsão de demanda {str_pais} na safra 2022/23{varia}{complemento} {numero} {unidade} toneladas<br><br>'

        elif coluna == 'exportacao':
          mensagem = f'Algodão: USDA {movimento} projeção de exportações {str_pais} na safra 2022/23{varia}{complemento} {numero} {unidade} toneladas<br><br>'

        else:
          mensagem = f'Algodão: USDA {movimento} perspectiva de estoques finais {str_pais} na safra 2022/23{varia}{complemento} {numero}  {unidade} toneladas<br><br>'

        texto_final = texto_final + mensagem
  except:
    texto_final = "O relatório ainda não está disponível!"   
  return texto_final





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


