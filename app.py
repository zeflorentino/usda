from flask import Flask, request, render_template
import json
import requests
import os
from datetime import datetime, timedelta

import funcoes
import telegram_funcoes

TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]

app = Flask(__name__)

@app.route("/")
def menu():
  menu =  render_template('menu.html')
  texto_final = f"<div style="text-align: center;"><h1 style="font-family: Verdana;">Relatório do USDA</h1></div><br><br}{menu}"
  return texto_final

@app.route("/milho-atual")
def milho_atual():
  mes = datetime.now().strftime('%m')
  ano = datetime.now().strftime('%Y')
  texto_meio = funcoes.escreve(mes, ano, "milho")
  texto_final = f"""<font face = "Tahoma" size = "5"><strong>Relatório deste mês.</strong></font><br><br>
        {texto_meio}
        <center><a href="/milho-anterior"><font face = "Tahoma" size = "4"><strong>Relatório do mês passado.</strong></font></a><br><a href="/"><font face = "Tahoma" size = "3"><strong>Retorne ao menu</strong></font></a></center>"""
  return texto_final
  
@app.route("/milho-anterior")
def milho_anterior():
  hoje = datetime.now()
  primeiro_dia = hoje.replace(day=1)
  data_anterior = primeiro_dia - timedelta(days=1)
  mes = data_anterior.strftime('%m')
  ano = data_anterior.strftime('%Y')
  texto_meio = funcoes.escreve(mes, ano, "milho")
  texto_final = f"""<font face = "Tahoma" size = "5"><strong>Relatório do mês passado.</strong></font><br><br>
        {texto_meio}
        <center><a href="/milho-atual"><font face = "Tahoma" size = "4"><strong>Relatório deste mês.</strong></font></a><br><a href="/"><font face = "Tahoma" size = "3"><strong>Retorne ao menu</strong></font></a></center>"""
  return texto_final

@app.route("/soja-atual")
def soja_atual():
  mes = datetime.now().strftime('%m')
  ano = datetime.now().strftime('%Y')
  texto_meio = funcoes.escreve(mes, ano, "soja")
  texto_final = f"""<font face = "Tahoma" size = "5"><strong>Relatório deste mês.</strong></font><br><br>
        {texto_meio}
        <center><a href="/soja-anterior"><font face = "Tahoma" size = "4"><strong>Relatório do mês passado.</strong></font></a><br><a href="/"><font face = "Tahoma" size = "3"><strong>Retorne ao menu</strong></font></a></center>"""
  return texto_final
  
@app.route("/soja-anterior")
def soja_anterior():
  hoje = datetime.now()
  primeiro_dia = hoje.replace(day=1)
  data_anterior = primeiro_dia - timedelta(days=1)
  mes = data_anterior.strftime('%m')
  ano = data_anterior.strftime('%Y')
  texto_meio = funcoes.escreve(mes, ano, "soja")
  texto_final = f"""<font face = "Tahoma" size = "5"><strong>Relatório do mês passado.</strong></font><br><br>
        {texto_meio}
        <center><a href="/soja-atual"><font face = "Tahoma" size = "4"><strong>Relatório deste mês.</strong></font></a><br><a href="/"><font face = "Tahoma" size = "3"><strong>Retorne ao menu</strong></font></a></center>"""
  return texto_final

@app.route("/trigo-atual")
def trigo_atual():
  mes = datetime.now().strftime('%m')
  ano = datetime.now().strftime('%Y')
  texto_meio = funcoes.escreve(mes, ano, "trigo")
  texto_final = f"""<font face = "Tahoma" size = "5"><strong>Relatório deste mês.</strong></font><br><br>
        {texto_meio}
        <center><a href="/trigo-anterior"><font face = "Tahoma" size = "4"><strong>Relatório do mês passado.</strong></font></a><br><a href="/"><font face = "Tahoma" size = "3"><strong>Retorne ao menu</strong></font></a></center>"""
  return texto_final
  
@app.route("/trigo-anterior")
def trigo_anterior():
  hoje = datetime.now()
  primeiro_dia = hoje.replace(day=1)
  data_anterior = primeiro_dia - timedelta(days=1)
  mes = data_anterior.strftime('%m')
  ano = data_anterior.strftime('%Y')
  texto_meio = funcoes.escreve(mes, ano, "trigo")
  texto_final = f"""<font face = "Tahoma" size = "5"><strong>Relatório do mês passado.</strong></font><br><br>
        {texto_meio}
        <center><a href="/trigo-atual"><font face = "Tahoma" size = "4"><strong>Relatório deste mês.</strong></font></a><br><a href="/"><font face = "Tahoma" size = "3"><strong>Retorne ao menu</strong></font></a></center>"""
  return texto_final

@app.route("/algodao-atual")
def algodao_atual():
  mes = datetime.now().strftime('%m')
  ano = datetime.now().strftime('%Y')
  texto_meio = funcoes.escreve(mes, ano, "algodao")
  texto_final = f"""<font face = "Tahoma" size = "5"><strong>Relatório deste mês.</strong></font><br><br>
        {texto_meio}
        <center><a href="/trigo-anterior"><font face = "Tahoma" size = "4"><strong>Relatório do mês passado.</strong></font></a><br><a href="/"><font face = "Tahoma" size = "3"><strong>Retorne ao menu</strong></font></a></center>"""
  return texto_final
  
@app.route("/algodao-anterior")
def algodao_anterior():
  hoje = datetime.now()
  primeiro_dia = hoje.replace(day=1)
  data_anterior = primeiro_dia - timedelta(days=1)
  mes = data_anterior.strftime('%m')
  ano = data_anterior.strftime('%Y')
  texto_meio = funcoes.escreve(mes, ano, "algodao")
  texto_final = f"""<font face = "Tahoma" size = "5"><strong>Relatório do mês passado.</strong></font><br><br>
        {texto_meio}
        <center><a href="/trigo-atual"><font face = "Tahoma" size = "4"><strong>Relatório deste mês.</strong></font></a><br><a href="/"><font face = "Tahoma" size = "3"><strong>Retorne ao menu</strong></font></a></center>"""
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
  safra = str(request.form['safra'])
  produto = str(request.form['produto'])
  resultado = funcoes.historico(link, produto, safra)
  mostra = f"""<font face = "Tahoma" size = "4"><strong>Destaques do relatório de {mes}/{ano} sobre a safra {safra} de {produto}:</strong></font><br><br>{resultado}"""
  return mostra

if __name__ == '__main__':
    app.run(debug=True)
