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
            text: "Dynamic Color: Iniciando..."
            halign: "center"
            theme_text_color: "Primary"
            adaptive_size: True

        MDRaisedButton:
            id: permission_btn
            text: "Conceder Permissão para Wallpaper"
            pos_hint: {"center_x": .5}
            on_release: app.request_android_permissions()
            adaptive_size: True

        MDLabel:
            id: debug_label
            text: ""
            halign: "center"
            theme_text_color: "Secondary"
            adaptive_size: True
'''

class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)

    def on_start(self):
        self.update_debug("App iniciado")
        if platform == "android":
            # Aguarda um pouco antes de solicitar permissões
            Clock.schedule_once(lambda dt: self.setup_android(), 1)
        else:
            self.activate_dynamic_color()

    def setup_android(self):
        """Configuração específica para Android"""
        self.update_debug("Configurando para Android...")
        
        # Verifica se já tem permissão
        if self.has_storage_permission():
            self.update_debug("Permissão já concedida")
            self.activate_dynamic_color()
        else:
            self.update_debug("Aguardando solicitação de permissão...")
            # Mostra o botão para solicitar permissão manualmente
            self.root.ids.permission_btn.disabled = False

    def has_storage_permission(self):
        """Verifica se a permissão já foi concedida"""
        if platform != "android":
            return True
            
        try:
            from android.permissions import check_permission, Permission
            has_perm = check_permission(Permission.READ_EXTERNAL_STORAGE)
            self.update_debug(f"Permissão verificada: {has_perm}")
            return has_perm
        except Exception as e:
            self.update_debug(f"Erro ao verificar permissão: {e}")
            return False

    def request_android_permissions(self):
        """Solicita permissões do usuário"""
        self.update_debug("Solicitando permissões...")
        
        if platform != "android":
            self.activate_dynamic_color()
            return

        try:
            from android.permissions import Permission, request_permissions
            
            # Para Android 13+ pode precisar de permissões diferentes
            permissions = [Permission.READ_EXTERNAL_STORAGE]
            
            def permission_callback(permissions, grant_results):
                self.update_debug(f"Resultado: {grant_results}")
                if all(grant_results):
                    self.update_debug("Permissões concedidas!")
                    self.root.ids.permission_btn.disabled = True
                    self.root.ids.permission_btn.text = "Permissão Concedida"
                    self.activate_dynamic_color()
                else:
                    self.update_debug("Permissões negadas :(")
                    self.root.ids.status_label.text = "Permissão negada - usando cores padrão"

            # Esta é a chamada que deve mostrar o diálogo
            request_permissions(permissions, permission_callback)
            self.update_debug("Diálogo de permissão solicitado")
            
        except Exception as e:
            self.update_debug(f"Erro nas permissões: {str(e)}")
            self.activate_dynamic_color()

    def activate_dynamic_color(self, *args):
        """Ativa as cores dinâmicas"""
        try:
            self.update_debug("Ativando dynamic_color...")
            
            # IMPORTANTE: Esta é a ordem correta
            self.theme_cls.dynamic_color = True
            self.theme_cls.set_colors()
            
            # Força uma atualização da UI
            Clock.schedule_once(self.update_ui_after_dynamic, 0.5)
            
        except Exception as e:
            self.update_debug(f"Erro no dynamic_color: {str(e)}")
            self.fallback_colors()

    def update_ui_after_dynamic(self, dt):
        """Atualiza a UI após ativar cores dinâmicas"""
        try:
            # Atualiza as cores da interface
            self.root.md_bg_color = self.theme_cls.surfaceColor
            
            status_text = f"Dynamic Color: Ativado!\\n"
            status_text += f"Tema: {self.theme_cls.theme_style}\\n"
            status_text += f"Primária: {self.theme_cls.primary_color}"
            
            self.root.ids.status_label.text = status_text
            self.update_debug("UI atualizada com cores dinâmicas")
            
        except Exception as e:
            self.update_debug(f"Erro ao atualizar UI: {str(e)}")

    def fallback_colors(self):
        """Cores de fallback se o dynamic_color falhar"""
        self.update_debug("Usando cores de fallback")
        
        # Cores padrão baseadas no tema do sistema
        try:
            from jnius import autoclass
            Configuration = autoclass('android.content.res.Configuration')
            context = autoclass('org.kivy.android.PythonActivity').mActivity
            
            current_night_mode = context.getResources().getConfiguration().uiMode & Configuration.UI_MODE_NIGHT_MASK
            
            if current_night_mode == Configuration.UI_MODE_NIGHT_YES:
                self.theme_cls.theme_style = "Dark"
                self.theme_cls.primary_palette = "DeepPurple"
            else:
                self.theme_cls.theme_style = "Light" 
                self.theme_cls.primary_palette = "Blue"
                
            self.root.ids.status_label.text = "Cores padrão (fallback)"
            
        except Exception as e:
            self.update_debug(f"Erro no fallback: {str(e)}")
            # Último fallback
            self.theme_cls.primary_palette = "Teal"

    def update_debug(self, message):
        """Atualiza o label de debug"""
        print(f"DEBUG: {message}")
        if hasattr(self, 'root') and self.root and 'debug_label' in self.root.ids:
            current_text = self.root.ids.debug_label.text
            new_text = f"{message}\\n{current_text}"
            # Mantém apenas as últimas 5 mensagens
            lines = new_text.split('\\n')
            if len(lines) > 5:
                new_text = '\\n'.join(lines[:5])
            self.root.ids.debug_label.text = new_text

    def on_resume(self, *args):
        """Recarrega quando o app volta do background"""
        if platform == "android":
            Clock.schedule_once(lambda dt: self.theme_cls.set_colors(), 0.5)

if __name__ == "__main__":
    Example().run()
