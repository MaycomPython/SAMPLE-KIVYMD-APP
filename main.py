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
    material_you_ativado = False

    def build(self):
        # Configuração inicial mínima
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)

    def on_start(self):
        """Tenta ativar o Material You de forma segura"""
        Clock.schedule_once(self.tentar_material_you, 1)

    def tentar_material_you(self, dt):
        """Método simplificado e direto para ativar Material You"""
        try:
            print("🎨 Tentando ativar Material You...")
            
            # Método direto que funcionou no outro script
            self.theme_cls.dynamic_color = True
            
            # Pequeno delay para garantir que as cores sejam aplicadas
            Clock.schedule_once(self.verificar_cores, 0.5)
            
        except Exception as e:
            print(f"❌ Material You não disponível: {e}")
            self.aplicar_tema_fallback()

    def verificar_cores(self, dt):
        """Verifica se as cores dinâmicas foram aplicadas"""
        try:
            # Verifica se as cores dinâmicas estão funcionando
            if hasattr(self.theme_cls, 'primary_color') and self.theme_cls.primary_color:
                self.material_you_ativado = True
                print("✅ Material You ativado com sucesso!")
                print(f"Cor primária: {self.theme_cls.primary_color}")
            else:
                self.aplicar_tema_fallback()
                
        except Exception as e:
            print(f"⚠️ Aviso na verificação de cores: {e}")
            self.aplicar_tema_fallback()

    def aplicar_tema_fallback(self):
        """Aplica fallback seguro sem Material You"""
        try:
            print("🔄 Aplicando tema fallback...")
            self.theme_cls.dynamic_color = False
            self.theme_cls.primary_palette = "Green"
            self.theme_cls.theme_style = "Light"
            self.material_you_ativado = False
        except Exception as e:
            print(f"⚠️ Erro no fallback: {e}")

    def fazer_login(self, usuario, senha):
        if usuario.strip() and senha.strip():
            status_material = "com Material You ✅" if self.material_you_ativado else "com tema padrão 🔄"
            self.show_alert_dialog("Sucesso!", f"Login realizado para: {usuario}\n{status_material}")
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
