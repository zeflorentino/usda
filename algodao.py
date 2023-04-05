from funcoes import importa_bibliotecas, ponto_para_virgula

importa_bibliotecas()

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
