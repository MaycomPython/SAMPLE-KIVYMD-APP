# main.py
from kivymd.app import MDApp
from kivy.lang import Builder

# Opcional: Para simular o tamanho de uma tela de celular no desktop
from kivy.core.window import Window
Window.size = (320, 600)

# String multi-linha contendo o layout KV com a correção final
LOGIN_SCREEN_KV = '''
MDScreen:

    MDFloatLayout:
        
        MDCard:
            id: login_card
            size_hint: .8, .6
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            elevation: 10
            padding: "25dp"
            spacing: "25dp"
            orientation: 'vertical'

            MDLabel:
                text: "Login"
                halign: "center"
                size_hint_y: None
                height: self.texture_size[1]

            MDTextField:
                id: username_field
                hint_text: "Usuário"
                helper_text: "Digite seu nome de usuário"
                helper_text_mode: "on_focus"
                icon_right: "account"
                # --- MUDANÇA AQUI ---
                # 'primary_color' foi substituído por 'primaryColor'
                icon_right_color: app.theme_cls.primaryColor
                pos_hint: {"center_x": 0.5}
                size_hint_x: None
                width: "220dp"

            MDTextField:
                id: password_field
                hint_text: "Senha"
                helper_text: "Digite sua senha"
                helper_text_mode: "on_focus"
                icon_right: "eye-off"
                # --- MUDANÇA AQUI ---
                # 'primary_color' foi substituído por 'primaryColor'
                icon_right_color: app.theme_cls.primaryColor
                pos_hint: {"center_x": 0.5}
                size_hint_x: None
                width: "220dp"
                password: True

            MDButton:
                style: "elevated"
                text: "ENTRAR"
                pos_hint: {"center_x": 0.5}
                on_release: app.login()
            
            MDLabel:
                id: login_status
                text: ""
                halign: "center"
'''


class LoginApp(MDApp):

    def build(self):
        # A definição do tema no código Python continua usando snake_case
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(LOGIN_SCREEN_KV)

    def login(self):
        username = self.root.ids.username_field.text
        password = self.root.ids.password_field.text
        
        if username == "admin" and password == "1234":
            print(f"Login bem-sucedido com o usuário: {username}")
            self.root.ids.login_status.text = f"Bem-vindo, {username}!"
            self.root.ids.login_status.theme_text_color = "Success"
        else:
            print("Credenciais inválidas!")
            self.root.ids.login_status.text = "Usuário ou senha inválidos!"
            self.root.ids.login_status.theme_text_color = "Error"


if __name__ == '__main__':
    LoginApp().run()
