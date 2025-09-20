from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFillRoundFlatButton, MDRectangleFlatIconButton


class UILayouts:
    def __init__(self, manager, controls=None):
        """
        :param manager: ScreenManager для управления экранами
        :param controls: UIControls — для кнопки 'Назад' и переходов
        """
        self.manager = manager
        self.controls = controls

    # ===============================
    # Создание всех экранов приложения
    # ===============================
    def create_all_screens(self):
        self.create_login_screen()
        self.create_main_screen()
        self.create_my_shelf()
        self.create_book_detail()
        self.create_add_book()
        self.create_search()

    # ===============================
    # Универсальные элементы
    # ===============================
    def create_back_button(self):
        """
        Универсальная кнопка 'Назад', возвращает на предыдущий экран
        """
        return MDRectangleFlatIconButton(
            text="Назад",
            icon="arrow-left",
            size_hint=(None, None),
            width=150,
            height=50,
            pos_hint={"center_x": 0.5},
            on_release=self.controls.go_back
        )

    def create_title_label(self, text):
        """
        Заголовок для экрана
        """
        label = Label(
            text=text,
            font_size=28,
            bold=True,
            color=(0.2, 0.4, 0.8, 1),
            size_hint=(1, 0.2),
            halign='center',
            valign='middle'
        )
        label.bind(size=label.setter('text_size'))
        return label

    # ===============================
    # Экраны приложения
    # ===============================

    def create_login_screen(self):
        screen = Screen(name="login")
        layout = BoxLayout(orientation="vertical", padding=40, spacing=20)

        layout.add_widget(self.create_title_label("Экран входа"))

        login_btn = MDFillRoundFlatButton(
            text="Войти",
            size_hint=(None, None),
            width=200,
            height=60,
            pos_hint={"center_x": 0.5},
            on_release=lambda x: self.controls.open_screen("main")
        )
        layout.add_widget(login_btn)

        screen.add_widget(layout)
        self.manager.add_widget(screen)

    def create_main_screen(self):
        screen = Screen(name="main")
        layout = BoxLayout(orientation="vertical", padding=40, spacing=30)

        # Заголовок
        layout.add_widget(self.create_title_label("Моя библиотека"))

        # Блок кнопок
        button_layout = BoxLayout(
            orientation="vertical",
            spacing=15,
            size_hint=(0.6, 0.6),
            pos_hint={'center_x': 0.5}
        )

        buttons = [
            ('Моя полка', lambda x: self.controls.open_screen('my_shelf')),
            ('Прочитано', lambda x: self.controls.open_screen('my_shelf')),
            ('Читаю', lambda x: self.controls.open_screen('my_shelf')),
            ('Хочу прочитать', lambda x: self.controls.open_screen('my_shelf')),
            ('Добавить книгу', lambda x: self.controls.open_screen('add_book')),
            ('Поиск', lambda x: self.controls.open_screen('search')),
        ]

        for text, callback in buttons:
            btn = MDFillRoundFlatButton(
                text=text,
                size_hint=(1, None),
                height=50,
                font_size=18,
                on_release=callback
            )
            button_layout.add_widget(btn)

        layout.add_widget(button_layout)
        screen.add_widget(layout)
        self.manager.add_widget(screen)

    def create_my_shelf(self):
        screen = Screen(name="my_shelf")
        layout = BoxLayout(orientation="vertical", padding=20, spacing=20)

        layout.add_widget(self.create_title_label("Моя полка книг"))
        layout.add_widget(self.create_back_button())

        screen.add_widget(layout)
        self.manager.add_widget(screen)

    def create_book_detail(self):
        screen = Screen(name="book_detail")
        layout = BoxLayout(orientation="vertical", padding=20, spacing=20)

        layout.add_widget(self.create_title_label("Детальная информация о книге"))
        layout.add_widget(self.create_back_button())

        screen.add_widget(layout)
        self.manager.add_widget(screen)

    def create_add_book(self):
        screen = Screen(name="add_book")
        layout = BoxLayout(orientation="vertical", padding=20, spacing=20)

        layout.add_widget(self.create_title_label("Добавление новой книги"))
        layout.add_widget(self.create_back_button())

        screen.add_widget(layout)
        self.manager.add_widget(screen)

    def create_search(self):
        screen = Screen(name="search")
        layout = BoxLayout(orientation="vertical", padding=20, spacing=20)

        layout.add_widget(self.create_title_label("Поиск по библиотеке"))
        layout.add_widget(self.create_back_button())

        screen.add_widget(layout)
        self.manager.add_widget(screen)
