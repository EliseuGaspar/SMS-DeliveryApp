from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.spinner import MDSpinner
from kivy.metrics import dp

class Load():

    def criar_loadscreen(self):
        loadscreen = MDRaisedButton(
            size_hint = (1, 1),
            md_bg_color = '#ffffff',
            ripple_color = '#ffffff',
            _no_ripple_effect = False
        )

        float_layout = FloatLayout()

        float_layout.add_widget(
            MDSpinner(
                size_hint = (None, None),
                size = (dp(46), dp(46)),
                pos_hint = {'center_x': .5, 'center_y': .55},
                active = True,
                color = '#fea625'
            )
        )

        float_layout.add_widget(
            MDLabel(
                text = 'Efectuando a Operação...',
                color = '#fea625',
                halign = 'center',
                font_size = '15dp',
                pos_hint = {'center_x': .5,'center_y': .42}
            )
        )

        loadscreen.add_widget(float_layout)

        return loadscreen


