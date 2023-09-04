from kivymd.uix.screen import MDScreen
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from ..alerts import Alert
from ....packages.Numbers import validar_telefone
from ....packages.API import Api
from herojson import HeroJson


# Tela de Editar Mensagens
class EditTasks(MDScreen):

    # Insere os dados nos campos da tela
    def inserir_dados(self, data : str, hora : str, mensagem : str, destinatario : list[str]):
        self.ids.data.text = str(data)
        self.ids.hora.text = str(hora)
        self.ids.mensagem.text = str(mensagem)
        self.ids.tel1.text = destinatario

    # Marca o chip de telefone clicado, permitindo alterar o mesmo
    def marcar_chips(self, chip):
        if chip.select:
            chip.select = False
            self.ids.telefone.text = ''
        else:
            chip.select = True
            self.ids.telefone.text = chip.text[4:]

    # Pega os dados da mensagem selecionada para a edição
    def pegar_organizar_dados(self):
        self.id_mensagem = HeroJson('src/temp/ids.json').key('id') # Pega o id da mensagem no arquivo json
        for mensagem in HeroJson('src/temp/mensagens.json').key('mensagens'): # Percorre as mensagens resgatadas do servidor d'Mensagens
            if str(mensagem['id']) == self.id_mensagem:
                self.data = mensagem['data']
                self.hora = mensagem['hora']
                self.mensagem = mensagem['mensagem']
                self.destinatario = mensagem['destinatario']
        self.inserir_dados(self.data,self.hora,self.mensagem,self.destinatario)

    # Adiciona um número de telefone ao proxímo campo vazio
    def adicionar_numero(self, numero):
        # Responsábiliza-se por garantir se é ou não uma edição de um número chip
        _numero = validar_telefone(numero)
        if _numero:
            if self.ids.tel1.select:
                self.ids.tel1.text = '+244'+numero if numero != '' and self.ids.tel1.text != numero else '+244 ??? ??? ???'
                self.ids.tel1.select = False # Retira a seleção do chip número
                self.ids.telefone.text = ''
            else:
                Alert().fire(text='Selecione a caixa com o numero para atualizar',type='failure')
        elif _numero is None: pass
        else:
            Alert().campos_vazios(arg='número')

    # Envia as informações atualizadas para a base o serviço de Mensagem
    def salvar_alteracoes(self, numero : str, mensagem : str, data : str, hora : str):
        success = False
        # Envia uma mensagem para cada um dos números inseridos
        if Api().atualizar_mensagem(self.id_mensagem,numero,mensagem,data,hora) == 200:
            success = True
        else: success = False
        if success:
            Alert().alteracoes()
            self.voltar_tela_mensagens()
        else: Alert().alteracoes(False)
    
    def alerta_apagar_mensagem(self):
        if not self.dialogo:
            self.dialogo = MDDialog(
                text = "Deletar esta mensagem, significa apagar ela permanentemente.\nDeseja continuar?",
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
                        on_release = lambda x: self.apagar_mensagem()
                    ),
                ],
            )
        self.dialogo.open()

    # Envia uma solicitação para deletar a mensagem da base de dados | Um alerta é dado com base a resposta do Servidor
    def apagar_mensagem(self):
        self.dialogo.dismiss()
        if Api().apagar_mensagem(self.id_mensagem) == 200:
            Alert().mensagem('del')
            self.voltar_tela_mensagens()
        else:
            Alert().fire(text='Falha na comunicação com o servidor!',type='failure')

    # Começa uma tarefa assim que a transição para essa tela é iniciada
    def on_pre_enter(self, *args):
        self.dialogo = None
        self.pegar_organizar_dados()

    # Retorna informações de data e hora para o front-end
    def info(self, info) -> str | int:
        from datetime import datetime
        if info == 'data':
            return str(datetime.now())[:10]
        elif info == 'hora':
            return str(datetime.now())[11:16]

    # Insere o data selecionada na caixa de data para a visualização do usuário
    def on_save_date(self, instance, value, date_range):
        self.ids.data.text = f'{value}'

    def on_cancel_date(self, instance, value):
        pass

    # Faz o mesmo que o on_save_data sendo que a hora é o dado visualizado
    def on_save_time(self, instance, value):
        self.ids.hora.text = str(value)[:5]

    def on_cancel_time(self, instance, value):
        pass

    # Abre o widget de data
    def abrir_data(self):
        date_dialog = MDDatePicker(
            title_input = 'Definir Data',
            title = 'Definir Data',
            md_bg_color = '#fea625',
            text_color = '#fea625',
            text_toolbar_color = '#ffffff'
        )
        date_dialog.bind(on_save=self.on_save_date, on_cancel=self.on_cancel_date)
        date_dialog.open()

    # Abre o widget de hora
    def abrir_hora(self):
        date_dialog = MDTimePicker(
            title_input = 'Definir Hora',
            title = 'Definir Hora',
            md_bg_color = '#fea625',
            text_color = '#fea625',
            text_button_color = '#fea625',
            text_toolbar_color = '#fea625'
        )
        date_dialog.bind(on_save=self.on_save_time, on_cancel=self.on_cancel_time)
        date_dialog.open()

    # Retorna para a tela de Tarefas
    def voltar_tela_mensagens(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'Tarefas'

