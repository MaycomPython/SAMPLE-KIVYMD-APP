from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.clock import Clock

# Import dos componentes de Dialog
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
)

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
    dynamic_color_activated = False

    def build(self):
        # Configuração inicial segura
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        return Builder.load_string(KV)

    def on_start(self):
        """Tenta ativar o Material You com tratamento de erro melhorado"""
        Clock.schedule_once(lambda dt: self.safe_activate_dynamic_color(), 1)

    def safe_activate_dynamic_color(self):
        """Ativa o dynamic color com proteção contra erros"""
        try:
            print("Tentando ativar Material You...")
            
            # Primeiro, tenta a abordagem mais recente
            self.theme_cls.dynamic_color = True
            
            # Usamos um método diferente para evitar o bug
            self.force_refresh_theme()
            
            self.dynamic_color_activated = True
            print("✅ Material You ativado com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao ativar Material You: {e}")
            self.dynamic_color_activated = False
            self.safe_fallback_theme()

    def force_refresh_theme(self):
        """Força atualização do tema sem usar set_colors() problemático"""
        try:
            # Método alternativo para atualizar cores
            current_style = self.theme_cls.theme_style
            # Alterna temporariamente o tema para forçar atualização
            self.theme_cls.theme_style = "Dark" if current_style == "Light" else "Light"
            self.theme_cls.theme_style = current_style
        except Exception as e:
            print(f"Aviso no refresh: {e}")

    def safe_fallback_theme(self):
        """Fallback seguro sem usar set_colors()"""
        try:
            print("Aplicando fallback seguro...")
            
            # IMPORTANTE: Desativa dynamic_color antes do fallback
            self.theme_cls.dynamic_color = False
            
            # Aplica tema simples sem dependências problemáticas
            self.theme_cls.theme_style = "Light"
            self.theme_cls.primary_palette = "Green"
            
            print("✅ Fallback aplicado com sucesso")
            
        except Exception as e:
            print(f"❌ Erro no fallback: {e}")
            # Último recurso - reinicia o tema_cls
            try:
                self.theme_cls.theme_style = "Light"
            except:
                pass

    def fazer_login(self, usuario, senha):
        if usuario.strip() and senha.strip():
            self.show_alert_dialog("Sucesso!", f"Login realizado para o usuário: {usuario}")
        else:
            self.show_alert_dialog("Erro", "Por favor, preencha todos os campos.")
            
    def esqueci_senha(self):
        self.show_alert_dialog("Aviso", "Função 'Esqueci minha senha' ainda não foi implementada.")

    def show_alert_dialog(self, title, text):
        if self.dialog:
            self.dialog.dismiss()

        self.dialog = MDDialog(
            MDDialogHeadlineText(text=title),
            MDDialogSupportingText(text=text),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="OK"),
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
