from flask import Flask, request, render_template
import json
import requests
import os
from datetime import datetime, timedelta
import pandas as pd

import funcoes
import telegram_funcoes
from graficos_usda import faz_grafico, baixa_tabela

TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]

app = Flask(__name__)

hoje = datetime.now().strftime("%m%y")
data_hoje = datetime.now()
primeiro_dia = data_hoje.replace(day=1)
data_anterior = primeiro_dia - timedelta(days=1)
data_anterior = data_anterior.strftime("%m%y")

@app.route("/")
def menu():
  return render_template('menu.html',
                         soja_link='/soja-atual',
                         milho_link='/milho-atual',
                         trigo_link='/trigo-atual',
                         algodao_link='/algodao-atual',
                         soja_antigo_link='/soja-anterior',
                         milho_antigo_link='/milho-anterior',
                         trigo_antigo_link='/trigo-anterior',
                         algodao_antigo_link='/algodao-anterior',
                         consulta_link='/consulta',
                         soja_text='Soja',
                         milho_text='Milho',
                         trigo_text='Trigo',
                         algodao_text='Algodão',
                         soja_antigo_text='Soja antigo',
                         milho_antigo_text='Milho antigo',
                         trigo_antigo_text='Trigo antigo',
                         algodao_antigo_text='Algodão antigo',
                         consulta_text='Consulte relatórios')

@app.route("/milho-atual")
def milho_atual():
  texto_meio = funcoes.exibe_texto(hoje, 'Milho')
  return render_template('estrutura.html',
                  titulo = 'Relatório deste mês',
                  opcao = 'Relatório do mês passado',
                  texto_meio = texto_meio,
                  url_passado = 'https://usda-zeflorentino.onrender.com/milho-anterior',
                  url_menu = 'https://usda-zeflorentino.onrender.com/')
  
@app.route("/milho-anterior")
def milho_anterior():
  texto_meio = funcoes.exibe_texto(data_anterior, 'Milho')
  return render_template('estrutura.html',
                  titulo = 'Relatório do mês passado',
                  opcao = 'Relatório do mês atual',
                  texto_meio = texto_meio,
                  url_passado = 'https://usda-zeflorentino.onrender.com/milho-atual',
                  url_menu = 'https://usda-zeflorentino.onrender.com/')

@app.route("/soja-atual")
def soja_atual():
  texto_meio = funcoes.exibe_texto(hoje, 'Soja')
  return render_template('estrutura.html',
                  titulo = 'Relatório deste mês',
                  opcao = 'Relatório do mês passado',
                  texto_meio = texto_meio,
                  url_passado = 'https://usda-zeflorentino.onrender.com/soja-anterior',
                  url_menu = 'https://usda-zeflorentino.onrender.com/')
  
@app.route("/soja-anterior")
def soja_anterior():
  texto_meio = funcoes.exibe_texto(data_anterior, 'Soja')
  return render_template('estrutura.html',
                  titulo = 'Relatório do mês passado',
                  opcao = 'Relatório do mês atual',
                  texto_meio = texto_meio,
                  url_passado = 'https://usda-zeflorentino.onrender.com/soja-atual',
                  url_menu = 'https://usda-zeflorentino.onrender.com/')

@app.route("/trigo-atual")
def trigo_atual():
  texto_meio = funcoes.exibe_texto(hoje, 'Trigo')
  return render_template('estrutura.html',
                  titulo = 'Relatório deste mês',
                  opcao = 'Relatório do mês passado',
                  texto_meio = texto_meio,
                  url_passado = 'https://usda-zeflorentino.onrender.com/trigo-anterior',
                  url_menu = 'https://usda-zeflorentino.onrender.com/')
  
@app.route("/trigo-anterior")
def trigo_anterior():
  texto_meio = funcoes.exibe_texto(data_anterior, 'Trigo')
  return render_template('estrutura.html',
                  titulo = 'Relatório do mês passado',
                  opcao = 'Relatório deste mês',
                  texto_meio = texto_meio,
                  url_passado = 'https://usda-zeflorentino.onrender.com/trigo-atual',
                  url_menu = 'https://usda-zeflorentino.onrender.com/')

@app.route("/algodao-atual")
def algodao_atual():
  texto_meio = funcoes.exibe_texto(hoje, 'Algodão')
  return render_template('estrutura.html',
                  titulo = 'Relatório deste mês',
                  opcao = 'Relatório do mês passado',
                  texto_meio = texto_meio,
                  url_passado = 'https://usda-zeflorentino.onrender.com/algodao-anterior',
                  url_menu = 'https://usda-zeflorentino.onrender.com/')
  
@app.route("/algodao-anterior")
def algodao_anterior():
  texto_meio = funcoes.exibe_texto(data_anterior, 'Algodão')
  return render_template('estrutura.html',
                  titulo = 'Relatório do mês passado',
                  opcao = 'Relatório deste mês',
                  texto_meio = texto_meio,
                  url_passado = 'https://usda-zeflorentino.onrender.com/algodao-atual',
                  url_menu = 'https://usda-zeflorentino.onrender.com/')

@app.route("/botdoze", methods=["POST"])
def telegram_bot():
  update = request.json
  telegram_funcoes.processa_update(update)
  return "Ok"

@app.route('/consulta')
def consulta():
  return render_template('index.html')

@app.route('/resultado', methods=['POST'])
def resultado():
  ano = str(request.form['ano'])
  ano2 = int(request.form['ano'])
  mes = str(request.form['mes'])
  mes2 = int(request.form['mes'])
  safra = str(request.form['safra'])
  produto = str(request.form['produto'])
  if ano2 > 2020:
    arquivo = pd.read_csv(f'https://www.usda.gov/sites/default/files/documents/oce-wasde-report-data-{ano}-0{mes}.csv')
  elif ano2 > 2015:
    arquivo = baixa_tabela('https://www.usda.gov/sites/default/files/documents/oce-wasde-report-data-2016-01-to-2020-12.zip')
  elif ano2 > 2009:
    arquivo = baixa_tabela('https://www.usda.gov/sites/default/files/documents/oce-wasde-report-data-2010-04-to-2015-12.zip')
  else:
    resultado = 'A combinação não está disponível'
  
  conteudo = faz_grafico(arquivo, safra, produto, ano2, mes2)
  grafico = conteudo[0]
  tabela = conteudo[1]
  
  return render_template('grafico.html', chart = grafico.to_json(), table = tabela)

if __name__ == '__main__':
    app.run(debug=True)
