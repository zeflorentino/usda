from funcoes import importa_bibliotecas, ponto_para_virgula

importa_bibliotecas()

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
