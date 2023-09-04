import requests as conn, json, os, datetime as dt
from herojson import HeroJson
from ...controllers import UserController


class Api():

    def __init__(self):
        self.url_usuario = 'http://localhost:2020'
        self.url_mensagem = 'http://localhost:2021'

    def conexao(self):
        try: return conn.get(url=F'{self.url_usuario}').status_code
        except: return 0

    def cadastrar(self, nome, senha, telefone):
        try:
            resposta = conn.post(
                url=F'{self.url_usuario}',
                json={
                    'nome' : nome,
                    'senha' : senha,
                    'telefone' : telefone,
                    'token': HeroJson("src/temp/tokens.json").key("token_usuario")
                },
                headers={'Authorization':F'Bearer {HeroJson("src/temp/tokens.json").key("token_usuario")}'}
            )
            return resposta.status_code, resposta.json()
        except:
            return 0, []
    
    def apagar_usuario(self, id : int):
        try:
            resposta = conn.delete(
                url = F'{self.url_usuario}/{id}',
                json = {
                    'token' : HeroJson("src/temp/tokens.json").key("token_usuario")
                },
                headers = {'Authorization':F'Bearer {HeroJson("src/temp/tokens.json").key("token_usuario")}'}
            )
            return resposta.status_code, resposta.json()
        except:
            return 0, []
    
    def atualizar_usuario(self, id, nome, senha, telefone):
        try:
            resposta = conn.put(
                url = F'{self.url_usuario}/{id}',
                json={
                    'nome' : nome,
                    'senha' : senha,
                    'telefone' : telefone,
                    'telefone_antigo' : UserController().pegar_usuario()[2],
                    'token': HeroJson("src/temp/tokens.json").key("token_usuario")
                },
                headers={'Authorization':F'Bearer {HeroJson("src/temp/tokens.json").key("token_usuario")}'}
            )
            if resposta.status_code == 401:
                self.pegar_chave_usuario()
                self.pegar_chave_mensagem()
                self.atualizar_usuario(id,nome,senha,telefone)
            return resposta.status_code, resposta.json()
        except:
            return 0, []
    
    def enviar_mensagem(self, destinatario, mensagem, data, hora):
        try:
            resposta = conn.post(
                url=F'{self.url_mensagem}/sms',
                json={
                    'usuario': UserController().pegar_usuario()[2],
                    'mensagem': mensagem,
                    'destinatario': destinatario,
                    'data': data,
                    'hora': hora
                },
                headers={'Authorization':F'Bearer {HeroJson("src/temp/tokens.json").key("token_usuario")}'}
            )
            if resposta.status_code == 401:
                self.pegar_chave_usuario()
                self.pegar_chave_mensagem()
                self.enviar_mensagem(destinatario,mensagem,data,hora)
            return resposta.status_code
        except: return 0

    def apagar_mensagem(self, id):
        try:
            resposta = conn.delete(
                url=F'{self.url_mensagem}/sms/{id}',
                headers={'Authorization':F'Bearer {HeroJson("src/temp/tokens.json").key("token_usuario")}'}
            )
            if resposta.status_code == 401:
                self.pegar_chave_usuario()
                self.pegar_chave_mensagem()
                self.enviar_mensagem(id)
            return resposta.status_code
        except: return 0
    
    def confirmar_cadastro(self, codigo):
        try:
            resposta = conn.post(
                url=F'{self.url_usuario}/confirm',
                json={'codigo':codigo},
                headers={'Authorization':F'Bearer {HeroJson("src/temp/tokens.json").key("token_usuario")}'}
            )
            if resposta.status_code == 401:
                self.pegar_chave_usuario()
                self.pegar_chave_mensagem()
                self.confirmar_cadastro(codigo)
            return resposta.status_code, resposta.json()
        except:
            return 0, []
    
    def reenviar_codigo(self, telefone):
        try:
            resposta = conn.post(
                url=F'{self.url_usuario}/re-codigo',
                json={
                    'telefone':telefone,
                    'token':HeroJson("src/temp/tokens.json").key("token_usuario")
                },
                headers={'Authorization':F'Bearer {HeroJson("src/temp/tokens.json").key("token_usuario")}'}
            )
            if resposta.status_code == 401:
                self.pegar_chave_usuario()
                self.pegar_chave_mensagem()
                self.reenviar_codigo(telefone)
            return resposta.status_code, resposta.json()
        except:
            return 0, []
    
    def pegar_mensagens(self, id):
        try:
            resposta = conn.get(
                url=F'{self.url_mensagem}/sms/{id}',
                headers={'Authorization':F'Bearer {HeroJson("src/temp/tokens.json").key("token_usuario")}'}
            )
            if resposta.status_code == 401:
                self.pegar_chave_usuario()
                self.pegar_chave_mensagem()
                self.pegar_mensagens(id)
            return resposta.status_code, resposta.json()
        except:
            return 0, []
    
    def atualizar_mensagem(self, id, destinatario, mensagem, data, hora):
        try:
            resposta = conn.put(
                url=F'{self.url_mensagem}/sms/{id}',
                json={
                    'usuario': UserController().pegar_usuario()[2],
                    'mensagem': mensagem,
                    'destinatario': destinatario,
                    'data': data,
                    'hora': hora
                },
                headers={'Authorization':F'Bearer {HeroJson("src/temp/tokens.json").key("token_usuario")}'}
            )
            if resposta.status_code == 401:
                self.pegar_chave_usuario()
                self.pegar_chave_mensagem()
                self.atualizar_mensagem(id,destinatario,mensagem,data,hora)
            return resposta.status_code
        except: return 0

    def pegar_chave_usuario(self) -> int:
        try:
            resposta = conn.get(
                url=F'{self.url_usuario}/login',
                json={'key':f"{os.getenv('key')}"}
            )
            if resposta.status_code == 200:
                HeroJson('src/temp/tokens.json').drop('token_usuario')
                HeroJson('src/temp/tokens.json').add('token_usuario',resposta.json()['token'])
                HeroJson('src/temp/tokens.json').update('tempo',str(dt.datetime.now()))
                return 200
            else:
                return 405
        except: return 0
    
    def pegar_chave_mensagem(self) -> int:
        try:
            resposta = conn.get(
                url=F'{self.url_mensagem}/token',
                json={'key':f"{os.getenv('key')}"}
            )
            if resposta.status_code == 200:
                HeroJson('src/temp/tokens.json').drop('token_mensagem')
                HeroJson('src/temp/tokens.json').add('token_mensagem',resposta.json()['token'])
                return 200
            else:
                return 405
        except: return 0


#END