import zipfile
import pandas as pd
import requests
import io
import altair as alt



def baixa_tabela(link):
  download = requests.get(link)
  arquivo = zipfile.ZipFile(io.BytesIO(download.content))
  conteudo = arquivo.namelist()
  conteudo = str(conteudo[0])
  tabela = pd.read_csv(arquivo.open((conteudo)))
  return tabela

def faz_grafico(tabela, safra, produto, ano, mes):
  produto = produto.lower()
  safra = safra
  if produto == 'soja':
    reporte = 'World Soybean Supply and Use'
  elif produto == 'milho':
    reporte = 'World Corn Supply and Use'
  elif produto == 'algodão':
    reporte = 'World Cotton Supply and Use'
  elif produto == 'trigo':
    reporte = 'World Wheat Supply and Use'
  else:
    return
  
  tabela = tabela.query('MarketYear	== @safra and ReportTitle == @reporte and ForecastYear == @ano and ForecastMonth == @mes')  
  tabela = tabela.loc[:, ['Region', 'Attribute', 'Value']] 
  tabela.columns = ['Local', 'Categoria', 'Estimativa']
  
  
  categorias = {'Beginning Stocks' : 'Estoques iniciais',
                'Domestic Crush' : 'Esmagamento interno',
                'Domestic Total' : 'Demanda total', 
                'Domestic Feed' : 'Demanda para alimentação',
                'Domestic Use' : 'Demanda interna',
                'Ending Stocks' : 'Estoques finais', 
                'Exports' : 'Exportações', 
                'Imports' : 'Importações',
                'Production' : 'Produção',
                'Loss' : 'Perdas'}
  tabela["Categoria"] = tabela["Categoria"].map(categorias)

  locais = {'Afr. Fr. Zone': 'Zona da Franco-Africana', 
            'Australia': 'Austrália', 
            'Bangladesh': 'Bangladesh', 
            'Brazil': 'Brasil', 
            'Central Asia': 'Ásia Central', 
            'China': 'China', 
            'European Union': 'União Europeia', 
            'India': 'Índia', 
            'Indonesia': 'Indonésia', 
            'Major Exporters': 'Principais Exportadores', 
            'Major Importers': 'Principais Importadores', 
            'Mexico': 'México', 
            'Pakistan': 'Paquistão', 
            'S. Hemis.': 'Hemisfério Sul', 
            'Thailand': 'Tailândia', 
            'Total Foreign': 'Total Estrangeiro', 
            'Turkey': 'Turquia', 
            'United States': 'Estados Unidos', 
            'Vietnam': 'Vietnã', 
            'World': 'Mundo', 
            'World Less China': 'Mundo sem China', 
            'Argentina': 'Argentina', 
            'Canada': 'Canadá', 
            'Egypt': 'Egito', 
            'Japan': 'Japão', 
            'Kazakhstan': 'Cazaquistão', 
            'N. Africa': 'Norte da África', 
            'Nigeria': 'Nigéria', 
            'Russia': 'Rússia', 
            'Sel. Mideast': 'Oriente Médio Selecionado', 
            'South Africa': 'África do Sul', 
            'South Korea': 'Coreia do Sul', 
            'Paraguay': 'Paraguai', 
            'Ukraine': 'Ucrânia', 
            'United Kingdom': 'Reino Unido',
            'Southeast Asia' : 'Sudeste Asiático'
            }

  tabela["Local"] = tabela["Local"].map(locais)

  agrupado = tabela.groupby('Categoria')
  graficos = []
  for categoria, data in agrupado:
    chart = alt.Chart(data).mark_bar().encode(x='Value', 
                                              y=alt.Y('Region', sort='-x'), 
                                              color='Region').properties(
      title='Projeções do USDA em milhões de toneladas',
      width=600,
      height=400).interactive()
    graficos.append(chart)
    
  grafico_final = alt.vconcat(*graficos)
  
  tabelavert = tabela.pivot(index='Local', columns='Categoria', values='Estimativa')

  tabelahtml = tabelavert.to_html(index = True)

  return grafico_final, tabelahtml
