from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from herojson import HeroJson

from ..create_tasks import CreateTasks
from ..login import  Login
from ..perfil import Perfil
from ..signup import SignUp
from ..tasks import Tasks
from ..contacts import Contacts
from ..start import Default
from ..confirmation import Confirmation
from ..edittasks import EditTasks
from ....controllers import UserController
from ....packages.API import Api
from ....packages.calculador_tempo import calcular
from ....temp.temp import limpar_temp

from os import system


class Delivery(MDApp):
    def carregar_classes(self, init_type : str = 'Cadastro'):
        self.manager = MDScreenManager()
        if init_type == 'Cadastro':
            self.manager.add_widget(Default())
            self.manager.add_widget(Confirmation())
            self.manager.add_widget(Login())
            self.manager.add_widget(SignUp())
            self.manager.add_widget(Tasks())
            self.manager.add_widget(EditTasks())
            self.manager.add_widget(CreateTasks())
            self.manager.add_widget(Perfil())
            self.manager.add_widget(Contacts())
        else:
            self.manager.add_widget(Tasks())
            self.manager.add_widget(Perfil())
            self.manager.add_widget(CreateTasks())
            self.manager.add_widget(EditTasks())
            self.manager.add_widget(Contacts())
            self.manager.add_widget(Default())
            self.manager.add_widget(Confirmation())
            self.manager.add_widget(Login())
            self.manager.add_widget(SignUp())

    def carregar_telas(self):
        self.load_all_kv_files('src/views/kvs')
    
    def config_inicio(self):
        limpar_temp()
        try:
            dados = not (UserController().pegar_usuario()[1] == None)
        except:
            dados = not (UserController().pegar_usuario() == [])
        if calcular(HeroJson('src/temp/tokens.json').key('tempo')) >= 60:
            Api().pegar_chave_usuario()
            Api().pegar_chave_mensagem()
        if not dados:
            self.carregar_classes()
        else:
            self.carregar_classes('other')

    def configuracoes_padroes(self):
        HeroJson('src/temp/confirmation_time.json').update('minutos','05')
        HeroJson('src/temp/confirmation_time.json').update('segundos','00')
    
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = 'Orange'
        self.carregar_telas()
        self.config_inicio()
        self.configuracoes_padroes()

        return self.manager 
