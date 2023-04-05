from funcoes import importa_bibliotecas, ponto_para_virgula

importa_bibliotecas()

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

