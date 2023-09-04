from kivymd.uix.screen import MDScreen
from kivymd.uix.list import (
    ThreeLineAvatarIconListItem,
    TwoLineIconListItem,
    IconLeftWidget
)
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from herojson import HeroJson

from ....controllers import UserController
from ....packages.API import Api



class Tasks(MDScreen):
    
    def on_pre_enter(self, *args):
        self.herojson = HeroJson('src/temp/ids.json')
        codigo , resposta = Api().pegar_mensagens(UserController().pegar_usuario()[2])
        if codigo == 200:
            self.mensagens = resposta['sms']
            HeroJson('src/temp/mensagens.json').update('mensagens',self.mensagens)
            self.limpar_tela()
            self.preencher_lista()
        elif codigo == 404:
            self.limpar_tela()
            self.sem_mensagens()
        else:
            self.limpar_tela()
            self.estado_da_net()
    
    def limpar_tela(self):
        try:
            self.ids.body.remove_widget(self.sem_mensagem_icon)
            self.ids.body.remove_widget(self.sem_mensagem_label)
        except: pass
        try:
            self.ids.body.remove_widget(self.estado_da_net_icon)
            self.ids.body.remove_widget(self.estado_da_net_label)
        except: pass
        
        self.ids.box.clear_widgets()
    
    def sem_mensagens(self):
        self.sem_mensagem_icon = MDIconButton(
                icon = 'comment-off',
                icon_size = "70sp",
                pos_hint = {'center_y':.55,'center_x':.5},
                ripple_color = '#ffffff',
                theme_icon_color = "Custom",
                icon_color = '#fea62575',
                _no_ripple_effect = True,
                on_release= lambda x: self.refresh()
            )
        self.sem_mensagem_label = MDLabel(
                text = 'Não tens nenhuma mansagem agendada.',
                text_size = "30sp",
                theme_text_color = 'Custom',
                text_color = '#fea625',
                valign = 'center',
                halign = 'center',
                pos_hint = {'center_y':.4,'center_x':.5},
                size_hint_x = .8
            )
        self.ids.body.add_widget(self.sem_mensagem_icon)
        self.ids.body.add_widget(self.sem_mensagem_label)
    
    def refresh(self):
        self.on_pre_enter()
    
    def preencher_lista(self):
        self.limpar_tela()
        self.ids.box.add_widget(TwoLineIconListItem(divider_color = (1,1,1,0),ripple_duration_in_fast = .1,bg_color = '#ffffff'))
        for mensagem in self.mensagens:
            self.ids.box.add_widget(
                ThreeLineAvatarIconListItem(
                    IconLeftWidget(
                        icon = "chat",
                        theme_icon_color = 'Custom',
                        icon_color = '#ffffff',
                        font_style = 'Body2'
                        ),
                    text=f"{mensagem['mensagem']}",
                    secondary_text = f"Para: {mensagem['destinatario']}",
                    tertiary_text = f"Data: {mensagem['data']} - {mensagem['hora']}",
                    font_style = 'Body2',
                    secondary_font_style = 'Caption',
                    tertiary_font_style = 'Caption',
                    divider_color = (1,1,1,0),
                    ripple_duration_in_fast = .1,
                    on_release = lambda x: self.tela_editar_mensagem(x),
                    bg_color = '#fea625',
                    theme_text_color = 'Custom',
                    secondary_theme_text_color = 'Custom',
                    tertiary_theme_text_color = 'Custom',
                    secondary_text_color = '#ffffff',
                    tertiary_text_color = '#ffffff',
                    text_color = '#ffffff',
                    id = str(mensagem['id'])
                )
            )
        self.ids.box.add_widget(TwoLineIconListItem(divider_color = (1,1,1,0),ripple_duration_in_fast = .1,bg_color = '#ffffff'))

    def tela_editar_mensagem(self, dados):
        if not self.herojson.add('id',f'{dados.id}'):
            self.herojson.update('id',f'{dados.id}')
        self.manager.transition.direction = 'left'
        self.manager.current = 'editar_tarefas'

    def estado_da_net(self):
        self.estado_da_net_icon = MDIconButton(
                icon = 'access-point-network-off',
                icon_size = "70sp",
                pos_hint = {'center_y':.55,'center_x':.5},
                ripple_color = '#ffffff',
                theme_icon_color = "Custom",
                icon_color = '#fea62575',
                _no_ripple_effect = True,
                on_release= lambda x: self.refresh()
            )
        self.estado_da_net_label = MDLabel(
                text = 'Sem conexão com a internet! \n Clique no ícone para refrescar a página.',
                text_size = "30sp",
                theme_text_color = 'Custom',
                text_color = '#fea625',
                valign = 'center',
                halign = 'center',
                pos_hint = {'center_y':.4,'center_x':.5},
                size_hint_x = .8
            )
        self.ids.body.add_widget(self.estado_da_net_icon)
        self.ids.body.add_widget(self.estado_da_net_label)

    def editar_mensagem(self, item):
        pass

    def tela_criar_mensagem(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'criar_tarefas'

    def tela_perfil(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'perfil'

    def tela_contactos(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'contactos'
    
    def fechar_app(self):
        from os import _exit
        _exit(1)

    def abrir_site(self):
        from webbrowser import open
        open('http://localhost:2022')


