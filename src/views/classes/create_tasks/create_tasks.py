from kivymd.uix.screen import MDScreen
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from ..alerts import Alert
from ....packages.API import Api
from ....packages.Numbers import validar_telefone


# Tela Criar Mensagens
class CreateTasks(MDScreen):

    # Adiciona um novo número
    def adicionar_numero(self, numero):
        if self.ids.tel1.select:
            self.ids.tel1.text = self.adicionar_numero_extensao(True,numero,self.ids.tel1) if (numero != '') else (
            self.adicionar_numero_extensao(False,numero,self.ids.tel1))
        elif self.ids.tel2.select:
            self.ids.tel2.text = self.adicionar_numero_extensao(True,numero,self.ids.tel2) if (numero != '') else (
            self.adicionar_numero_extensao(False,numero,self.ids.tel2))
        elif self.ids.tel3.select:
            self.ids.tel3.text = self.adicionar_numero_extensao(True,numero,self.ids.tel3) if (numero != '') else (
            self.adicionar_numero_extensao(False,numero,self.ids.tel3))
        elif self.ids.tel4.select:
            self.ids.tel4.text = self.adicionar_numero_extensao(True,numero,self.ids.tel4) if (numero != '') else (
            self.adicionar_numero_extensao(False,numero,self.ids.tel4))
        else:
            _numero = validar_telefone(numero) # Como o nome sugere valida o número digitado
            if _numero == False: Alert().campos_vazios('numeros')
            elif _numero == None: pass
            else:
                self.preencher_campo_seguinte(numero)
    
    # Modifica as propriedades do campo chip telefone passado dependendo da ordem passada
    def adicionar_numero_extensao(self, tipo : bool, numero : str, widget : any) -> str:
        if tipo:
            widget.select = False # Desmarca a seleção feita neste widget
            widget.numero = True # Identifica que o campo já está preenchido
            return '+244'+numero
        else:
            widget.select = False # Desmarca a seleção feita neste widget
            widget.numero = False # Identifica que o campo ainda está vazio
            return '+244 ??? ??? ???'
    
    # Preenche o proxímo campo chip com o número digitado | Caso todos os campos estejam preenchidos um alerta é disparado
    def preencher_campo_seguinte(self, numero):
        if self.existencia_do_numero(numero):
            if not self.ids.tel1.numero:
                self.ids.tel1.text = '+244'+numero
                self.ids.tel1.numero = True
            elif not self.ids.tel2.numero:
                self.ids.tel2.text = '+244'+numero
                self.ids.tel2.numero = True
            elif not self.ids.tel3.numero:
                self.ids.tel3.text = '+244'+numero
                self.ids.tel3.numero = True
            elif not self.ids.tel4.numero:
                self.ids.tel4.text = '+244'+numero
                self.ids.tel4.numero = True
            else: Alert().fire(text='Não é possível adicionar mais números.',type='failure')
        else: Alert().fire(text='Não é possível adicionar o mesmo número!',type='failure')
    
    # Marca o chip de telefone clicado, permitindo alterar o mesmo
    def marcar_chips(self, chip):
        if chip.select:
            chip.select = False
            self.ids.telefone.text = ''
        else:
            self.ids.tel1.select = False
            self.ids.tel2.select = False
            self.ids.tel3.select = False
            self.ids.tel4.select = False
            chip.select = True if chip.text != '+244 ??? ??? ???' else False
            self.ids.telefone.text = chip.text[4:] if chip.text != '+244 ??? ??? ???' else ''
    
    # Verfica se o número digitado é um número existente ou não
    def existencia_do_numero(self, numero) -> bool:
        return (
            self.ids.tel1.text != '+244'+numero
            and
            self.ids.tel2.text != '+244'+numero
            and
            self.ids.tel3.text != '+244'+numero
            and
            self.ids.tel4.text != '+244'+numero
        )
    
    # Retorna uma lista com todos os números inseridos | E um valor None caso não haja nenhum número
    def numeros_(self) -> list[str] | None:
        numero = []
        if(
            not self.ids.tel1.numero
            and
            not self.ids.tel2.numero
            and
            not self.ids.tel3.numero
            and
            not self.ids.tel4.numero
            ): return None
        else:
            for telefone in (self.ids.tel1, self.ids.tel2, self.ids.tel3, self.ids.tel4):
                if telefone.numero: numero.append(telefone.text)
            return numero
    
    # Envia as mensagens para o Servidor de Mensagens
    def enviar_mensagens(self, mensagem : str, data : str, hora : str):
        success = []
        numeros = self.numeros_()
        if numeros == None:
            Alert().fire(text='Não há nenhum destinatário!',type='failure')
        else:
            for numero in numeros:
                if numero != '':
                    if Api().enviar_mensagem(numero,mensagem,data,hora) == 200:
                        success.append(True)
                    else: pass
            if len(success) == len(numeros):
                Alert().mensagem()
                self.voltar_tela_mensagens()
            elif len(success) != len(numeros) and len(success) != 0:
                Alert().mensagem('def')
            elif len(success) <= 0: Alert().mensagem('n')

    # Retorna a data ou a hora atual para o front-end
    def info(self, info) -> str | int:
        from datetime import datetime
        if info == 'data':
            return str(datetime.now())[:10]
        elif info == 'hora':
            return str(datetime.now())[11:16]
    
    # Executa uma rotina quando a transição para uma outra tela é iniciada
    def on_pre_leave(self, *args):
        self.ids.telefone.txt = ''
        self.ids.mensagem.txt = ''
        self.ids.tel1.text = '+244 ??? ??? ???'
        self.ids.tel2.text = '+244 ??? ??? ???'
        self.ids.tel3.text = '+244 ??? ??? ???'
        self.ids.tel4.text = '+244 ??? ??? ???'
        self.ids.tel2.numero = False
        self.ids.tel1.numero = False
        self.ids.tel3.numero = False
        self.ids.tel4.numero = False
        self.ids.data.txt = self.info('data')
        self.ids.hora.txt = self.info('hora')
    
    # Executa uma rotina quando a transição para a tela de 'Criar Mensagens' é iniciada
    def on_pre_enter(self, *args):
        self.ids.telefone.txt = ''
        self.ids.mensagem.txt = ''
        self.ids.tel1.text = '+244 ??? ??? ???'
        self.ids.tel2.text = '+244 ??? ??? ???'
        self.ids.tel3.text = '+244 ??? ??? ???'
        self.ids.tel4.text = '+244 ??? ??? ???'
        self.ids.tel1.numero = False
        self.ids.tel2.numero = False
        self.ids.tel3.numero = False
        self.ids.tel4.numero = False
        self.ids.data.txt = self.info('data')
        self.ids.hora.txt = self.info('hora')
    
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

    # Abre o widget de Data
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
    
    # Abre o widget de Hora
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
    
    # Volta para a Tela de Mensagens
    def voltar_tela_mensagens(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'Tarefas'
