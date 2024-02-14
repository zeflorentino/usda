import gspread
import json
import requests
import os
import openai

from datetime import datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials

import funcoes

palavra_secreta = os.environ["PALAVRA_SECRETA"]

GOOGLE_SHEETS_CREDENTIALS = os.environ['GOOGLE_SHEETS_CREDENTIALS']
with open('credenciais.json', mode = "w") as arquivo:
 arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name('credenciais.json')
 
api = gspread.authorize(conta)
planilha = api.open_by_key("16sUMF5oixWfKfRAWzcvy_brPqgUanVwiHz_UGk72rQw")
registros = planilha.worksheet("registros")
cadastrados = planilha.worksheet("cadastrados")
ultimo = int(registros.get("A1")[0][0])
token = os.environ["TELEGRAM_API_KEY"]

def envia_boletim():
 resumo = funcoes.texto_cabeca('0323')
 nova_resposta = f'&#127805 <strong>NOVO RELATÓRIO:</strong> {resumo} \n\n<a href="https://site-teste-zeflorentino.onrender.com/"><strong>Clique para ler todos os destaques.</strong></a>' 
 lista_cadastros = cadastrados.get_all_values()

 for x in lista_cadastros:
  chat_id_resposta = x[3]
  nova_mensagem = {"chat_id": chat_id_resposta, "text": nova_resposta, "parse_mode" : 'HTML'}
  requests.post(f"https://api.telegram.org./bot{token}/sendMessage", data=nova_mensagem)
 

def processa_update(dados):
 update = dados
 update_id = update["update_id"]
 first_name = update["message"]["from"]["first_name"]
 message = update["message"]["text"]
 chat_id = update["message"]["chat"]["id"]
 data_hora = datetime.fromtimestamp(update["message"]["date"])
 if "username" in update["message"]["from"]:
  username = update["message"]["from"]["username"]
 else:
  username = '[não definido]'
 if message == "/start":
  texto_resposta = f"Olá, <strong>{first_name}</strong>! Seja bem-vinda(o). \n\nQuer receber mensalmente as projeções do <strong>Departamento de Agricultura dos Estados Unidos</strong> para a safra de milho? \n\nSe sim, envie '1'. \n\nSe quer parar de receber, envie '2'."
 elif message == "1":
  ja_cadastrado = cadastrados.findall(str(chat_id))
  if len(ja_cadastrado) >= 1:
   texto_resposta = f"<strong>{first_name}</strong>, você já está cadastrado!"
  else: 
   cadastrados.append_row([str(data_hora), username, first_name, chat_id])
   texto_resposta = f"{first_name}, você foi cadastrado com sucesso!"
 elif message == "2":
  texto_resposta = f"Ok, <strong>{first_name}</strong>, retiramos você da nossa lista. Até breve!"
  lista_cadastros = cadastrados.get_all_values()
  for x in lista_cadastros:
   if x[3] == str(chat_id):
    lista_cadastros.remove(x)
  cadastrados.clear()
  cadastrados.update("A1", lista_cadastros)
 elif message == palavra_secreta:
  texto_resposta = f'<strong>{first_name}</strong>, caso não queira mais receber os alertas, envie "2".'
  envia_boletim()
 else:
  texto_resposta = f"Não entendi, <strong>{first_name}</strong>!\n\nCaso queira receber mensalmente as projeções do <strong>Departamento de Agricultura dos Estados Unidos</strong>, envie '1'.\n\nSe quer parar de receber, envie '2'."
 nova_mensagem = {"chat_id": chat_id, "text": texto_resposta, "parse_mode" : 'HTML'}
 requests.post(f"https://api.telegram.org./bot{token}/sendMessage", data=nova_mensagem)  

 update_id = update["update_id"]
 registros.update("A1", update_id)
