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
  data_hoje = datetime.now().strftime('%m%y')
  texto_meio = funcoes.texto_milho(data_hoje)
  texto_final = f"""<font face = "Tahoma" size = "5"><strong>Relatório deste mês.</strong></font><br><br>
        {texto_meio}
        <center><a href="/milho-anterior"><font face = "Tahoma" size = "4"><strong>Relatório do mês passado.</strong></font></a><br><a href="/"><font face = "Tahoma" size = "3"><strong>Retorne ao menu</strong></font></a></center>"""
  return texto_final
  
@app.route("/milho-anterior")
def milho_anterior():
  hoje = datetime.now()
  primeiro_dia = hoje.replace(day=1)
  data_anterior = primeiro_dia - timedelta(days=1)
  data_anterior = data_anterior.strftime("%m%y")
  texto_meio = funcoes.texto_milho(data_anterior)
  texto_final = f"""<font face = "Tahoma" size = "5"><strong>Relatório do mês passado.</strong></font><br><br>
        {texto_meio}
        <center><a href="/milho-atual"><font face = "Tahoma" size = "4"><strong>Relatório deste mês.</strong></font></a><br><a href="/"><font face = "Tahoma" size = "3"><strong>Retorne ao menu</strong></font></a></center>"""
  return texto_final

@app.route("/soja-atual")
def soja_atual():
  data_hoje = datetime.now().strftime('%m%y')
  texto_meio = funcoes.texto_soja(data_hoje)
  texto_final = f"""<font face = "Tahoma" size = "5"><strong>Relatório deste mês.</strong></font><br><br>
        {texto_meio}
        <center><a href="/soja-anterior"><font face = "Tahoma" size = "4"><strong>Relatório do mês passado.</strong></font></a><br><a href="/"><font face = "Tahoma" size = "3"><strong>Retorne ao menu</strong></font></a></center>"""
  return texto_final
  
@app.route("/soja-anterior")
def soja_anterior():
  hoje = datetime.now()
  primeiro_dia = hoje.replace(day=1)
  data_anterior = primeiro_dia - timedelta(days=1)
  data_anterior = data_anterior.strftime("%m%y")
  texto_meio = funcoes.texto_soja(data_anterior)
  texto_final = f"""<font face = "Tahoma" size = "5"><strong>Relatório do mês passado.</strong></font><br><br>
        {texto_meio}
        <center><a href="/soja-atual"><font face = "Tahoma" size = "4"><strong>Relatório deste mês.</strong></font></a><br><a href="/"><font face = "Tahoma" size = "3"><strong>Retorne ao menu</strong></font></a></center>"""
  return texto_final

@app.route("/trigo-atual")
def trigo_atual():
  data_hoje = datetime.now().strftime('%m%y')
  texto_meio = funcoes.texto_trigo(data_hoje)
  texto_final = f"""<font face = "Tahoma" size = "5"><strong>Relatório deste mês.</strong></font><br><br>
        {texto_meio}
        <center><a href="/trigo-anterior"><font face = "Tahoma" size = "4"><strong>Relatório do mês passado.</strong></font></a><br><a href="/"><font face = "Tahoma" size = "3"><strong>Retorne ao menu</strong></font></a></center>"""
  return texto_final
  
@app.route("/trigo-anterior")
def trigo_anterior():
  hoje = datetime.now()
  primeiro_dia = hoje.replace(day=1)
  data_anterior = primeiro_dia - timedelta(days=1)
  data_anterior = data_anterior.strftime("%m%y")
  texto_meio = funcoes.texto_trigo(data_anterior)
  texto_final = f"""<font face = "Tahoma" size = "5"><strong>Relatório do mês passado.</strong></font><br><br>
        {texto_meio}
        <center><a href="/trigo-atual"><font face = "Tahoma" size = "4"><strong>Relatório deste mês.</strong></font></a><br><a href="/"><font face = "Tahoma" size = "3"><strong>Retorne ao menu</strong></font></a></center>"""
  return texto_final

@app.route("/algodao-atual")
def algodao_atual():
  data_hoje = datetime.now().strftime('%m%y')
  texto_meio = funcoes.texto_algodao(data_hoje)
  texto_final = f"""<font face = "Tahoma" size = "5"><strong>Relatório deste mês.</strong></font><br><br>
        {texto_meio}
        <center><a href="/algodao-anterior"><font face = "Tahoma" size = "4"><strong>Relatório do mês passado.</strong></font></a><br><a href="/"><font face = "Tahoma" size = "3"><strong>Retorne ao menu</strong></font></a></center>"""
  return texto_final
  
@app.route("/algodao-anterior")
def algodao_anterior():
  hoje = datetime.now()
  primeiro_dia = hoje.replace(day=1)
  data_anterior = primeiro_dia - timedelta(days=1)
  data_anterior = data_anterior.strftime("%m%y")
  texto_meio = funcoes.texto_algodao(data_anterior)
  texto_final = f"""<font face = "Tahoma" size = "5"><strong>Relatório do mês passado.</strong></font><br><br>
        {texto_meio}
        <center><a href="/algodao-atual"><font face = "Tahoma" size = "4"><strong>Relatório deste mês.</strong></font></a><br><a href="/"><font face = "Tahoma" size = "3"><strong>Retorne ao menu</strong></font></a></center>"""
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
  mostra = f"""<font face = "Tahoma" size = "5"><strong>Destaques do relatório de {mes}/{ano} sobre a safra {safra} de {produto}:</strong></font><br><br>{resultado}"""
  return mostra

if __name__ == '__main__':
    app.run(debug=True)
