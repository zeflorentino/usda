from flask import Flask, request, render_template
import json
import requests
import os
from datetime import datetime, timedelta

import funcoes
import telegram_funcoes
import consulta

TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]

app = Flask(__name__)

@app.route("/")
def menu():
  texto_final = f"""<br><br><center><font face = "Tahoma" size = "6"><strong><a href="/milho-atual">Milho</a> | <a href="/milho-anterior">Milho Antigo</a><br><br><a href="/soja-atual">Soja</a> | <a href="/soja-anterior">Soja Antigo</a><br><br><a href="/erro">Erro</a></strong></font></center> | <a href="/consulta">Consulta Relatórios</a>"""
  return texto_final

@app.route("/milho-atual")
def milho_atual():
  data_hoje = datetime.now().strftime('%m%y')
  texto_meio = funcoes.texto_milho(data_hoje)
  texto_final = f"""<font face = "Tahoma" size = "6"><strong>Relatório deste mês.</strong></font><br><br>
        {texto_meio}
        <center><a href="/milho-anterior"><font face = "Tahoma" size = "5"><strong>Relatório do mês passado.</strong></font></a><br><a href="/"><font face = "Tahoma" size = "4"><strong>Retorne ao menu</strong></font></a></center>"""
  return texto_final
  
@app.route("/milho-anterior")
def milho_anterior():
  hoje = datetime.now()
  primeiro_dia = hoje.replace(day=1)
  data_anterior = primeiro_dia - timedelta(days=1)
  data_anterior = data_anterior.strftime("%m%y")
  texto_meio = funcoes.texto_milho(data_anterior)
  texto_final = f"""<font face = "Tahoma" size = "6"><strong>Relatório do mês passado.</strong></font><br><br>
        {texto_meio}
        <center><a href="/milho-atual"><font face = "Tahoma" size = "5"><strong>Relatório deste mês.</strong></font></a><br><a href="/"><font face = "Tahoma" size = "4"><strong>Retorne ao menu</strong></font></a></center>"""
  return texto_final

@app.route("/soja-atual")
def soja_atual():
  data_hoje = datetime.now().strftime('%m%y')
  texto_meio = funcoes.texto_soja(data_hoje)
  texto_final = f"""<font face = "Tahoma" size = "6"><strong>Relatório deste mês.</strong></font><br><br>
        {texto_meio}
        <center><a href="/soja-anterior"><font face = "Tahoma" size = "5"><strong>Relatório do mês passado.</strong></font></a><br><a href="/"><font face = "Tahoma" size = "4"><strong>Retorne ao menu</strong></font></a></center>"""
  return texto_final
  
@app.route("/soja-anterior")
def soja_anterior():
  hoje = datetime.now()
  primeiro_dia = hoje.replace(day=1)
  data_anterior = primeiro_dia - timedelta(days=1)
  data_anterior = data_anterior.strftime("%m%y")
  texto_meio = funcoes.texto_soja(data_anterior)
  texto_final = f"""<font face = "Tahoma" size = "6"><strong>Relatório do mês passado.</strong></font><br><br>
        {texto_meio}
        <center><a href="/soja-atual"><font face = "Tahoma" size = "5"><strong>Relatório deste mês.</strong></font></a><br><a href="/"><font face = "Tahoma" size = "4"><strong>Retorne ao menu</strong></font></a></center>"""
  return texto_final
  
@app.route("/erro")
def error():
  data_errada = '0625'
  texto_meio = funcoes.texto_milho(data_errada)
  texto_final = f"""<font face = "Tahoma" size = "6"><strong>Demonstração de erro.</strong></font><br><br>
        {texto_meio}
        <center><a href="/"><font face = "Tahoma" size = "4"><strong>Retorne ao menu</strong></font></a></center>"""
  return texto_final

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
  mes = str(request.form['mes'])
  link = f"https://www.usda.gov/sites/default/files/documents/oce-wasde-report-data-{ano}-{mes}.csv"
  resultado = funcoes.historico(link)
  mostra = f"Veja os resultados!<br><br>{resultado}"
  return mostra

if __name__ == '__main__':
    app.run(debug=True)
