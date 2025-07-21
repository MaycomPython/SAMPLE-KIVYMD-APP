from kivy.lang import Builder

from carbonkivy.app import CarbonApp
from carbonkivy.uix.screen import CScreen

class MyApp(CarbonApp):

    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)

    def build(self, *args) -> CScreen:
        self.kvlang = '''

CScreen:

    CLabel:
        text: "Carbon Design System"
        font_size: plex_18
        halign: "center"
        pos_hint: {"center_x" : 0.5, "center_y" : 0.6}

    CButtonPrimary:
        text: "Primary Button"
        role: "Large Productive"
        pos_hint: {"center_x" : 0.5, "center_y" : 0.4}
        on_press:
            self.icon = "add"

        '''
        return Builder.load_string(self.kvlang)

if __name__ == "__main__":
    app = MyApp()
    app.run()
