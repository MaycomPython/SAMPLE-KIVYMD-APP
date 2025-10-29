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
            text: "Aguardando ativação..."
            halign: "center"
            theme_text_color: "Primary"
            adaptive_size: True

        MDButton:
            id: check_btn
            text: "Ativar Cores Dinâmicas"
            pos_hint: {"center_x": .5}
            on_release: app.activate_dynamic_color()
            adaptive_size: True
'''

class Example(MDApp):
    def build(self):
        # Configuração inicial do tema
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

    def on_start(self):
        # Tenta ativar automaticamente após um breve delay
        Clock.schedule_once(lambda dt: self.activate_dynamic_color(), 2)

    def activate_dynamic_color(self, *args):
        """Ativa as cores dinâmicas sem precisar de permissões"""
        try:
            print("Tentando ativar dynamic_color...")
            
            # Método correto para ativar dynamic_color
            self.theme_cls.dynamic_color = True
            # Força a atualização das cores
            self.theme_cls.set_colors()
            
            # Atualiza a UI após as cores serem carregadas
            Clock.schedule_once(self.update_ui, 0.5)
            
        except Exception as e:
            print(f"Erro ao ativar dynamic_color: {e}")
            self.fallback_theme()

    def update_ui(self, dt):
        """Atualiza a interface com as cores dinâmicas"""
        try:
            # Atualiza o texto de status
            status_text = "Cores dinâmicas ativadas!\\n"
            
            # Acessa as cores de forma segura
            if hasattr(self.theme_cls, '_primary_color'):
                primary = self.theme_cls._primary_color
                status_text += f"Cor primária: RGB{primary[:3]}"
            else:
                status_text += "Usando cores do tema"
            
            self.root.ids.status_label.text = status_text
            self.root.ids.check_btn.text = "Cores Ativadas!"
            self.root.ids.check_btn.disabled = True
            
            print("Dynamic color aplicado com sucesso!")
            
        except Exception as e:
            print(f"Erro ao atualizar UI: {e}")
            self.fallback_theme()

    def fallback_theme(self):
        """Fallback caso o dynamic_color não funcione"""
        try:
            # Tenta detectar o tema do sistema
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
                
            self.root.ids.status_label.text = theme_info
            self.root.ids.check_btn.text = "Tema Fallback"
            
        except Exception as e:
            print(f"Erro no fallback: {e}")
            # Fallback final
            self.theme_cls.primary_palette = "Teal"
            self.root.ids.status_label.text = "Tema Padrão"

if __name__ == "__main__":
    Example().run()
