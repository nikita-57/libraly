from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from ui_layouts import UILayouts
from ui_controls import UIControls


class MyLibraryApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Pink'

        self.manager = ScreenManager()

        # Инициализация контролов
        self.ui_controls = UIControls(self.manager)
        self.ui_layouts = UILayouts(self.manager, controls=self.ui_controls)

        # Создаём экраны
        self.ui_layouts.create_all_screens()

        return self.manager


if __name__ == '__main__':
    MyLibraryApp().run()
