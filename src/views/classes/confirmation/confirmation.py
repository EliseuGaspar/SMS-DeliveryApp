from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from herojson import HeroJson
from ....packages.API import Api
from ....models.user import Users
from ....controllers import UserController
from ..alerts import Alert

class Confirmation(MDScreen):

    def on_enter(self, *args):
        self.contador = Clock.schedule_interval(self.ContadorDecrescente, 1)

    def ContadorDecrescente(self, *args):
        cancel = False
        minutos = HeroJson('src/temp/confirmation_time.json').key('minutos')
        segundos = HeroJson('src/temp/confirmation_time.json').key('segundos')
        if segundos == '00':
            if minutos != '00':
                segundos = '59'
                minutos = F"0{int(minutos[1:2])-1}"
            else: cancel = True
        else:
            segundos = int(segundos) - 1 if int(segundos) >= 11 else F"0{int(segundos[1:2])-1}" if segundos != '10' else F"0{int(segundos) - 1}"
        HeroJson('src/temp/confirmation_time.json').update('minutos',minutos)
        HeroJson('src/temp/confirmation_time.json').update('segundos',str(segundos))
        self.ids.contador.text = f'O código expira em: {minutos}:{segundos}' if not cancel else 'O tempo de confirmação expirou!'

    def confirmar_conta(self):
        if "" != self.ids.c1.text and "" != self.ids.c2.text and "" != self.ids.c3.text and "" != self.ids.c4.text:
            code , resposta = Api().confirmar_cadastro(F'{self.ids.c1.text}{self.ids.c2.text}{self.ids.c3.text}{self.ids.c4.text}')
            if code == 200:
                dados = resposta['usuario']
                UserController().cadastrar_usuario(Users(
                        dados['id'],
                        dados['nome'],
                        dados['telefone'],
                        dados['senha']
                    ))
                self.manager.transition.direction = 'left'
                self.manager.current = 'Tarefas'
            elif code == 410:
                Alert().fire(
                    text=F'Este código({self.ids.c1.text}{self.ids.c2.text}{self.ids.c3.text}{self.ids.c4.text}) já expirou! Cadastre-se novamente.',
                    type='failure'
                )
            else:
                Alert().fire(
                    text='Há um problema na comunicação com o servidor. Tente mais tarde!',
                    type='failure'
                )
        else:
            Alert().fire(
                text='Verifique se há algum campo vazio!',
                type='failure'
            )

    def pedir_novo_envio(self):
        minutos = HeroJson('src/temp/confirmation_time.json').key('minutos')
        segundos = HeroJson('src/temp/confirmation_time.json').key('segundos')
        if minutos != '00' and segundos != '00':
            codigo, resposta = Api().reenviar_codigo(HeroJson('src/temp/dados_usuario.json').key('telefone'))
            if codigo == 200:
                HeroJson('src/temp/confirmation_time.json').update('minutos',resposta['tempo'][:2])
                HeroJson('src/temp/confirmation_time.json').update('segundos',resposta['tempo'][3:5])
            elif codigo == 404:
                Alert().fire(text='Não foi possível enviar um novo codigo, realize um novo cadastro',type='failure')
            elif codigo == 500:
                Alert().fire(text='Não foi possível manter a comunicação com o servidor.',type='failure')
            else:
                Alert().fire(text='Falha na comunicação. Verifique a sua conexão a internet.',type='failure')
        else: Alert().fire(text='O tempo de confirmação expirou, realize um novo cadastro.',type='failure')

    def fechar_app(self):
        from os import _exit
        _exit(1)
    
    def proxima_tela(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'Tarefas'


