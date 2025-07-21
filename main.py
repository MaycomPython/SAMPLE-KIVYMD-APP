# Arquivo: main.py

from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
import webbrowser

# A linha Window.size só deve ser usada para testes no desktop.
# Em um app real, ela deve ser removida para que o app ocupe a tela inteira.
# from kivy.core.window import Window
# Window.size = (360, 640)


class MainScreen(MDScreen):
    """
    A tela principal da calculadora. A lógica agora está no app principal,
    e a tela apenas contém os widgets.
    """
    pass


class SettingsScreen(MDScreen):
    """
    A tela de configurações.
    """
    pass


class CalculadoraApp(MDApp):
    def build(self):
        # Define o tema inicial do app
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        # Carrega a interface a partir de um arquivo .kv separado
        # O Kivy faz isso automaticamente se o nome do arquivo for 'calculadora.kv'
        return Builder.load_file('calculadora.kv')

    def on_button_click(self, value: str):
        """Adiciona um valor ao display da calculadora."""
        display = self.root.get_screen("main").ids.display
        current_text = display.text

        # Se o texto atual for '0' ou um 'Erro', substitui pelo novo valor
        if current_text == '0' or current_text == 'Erro':
            display.text = value
        else:
            display.text += value

    def clear_all(self):
        """Limpa o display, conectado ao botão 'AC'."""
        self.root.get_screen("main").ids.display.text = '0'

    def backspace(self):
        """Apaga o último caractere do display."""
        display = self.root.get_screen("main").ids.display
        current_text = display.text
        if len(current_text) > 1:
            display.text = current_text[:-1]
        else:
            display.text = '0'

    def calculate(self):
        """Calcula a expressão no display."""
        display = self.root.get_screen("main").ids.display
        try:
            # Substitui os caracteres visuais pelos operadores reais do Python
            expression = display.text.replace('x', '*').replace('÷', '/').replace(',', '.')
            # Usar eval() é perigoso em produção, mas ok para uma calculadora simples
            result = eval(expression)
            
            # Formata o resultado para remover o ".0" de números inteiros
            if result == int(result):
                result = int(result)
                
            display.text = str(result).replace('.', ',')
        except Exception:
            display.text = 'Erro'

    def change_screen(self, screen_name: str):
        """Muda a tela atual do ScreenManager."""
        self.root.current = screen_name

    def open_link(self):
        """Abre o link do seu Telegram."""
        webbrowser.open("https://t.me/Mayc00m")

    def toggle_theme(self, switch_instance, active: bool):
        """Alterna entre os temas Claro e Escuro."""
        if active:
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"


if __name__ == "__main__":
    CalculadoraApp().run()