from kivymd_extensions.sweetalert import SweetAlert
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.uix.snackbar import Snackbar
from herojson import HeroJson

class Alert(SweetAlert):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def alteracoes(self, type : bool = True):
        if type: return self.fire(text='Alterações feitas com sucesso!',type='success')
        else: return self.fire(text='Não foi possível salvar as alterações.',type='failure')
    
    def campos_vazios(self, arg : str = 'dados'):
        return self.fire(text=f'Não é possível adicionar {arg} se estiver vazio.',type='failure')

    def valores_invalidos(self, type : str = 's', arg : str = 'dado'):
        if type == 's': return self.fire(text=f'O {arg} inserido está errado.',type='failure')
        else: return self.fire(text=f'Os {arg} inseridos estão errados.',type='failure')
    
    def mensagem(self, type = 's'):
        if type == 's': return self.fire(text='Mensagens enviadas com sucesso!',type='success')
        elif type == 'del': return self.fire(text='Mensagem apagada com sucesso!',type='success')
        elif type == 'delx': return self.fire(text='Não foi possivel apagar esta mensagem!',type='failure')
        elif type == 'def': return self.fire(text='Algumas mensagens não foram enviadas!',type='info')
        else: return self.fire(text='Não foi possível enviar a mensagem. Tente mais tarde!',type='failure')
    
    def conexao_de_internet(self, *args):
        if not HeroJson('src/temp/internet.json').key('status'):
            try: self.snack_yes.dismiss()
            except: pass
            self.snack_no = Snackbar(
                text="Sem conexão com a internet!",
                bg_color='#fea625',
                duration=.3,
                snackbar_x="10dp",
                snackbar_y="10dp",
                size_hint_x=(
                    Window.width - (dp(10) * 2)
                ) / Window.width
            ).open()
        else:
            if HeroJson('src/temp/internet.json').key('code') == 0:
                try: self.snack_no.dismiss()
                except: pass
                self.snack_yes = Snackbar(
                    text="Conexão Estabelecida",
                    bg_color='#fea625',
                    duration=.3,
                    snackbar_x="10dp",
                    snackbar_y="10dp",
                    size_hint_x=(
                        Window.width - (dp(10) * 2)
                    ) / Window.width
                ).open()
                HeroJson('src/temp/internet.json').update('code',1)