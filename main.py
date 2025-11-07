from kivy.lang import Builder
from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.app import MDApp
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
                
        MDButton:
            style: "text"
            on_release: app.esqueci_senha()
            pos_hint: {'center_x': 0.5}

            MDButtonText:
                text: 'Esqueci minha senha'
                theme_text_color: 'Primary'

        MDLabel:
            id: status_label
            text: "Verificando tema do sistema..."
            halign: "center"
            theme_text_color: "Secondary"
            font_size: "12sp"
            adaptive_height: True
'''

class DynamicLoginApp(MDApp):
    dialog = None

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        return Builder.load_string(KV)

    def on_start(self):
        Clock.schedule_once(lambda dt: self.activate_dynamic_color(), 1)

    def activate_dynamic_color(self, *args):
        """Ativa as cores dinâmicas."""
        try:
            print("Tentando ativar dynamic_color...")
            self.theme_cls.dynamic_color = True
            self.theme_cls.set_colors()
            Clock.schedule_once(self.update_ui, 0.5)
        except Exception as e:
            print(f"Erro ao ativar dynamic_color: {e}")
            # --- CORREÇÃO CRÍTICA AQUI ---
            # Desativa o modo dinâmico antes de chamar o fallback para evitar o crash.
            self.theme_cls.dynamic_color = False
            self.fallback_theme()

    def update_ui(self, dt):
        """Atualiza a interface com as cores dinâmicas."""
        try:
            primary_color_info = ""
            if hasattr(self.theme_cls, '_primary_color'):
                primary = self.theme_cls._primary_color
                primary_color_info = f" | Cor primária: RGB{primary[:3]}"

            status_text = f"Cores dinâmicas ativadas!{primary_color_info}"
            self.root.ids.status_label.text = status_text
            print("Dynamic color aplicado com sucesso!")
            
            Clock.schedule_once(lambda dt: self.hide_status_label(), 4)
        except Exception as e:
            print(f"Erro ao atualizar UI: {e}")
            self.fallback_theme()

    def fallback_theme(self):
        """Fallback caso o dynamic_color não funcione."""
        theme_info = "Tema Padrão (Fallback)"
        try:
            from jnius import autoclass
            Configuration = autoclass('android.content.res.Configuration')
            context = autoclass('org.kivy.android.PythonActivity').mActivity
            
            current_night_mode = context.getResources().getConfiguration().uiMode & Configuration.UI_MODE_NIGHT_MASK
            
            if current_night_mode == Configuration.UI_MODE_NIGHT_YES:
                self.theme_cls.theme_style = "Dark"
                self.theme_cls.primary_palette = "DeepPurple"
                theme_info = "Tema Escuro (Fallback)"
            else:
                self.theme_cls.theme_style = "Light"
                self.theme_cls.primary_palette = "Blue" 
                theme_info = "Tema Claro (Fallback)"
                
        except Exception as e:
            print(f"Erro no fallback (usando tema padrão): {e}")
            self.theme_cls.theme_style = "Light"
            self.theme_cls.primary_palette = "Teal"
        finally:
            self.root.ids.status_label.text = theme_info
            Clock.schedule_once(lambda dt: self.hide_status_label(), 4)

    def hide_status_label(self):
        self.root.ids.status_label.text = ""

    # --- Métodos da lógica de login ---
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
    DynamicLoginApp().run()
