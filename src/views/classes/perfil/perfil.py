from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from ....models.user import Users
from ....controllers import UserController
from ....packages.Numbers import validar_telefone
from ....packages.API import Api
from ..alerts import Alert

class Perfil(MDScreen):
    
    def tela_tarefas(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'Tarefas'
    
    def alerta_apagar_conta(self):
        if not self.dialogo:
            self.dialogo = MDDialog(
                text = "Deletar sua conta, significa apagar ela permanentemente.\nDeseja continuar?",
                md_bg_color = '#ffffff',
                radius = [20, 7, 20, 7],
                buttons = [
                    MDFlatButton(
                        text = "Cancelar",
                        theme_text_color = "Custom",
                        text_color = "#ffffff",
                        md_bg_color = '#fea625',
                        on_release = lambda x: self.dialogo.dismiss()
                    ),
                    MDFlatButton(
                        text= " Continuar",
                        theme_text_color = "Custom",
                        text_color = "#ffffff",
                        md_bg_color = '#fea625',
                        on_release = lambda x: self.apagar_conta()
                    ),
                ],
            )
        self.dialogo.open()
    
    def apagar_conta(self):
        codigo ,resposta = Api().apagar_usuario(UserController().pegar_usuario()[0])
        if codigo == 200:
            if UserController().apagar_usuario():
                Alert().fire(text='Conta apagada com sucesso!')
                self.dialogo.dismiss()
                self.manager.transition.direction = 'right'
                self.manager.current = 'default'
        else:
            Alert().fire(text='Não foi possível apagar sua conta. Tente mais tarde!',type='failure')
    
    def introduzir_informacoes(self):
        self.id_usuario = UserController().pegar_usuario()[0]
        self.ids.nome.text = UserController().pegar_usuario()[1]
        self.ids.telefone.text = UserController().pegar_usuario()[2]
        self.ids.senha.text = UserController().pegar_usuario()[3]
    
    def on_pre_enter(self, *args):
        self.dialogo = None
        self.introduzir_informacoes()
    
    def campos_vazios(self, campos = []) -> bool:
        for campo in campos:
            if campo == '': return False
        return True
    
    def salvar_alteracoes(self, nome, senha, telefone):
        if self.campos_vazios((nome,senha,telefone)):
            if validar_telefone(telefone):
                code, resposta = Api().atualizar_usuario(self.id_usuario,nome,senha,telefone)
                print(resposta)
                if code == 200:
                    dados = resposta['usuario']
                    UserController().atualizar_usuario(Users(
                        UserController().pegar_usuario()[0],
                        dados['nome'],
                        dados['telefone'],
                        dados['senha']
                    ))
                    Alert().alteracoes()
                    self.introduzir_informacoes()
                elif code == 404:
                    Alert().fire(
                        text='Não está sendo possível atualizar os seus dados agora. Tente mais tarde!',
                        type='failure'
                    )
                else:
                    Alert().fire(
                        text='Há um problema na comunicação com o servidor. Tente mais tarde!',
                        type='failure'
                    )
            else: pass
        else: Alert().campos_vazios()