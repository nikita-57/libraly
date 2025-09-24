from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from ui_layouts import UILayouts
from ui_controls import UIControls
from app_logic import AppLogic  # подключаем работу с PostgreSQL


class MyLibraryApp(MDApp):
    def build(self):
        """
        Основной метод приложения.
        Здесь настраиваем тему, менеджер экранов и подключаем все модули.
        """
        # Настройки темы
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Pink'

        # ScreenManager — управление экранами
        self.manager = ScreenManager()

        # Инициализация логики работы с базой данных
        self.db = AppLogic()

        # Инициализация контролов (навигация и история экранов)
        self.ui_controls = UIControls(self.manager, db=self.db)

        # Инициализация интерфейса экранов
        self.ui_layouts = UILayouts(self.manager, controls=self.ui_controls, db=self.db)

        # Создаём все экраны приложения
        self.ui_layouts.create_all_screens()

        return self.manager


if __name__ == '__main__':
    MyLibraryApp().run()
