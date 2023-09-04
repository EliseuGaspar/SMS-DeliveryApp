from kivymd.uix.screen import MDScreen
from herojson import HeroJson
from ..alerts import Alert, SweetAlert
from ....packages.Numbers import validar_telefone
from ..loads import Load
from ....packages.API import Api

class SignUp(MDScreen):

    def on_pre_enter(self, *args):
        self.load_event_instance = None
        self.status = None
    
    def cadastrar_usuario(self, telefone, senha, nome, terms):
        if telefone == '' or senha == '' or nome == '': Alert().campos_vazios()
        elif not validar_telefone(telefone): pass
        elif not terms: SweetAlert().fire(
            text='Apenas os que concordam com os termos são registrados',
            type='failure'
        )
        else:
            self.load_widget = Load().criar_loadscreen()
            self.add_widget(self.load_widget)
            codigo , resposta = Api().cadastrar(nome,senha,telefone)
            if codigo == 200:
                HeroJson('src/temp/confirmation_time.json').update('minutos',resposta['tempo'][:2])
                HeroJson('src/temp/confirmation_time.json').update('segundos',resposta['tempo'][3:5])
                HeroJson('src/temp/dados_usuario.json').update('telefone',self.ids.telefone.text)
                self.manager.transition.direction = 'left'
                self.manager.current = 'Confirmation'
            else:
                self.remove_widget(self.load_widget)
    
    def on_pre_leave(self, *args):
        try: self.remove_widget(self.load_widget)
        except: pass
    
    def voltar_tela(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'Login'
    
    def mudar_estado_checkbox(self):
        if not self.ids.check.active:
            self.ids.check.active = True
        else:
            self.ids.check.active = False