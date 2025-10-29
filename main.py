from kivy import platform
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.app import MDApp

KV = '''
MDScreen:
    md_bg_color: app.theme_cls.surfaceColor

    MDBoxLayout:
        orientation: "vertical"
        spacing: "20dp"
        padding: "20dp"
        pos_hint: {"center_x": .5, "center_y": .5}

        MDLabel:
            id: status_label
            text: "Dynamic Color: Aguardando..."
            halign: "center"
            theme_text_color: "Primary"

        MDButton:
            style: "elevated"
            pos_hint: {"center_x": .5}
            on_release: app.check_dynamic_color()

            MDButtonIcon:
                icon: "palette"

            MDButtonText:
                text: "Verificar Cores Dinâmicas"
'''


class Example(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dynamic_color_checked = False

    def build(self):
        self.theme_cls.theme_style_switch_animation = True
        return Builder.load_string(KV)

    def on_start(self):
        # Verifica se está no Android e tenta ativar dynamic_color
        if platform == "android":
            self.setup_android_permissions()
        else:
            # Para outras plataformas, apenas ativa
            self.activate_dynamic_color()

    def setup_android_permissions(self):
        def permission_callback(permissions, results):
            if all(results):
                print("Permissões concedidas")
                Clock.schedule_once(lambda dt: self.activate_dynamic_color(), 1)
            else:
                print("Permissões negadas")
                self.update_status("Permissões negadas - usando cores padrão")

        try:
            from android.permissions import Permission, request_permissions
            
            # Permissões atualizadas para Android 10+
            permissions = [
                Permission.READ_EXTERNAL_STORAGE,
            ]
            
            request_permissions(permissions, permission_callback)
        except ImportError:
            print("Não é Android - usando cores padrão")
            self.activate_dynamic_color()

    def activate_dynamic_color(self, *args):
        try:
            # Ativa dynamic_color
            self.theme_cls.dynamic_color = True
            self.theme_cls.set_colors()
            
            # Atualiza a interface
            self.update_ui_with_dynamic_colors()
            self.dynamic_color_checked = True
            
            print("Dynamic color ativado!")
            print(f"Primary color: {self.theme_cls.primary_color}")
            print(f"Surface color: {self.theme_cls.surfaceColor}")
            
        except Exception as e:
            print(f"Erro ao ativar dynamic_color: {e}")
            self.update_status(f"Erro: {str(e)}")

    def update_ui_with_dynamic_colors(self):
        try:
            # Atualiza o texto de status
            status_text = f"Dynamic Color: Ativado\\n"
            status_text += f"Primária: {self.theme_cls.primary_color}\\n"
            status_text += f"Surface: {self.theme_cls.surfaceColor}"
            
            self.root.ids.status_label.text = status_text
            
        except Exception as e:
            print(f"Erro ao atualizar UI: {e}")

    def update_status(self, message):
        if hasattr(self.root, 'ids') and 'status_label' in self.root.ids:
            self.root.ids.status_label.text = message

    def check_dynamic_color(self):
        """Função para verificar manualmente o dynamic color"""
        if not self.dynamic_color_checked:
            self.activate_dynamic_color()
        else:
            self.update_ui_with_dynamic_colors()

    def on_resume(self, *args):
        """Recarrega as cores quando o app retorna do background"""
        if platform == "android" and self.dynamic_color_checked:
            Clock.schedule_once(lambda dt: self.theme_cls.set_colors(), 0.5)


if __name__ == "__main__":
    Example().run()
