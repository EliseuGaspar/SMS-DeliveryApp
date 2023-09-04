from kivymd.uix.screen import MDScreen


class Default(MDScreen):
    
    def proxima_tela(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'Login'
    
    def fechar_app(self):
        import os
        os._exit(1)