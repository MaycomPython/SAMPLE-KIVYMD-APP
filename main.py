from kivy import platform
from kivy.lang import Builder
from kivy.clock import Clock

from kivymd.app import MDApp

KV = '''
MDScreen:
    md_bg_color: app.theme_cls.surfaceColor

    MDButton:
        style: "elevated"
        pos_hint: {"center_x": .5, "center_y": .5}

        MDButtonIcon:
            icon: "plus"

        MDButtonText:
            text: "Elevated"
'''


class Example(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_resume(self, *args):
        '''Updating the color scheme when the application resumes.'''

        self.theme_cls.set_colors()

    def set_dynamic_color(self, *args) -> None:
        '''
        When sets the `dynamic_color` value, the self method will be
        `called.theme_cls.set_colors()` which will generate a color
        scheme from a custom wallpaper if `dynamic_color` is `True`.
        '''

        self.theme_cls.dynamic_color = True

    def on_start(self) -> None:
        '''
        It is fired at the start of the application and requests the
        necessary permissions.
        '''

        def callback(permission, results):
            if all([res for res in results]):
                Clock.schedule_once(self.set_dynamic_color)

        if platform == "android":
            from android.permissions import Permission, request_permissions

            permissions = [Permission.READ_EXTERNAL_STORAGE]
            request_permissions(permissions, callback)


Example().run()
