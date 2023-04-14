import requests
from datetime import datetime, timedelta
import pandas as pd

def tabela_grafico(tabela, safra, produto, ano, mes):
  produto = produto.lower()
  safra = safra
  if produto == 'soja':
    reporte = 'World Soybean Supply and Use'
    head = "Soja:"
  elif produto == 'milho':
    reporte = 'World Corn Supply and Use'
    head = "Milho:"
  elif produto == 'algodão':
    reporte = 'World Cotton Supply and Use'
    head = "Algodão:"
  elif produto == 'trigo':
    reporte = 'World Wheat Supply and Use'
    head = "Trigo:"
  else:
    return
  
  tabela = tabela.query('MarketYear	== @safra and ReportTitle == @reporte ForecastYear == @ano and ForecastMonth == "mes"')  
  tabela = tabela.loc[:, ['Commodity', 'Region', 'Attribute', 'Value']] 
  tabela.columns = ['Commodity', 'Local', 'Categoria', 'Estimativa']
  
  
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

  grafico = alt.Chart(tabela).mark_circle(color="red", opacity=0.5).encode(
    x='Estimativa',
    y= 'Categoria',
    color = 'Local',
    size = alt.Size('Estimativa', scale=alt.Scale(range=[50, 400])),
    tooltip=['Local', 'Categoria', 'Estimativa']).properties(
    title='Projeções do USDA em milhões de toneladas',
    width=700,
    height=400).interactive()
  
  tabelahtml = tabela.to_html(index=False)

  return grafico, tabelahtml
