from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.metrics import dp

# Import dos componentes de Dialog
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
)

# --- CORREÇÃO AQUI ---
# Import dos componentes de Button que serão criados no código Python
from kivymd.uix.button import MDButton, MDButtonText


KV = '''
MDScreen:
    md_bg_color: self.theme_cls.backgroundColor

    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        adaptive_height: True
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        size_hint_x: 0.9

        MDLabel:
            text: 'Bem-vindo'
            theme_text_color: 'Primary'
            halign: 'center'
            font_size: "26sp"
            bold: True
            adaptive_height: True

        MDLabel:
            text: 'Faça login para continuar'
            theme_text_color: 'Secondary'
            halign: 'center'
            font_size: "16sp"
            adaptive_height: True

        MDTextField:
            id: usuario
            mode: "filled"
            size_hint_x: 1
            
            MDTextFieldHintText:
                text: "Usuário ou E-mail"
            
            MDTextFieldLeadingIcon:
                icon: "account"

        MDTextField:
            id: senha
            password: True
            mode: "filled"
            size_hint_x: 1

            MDTextFieldHintText:
                text: "Senha"
            
            MDTextFieldLeadingIcon:
                icon: "lock"
            
            MDTextFieldTrailingIcon:
                icon: "eye-off"
                on_touch_down:
                    if self.icon == "eye-off": self.icon = "eye"; senha.password = False
                    else: self.icon = "eye-off"; senha.password = True

        MDButton:
            style: "filled"
            on_release: app.fazer_login(usuario.text, senha.text)
            size_hint_x: 1
            pos_hint: {'center_x': 0.5}

            MDButtonText:
                text: "ENTRAR"
                font_size: "16sp"
                bold: True
                
        MDButton:
            style: "text"
            on_release: app.esqueci_senha()
            pos_hint: {'center_x': 0.5}

            MDButtonText:
                text: 'Esqueci minha senha'
                theme_text_color: 'Primary'
                font_size: "14sp"
'''

class LoginApp(MDApp):
    dialog = None

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)

    def fazer_login(self, usuario, senha):
        if usuario.strip() and senha.strip():
            self.show_alert_dialog("Sucesso!", f"Login realizado para o usuário: {usuario}")
        else:
            self.show_alert_dialog("Erro", "Por favor, preencha todos os campos.")
            
    def esqueci_senha(self):
        self.show_alert_dialog("Aviso", "Função 'Esqueci minha senha' ainda não foi implementada.")

    def show_alert_dialog(self, title, text):
        if self.dialog:
            return

        self.dialog = MDDialog(
            MDDialogHeadlineText(text=title),
            MDDialogSupportingText(text=text),
            MDDialogButtonContainer(
                MDButton( # Agora o Python sabe o que é MDButton
                    MDButtonText(text="OK"), # E o que é MDButtonText
                    style="text",
                    on_release=self.close_dialog,
                ),
                spacing="8dp",
            ),
        )
        self.dialog.open()

    def close_dialog(self, *args):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None

if __name__ == '__main__':
    LoginApp().run()
