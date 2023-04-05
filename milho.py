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
