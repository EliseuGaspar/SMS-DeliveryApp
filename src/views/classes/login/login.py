from kivymd.uix.screen import MDScreen

from ..alerts import Alert
from ....controllers import UserController

class Login(MDScreen):
    
    def proxima_tela(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'Tarefas'
    
    def voltar_tela(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'default'
    
    def _tela_criar_conta(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'Cadastrar'
    
    def login(self, telefone, senha):
        dados = UserController().pegar_usuario()
        try:
            if dados[2] == telefone and dados[3] == senha:
                self.proxima_tela()
            else:
                Alert().fire(
                    text='Erro ao logar,verifique se os dados inseridos estão corretos.',
                    type='failure'
                )
        except:
            Alert().fire(
                text='Estes dados não existem. Faça um cadastro!',
                type='failure'
            )