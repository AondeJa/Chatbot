
# -*- coding: utf-8 -

import random
from flask import Flask, request
from pymessenger.bot import Bot
from pymessenger import Button
from pymessenger.user_profile import UserProfileApi
from persist import insert
from session import Session

app = Flask(__name__)
ACCESS_TOKEN = 'EAAEJZBM7qpfcBAOyZC4OZCHAqLCdn0av4FbDlKTywy4sgiqwH6O0pASb8Lhyfmwy8yhtsMhPOZB3E4HZCXrS2RUexmCbpW3peT6VDYd8VMVV3pazZAy5cZBNZC7G7OplfaPVnM9IRVfcZBhXKccXrNEcOhA8BmjDz0d0ZA2IUGZBdqkeRgjZCkzFUqZB0'
VERIFY_TOKEN = 'mcjJsvg6S4'
bot = Bot(ACCESS_TOKEN)
user = UserProfileApi(ACCESS_TOKEN)
sessao = []
resposta = ''
index = 0 

@app.route("/api", methods=['GET', 'POST'])
def receive_message():
    global sessao
    global index
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:
        verifica()
        print(index)
        if sessao[index].status == 1: 
            first_int(sessao[index].recipient_id)
        elif sessao[index].status == 2:
            second_int()
        elif sessao[index].status == 3:
            ter_int()
        elif sessao[index].status == 4:
            quar_int()
        elif sessao[index].status == 5:
            quin_int()
        elif sessao[index].status == 6:
        	sex_int()
        elif sessao[index].status == 7:
            set_int()
        if  sessao[index].status > 7:
            del(sessao[index])
        

        

    return "Message Processed"


def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


def first_int(recipient_id):
            button_message(recipient_id)
            sessao[index].incremento()

def second_int():
    global sessao
    global resposta
    global index
    output = request.get_json()
    for event in output['entry']:
      messaging = event['messaging']
      for message in messaging:
        if message.get('postback'):
            recipient_id = message['sender']['id']
            resposta = message['postback']['payload']
            if resposta == "Sim":
               send_message(recipient_id, 'Muito bem, informe a placa do veículo.')
               sessao[index].incremento()
            elif resposta == "Não":
                send_message(recipient_id,'Infelizmente só estamos trabalhando com informação de veículos oficiais no momento!')            
                del(sessao[index])

def ter_int():
    global sessao
    global index
    output = request.get_json()
    for event in output['entry']:
      messaging = event['messaging']
      for message in messaging:
        if message.get('message'):
            recipient_id = message['sender']['id']  
            sessao[index].placa_carro = message['message']['text']
            send_message(recipient_id,'Ok! Informe a qual órgão público pertence este veículo! ')
            sessao[index].incremento()



def quar_int():
    global sessao
    global index
    output = request.get_json()
    for event in output['entry']:
      messaging = event['messaging']
      for message in messaging:
        if message.get('message'):
            recipient_id = message['sender']['id']  
            sessao[index].nome_orgao = message['message']['text']
            send_message(recipient_id,'Ok! Anexe a imagem da ocorrência! ')
            sessao[index].incremento()


def quin_int():
    global sessao
    global index
    output = request.get_json()
    for event in output['entry']:
      messaging = event['messaging']
      for message in messaging:
        if message.get('message'):
            if message['message'].get('attachments'):
                attachments = message['message']['attachments']
                recipient_id = message['sender']['id']
                sessao[index].url_imagem = attachments[0]['payload']['url']
                require_location(recipient_id,'Informe a localização da ocorrência')
                sessao[index].incremento()


def sex_int():
    global sessao
    global index
    output = request.get_json()
    for event in output['entry']:
      messaging = event['messaging']
      for message in messaging:
        if message.get('message'):
            if message['message'].get('attachments'):
                attachments = message['message']['attachments']
                recipient_id = message['sender']['id']
                coordinates = attachments[0]['payload']['coordinates']
                sessao[index].lat = coordinates['lat']
                sessao[index].lon = coordinates['long']
                send_message(recipient_id,'Agora faça uma descrição breve do que você presenciou')
                sessao[index].incremento()


def set_int():
    global sessao
    global index
    output = request.get_json()
    for event in output['entry']:
      messaging = event['messaging']
      for message in messaging:
        if message.get('message'):
            recipient_id = message['sender']['id']  
            sessao[index].descricao = message['message']['text']
            sessao[index].inserir()
            send_message(recipient_id,'Obrigado {}, pelo seu apoio!!'.format(sessao[index].nome))
            sessao[index].incremento()

def verifica():
    global sessao
    output = request.get_json()
    for event in output['entry']:
      messaging = event['messaging']
      for message in messaging:
        if message.get('message'):
            recipient_id = message['sender']['id']
            fields = ['id', 'first_name']
            if existe(recipient_id) == 0:
                user_profile = user.get(recipient_id, fields=fields)
                temp = Session(user_profile['id'],user_profile['first_name'],recipient_id)
                sessao.append(temp)  
            index = get_index(recipient_id)
    return 

def existe(id):
    global sessao
    for ses in sessao:
        if id == ses.id:
            return 1
    return 0

def get_index(id):
    global sessao
    global index
    cont = 0
    for ses in sessao:
        if ses.id == id:
            index = cont
        cont += 1

'''Funções de comunicação do bot.'''
def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return "success"
def require_location(recipient_id, response):
    bot.send_location_message(recipient_id, response)
    return "success"

def button_message(recipient_id):
    global sessao
    global index
    buttons = []
    button = Button(title='Sim', type='postback', payload='Sim')
    buttons.append(button)
    button = Button(title='Não', type='postback', payload='Não')
    buttons.append(button)
    text = 'Olá {}, você gostaria de reportar o uso indevido de um veículo público? Para isto você precisará informar a placa do veículo e ter uma foto do flagrante.'.format(sessao[index].nome)
    bot.send_button_message(recipient_id, text, buttons)   


if __name__ == "__main__":
     app.run()
