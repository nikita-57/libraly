from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDRectangleFlatIconButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen


class UILayouts:
    def __init__(self, manager, controls=None, db=None):
        self.manager = manager
        self.controls = controls
        self.db = db
        self.selected_status = None  # выбранный статус книги

    # ---------- СОЗДАНИЕ ВСЕХ ЭКРАНОВ ----------
    def create_all_screens(self):
        """Создаёт все экраны приложения"""
        self.create_login_screen()
        self.create_main_screen()
        self.create_my_shelf_screen()
        self.create_book_detail_screen()
        self.create_add_book()
        self.create_search_screen()

    # ---------- Универсальные элементы ----------
    def create_title_label(self, text):
        """Создаёт заголовок для экранов"""
        return Label(
            text=text,
            font_size=28,
            bold=True,
            size_hint=(1, 0.2),
            halign='center',
            valign='middle',
            color=(0, 0, 0, 1)
        )

    def create_back_button(self):
        """Кнопка 'Назад' для возврата на предыдущий экран"""
        return MDRectangleFlatIconButton(
            text="Назад",
            icon="arrow-left",
            size_hint=(None, None),
            width=150,
            height=50,
            pos_hint={"center_x": 0.5},
            on_release=self.controls.go_back
        )

    # ---------- Экран логина ----------
    def create_login_screen(self):
        screen = Screen(name="login")
        layout = BoxLayout(orientation="vertical", padding=20, spacing=20)
        layout.add_widget(self.create_title_label("Экран входа"))

        btn = MDRaisedButton(
            text="Войти",
            size_hint=(None, None),
            width=200,
            pos_hint={"center_x": 0.5},
            on_release=lambda x: self.controls.open_screen("main")
        )
        layout.add_widget(btn)
        screen.add_widget(layout)
        self.manager.add_widget(screen)

    # ---------- Главный экран ----------
    def create_main_screen(self):
        screen = Screen(name="main")
        layout = BoxLayout(orientation="vertical", padding=20, spacing=20)

        layout.add_widget(self.create_title_label("Моя библиотека"))

        # Кнопки главного меню
        buttons = [
    ("Моя полка", lambda x: (self.load_books(), self.controls.open_screen("my_shelf"))),
    ("Прочитано", lambda x: (self.load_books("read"), self.controls.open_screen("my_shelf"))),
    ("Читаю", lambda x: (self.load_books("reading"), self.controls.open_screen("my_shelf"))),
    ("Хочу прочитать", lambda x: (self.load_books("want_to_read"), self.controls.open_screen("my_shelf"))),
    ("Добавить книгу", lambda x: self.controls.open_screen("add_book")),
    ("Поиск", lambda x: self.controls.open_screen("search")),
]


        for text, callback in buttons:
            btn = MDRaisedButton(
                text=text,
                size_hint=(None, None),
                width=250,
                pos_hint={"center_x": 0.5},
                on_release=callback
            )
            layout.add_widget(btn)

        screen.add_widget(layout)
        self.manager.add_widget(screen)

    # ---------- Экран деталей книги ----------
    def create_book_detail_screen(self):
        screen = Screen(name="book_detail")
        layout = BoxLayout(orientation="vertical", padding=20, spacing=20)
        layout.add_widget(self.create_title_label("Детальная информация о книге"))
        layout.add_widget(self.create_back_button())
        screen.add_widget(layout)
        self.manager.add_widget(screen)

    # ---------- Экран добавления книги ----------
    def create_add_book(self):
        screen = Screen(name="add_book")

        # Основной контейнер
        layout = BoxLayout(orientation="vertical", padding=20, spacing=20)
        layout.add_widget(self.create_title_label("Добавить новую книгу"))

        # Поле ввода Названия
        self.title_input = MDTextField(
            hint_text="Название книги",
            helper_text="Обязательное поле",
            helper_text_mode="on_focus"
        )
        layout.add_widget(self.title_input)

        # Поле ввода Автора
        self.author_input = MDTextField(hint_text="Автор")
        layout.add_widget(self.author_input)

        # Поле ввода Описания
        self.description_input = MDTextField(
            hint_text="Описание книги",
            helper_text="Необязательное поле",
            helper_text_mode="on_focus"
        )
        layout.add_widget(self.description_input)

        # Выбор статуса через выпадающее меню
        status_items = [
            {"text": "Прочитано", "code": "read"},
            {"text": "Читаю", "code": "reading"},
            {"text": "Хочу прочитать", "code": "want_to_read"},
        ]

        def set_status(selected_item):
            self.selected_status = selected_item["code"]
            self.status_button.text = f"Статус: {selected_item['text']}"
            self.status_menu.dismiss()

        self.status_button = MDRaisedButton(
            text="Выбрать статус",
            size_hint=(None, None),
            width=200,
            pos_hint={"center_x": 0.5}
        )

        self.status_menu = MDDropdownMenu(
            caller=self.status_button,
            items=[
                {
                    "viewclass": "OneLineListItem",
                    "text": item["text"],
                    "on_release": lambda x=item: set_status(x)
                } for item in status_items
            ],
            width_mult=4
        )

        self.status_button.bind(on_release=lambda x: self.status_menu.open())
        layout.add_widget(self.status_button)

        # Кнопка сохранения книги
        save_button = MDRaisedButton(
            text="Сохранить книгу",
            size_hint=(None, None),
            width=200,
            pos_hint={"center_x": 0.5},
            on_release=lambda x: self.save_book()
        )
        layout.add_widget(save_button)

        # Кнопка Назад
        layout.add_widget(self.create_back_button())

        screen.add_widget(layout)
        self.manager.add_widget(screen)

    # ---------- Сохранение книги ----------
    def save_book(self):
        title = self.title_input.text.strip()
        author = self.author_input.text.strip()
        description = self.description_input.text.strip()
        status = self.selected_status

        # Валидация данных
        if not title:
            print("Ошибка: Название книги обязательно!")
            return

        if not status:
            print("Ошибка: Выберите статус!")
            return

        # Сохраняем книгу в базу данных
        try:
            self.db.add_book(title, author, description, status)
            print(f"Книга '{title}' успешно добавлена!")

            # Очищаем форму
            self.title_input.text = ""
            self.author_input.text = ""
            self.description_input.text = ""
            self.selected_status = None
            self.status_button.text = "Выбрать статус"

        except Exception as e:
            print(f"Ошибка при добавлении книги: {e}")

    # ---------- Экран поиска ----------
    def create_search_screen(self):
        screen = Screen(name="search")
        layout = BoxLayout(orientation="vertical", padding=20, spacing=20)
        layout.add_widget(self.create_title_label("Поиск по библиотеке"))
        layout.add_widget(self.create_back_button())
        screen.add_widget(layout)
        self.manager.add_widget(screen)

    def create_my_shelf_screen(self):
        screen = Screen(name="my_shelf")

        main_layout = BoxLayout(orientation="vertical", padding=20, spacing=20)

        main_layout.add_widget(self.create_title_label("Моя полка книг"))

        from kivy.uix.scrollview import ScrollView
        scroll_view = ScrollView(size_hint=(1, 1))

        self.books_container = BoxLayout(
            orientation="vertical",
            spacing=10,
            size_hint_y=None
        )
        self.books_container.bind(minimum_height=self.books_container.setter('height'))

        scroll_view.add_widget(self.books_container)
        main_layout.add_widget(scroll_view)

        main_layout.add_widget(self.create_back_button())
        screen.add_widget(main_layout)
        self.manager.add_widget(screen)



    def load_books(self, status_code=None):
        """Загружает книги из базы и обновляет список на экране"""
        self.books_container.clear_widgets()

        try:
            books = self.db.get_books(status_code)  # передаём статус в запрос
            if not books:
                self.books_container.add_widget(
                    Label(
                        text="Нет книг в библиотеке",
                        color=(0, 0, 0, 1),
                        size_hint_y=None,
                        height=40
                    )
                )
                return

            for book in books:
                title = book['title']
                author = book['author'] if book['author'] else "Автор неизвестен"
                status = book['status'] if book['status'] else "Статус не указан"

                self.books_container.add_widget(
                    Label(
                        text=f"{title} — {author} ({status})",
                        color=(0, 0, 0, 1),
                        size_hint_y=None,
                        height=40
                    )
                )

        except Exception as e:
            self.books_container.add_widget(
                Label(
                    text=f"Ошибка загрузки книг: {e}",
                    color=(1, 0, 0, 1),
                    size_hint_y=None,
                    height=40
                )
            )
            print("Ошибка при загрузке книг:", e)

    def create_search_screen(self):
        screen = Screen(name="search")

        layout = BoxLayout(orientation="vertical", padding=20, spacing=20)

        layout.add_widget(self.create_title_label("Поиск по библиотеке"))

        # Поле для ввода текста
        self.search_input = MDTextField(
            hint_text="Введите название или автора",
            size_hint_x=1,
            mode="rectangle"
        )
        layout.add_widget(self.search_input)

        # Кнопка поиска
        search_button = MDRaisedButton(
            text="Найти",
            size_hint=(None, None),
            width=200,
            pos_hint={"center_x": 0.5},
            on_release=lambda x: self.perform_search()
        )
        layout.add_widget(search_button)

        # Прокручиваемый список для результатов
        scroll_view = ScrollView(size_hint=(1, 1))

        self.search_results_container = BoxLayout(
            orientation="vertical",
            spacing=10,
            size_hint_y=None
        )
        self.search_results_container.bind(
            minimum_height=self.search_results_container.setter('height')
        )

        scroll_view.add_widget(self.search_results_container)
        layout.add_widget(scroll_view)

        layout.add_widget(self.create_back_button())

        screen.add_widget(layout)
        self.manager.add_widget(screen)


    def perform_search(self):
        """Выполняет поиск книг и отображает результаты"""
        query = self.search_input.text.strip()

        self.search_results_container.clear_widgets()

        if not query:
            self.search_results_container.add_widget(
                Label(
                    text="Введите запрос для поиска",
                    color=(0, 0, 0, 1),
                    size_hint_y=None,
                    height=40
                )
            )
            return

        try:
            books = self.db.search_books(query)

            if not books:
                self.search_results_container.add_widget(
                    Label(
                        text="Книг не найдено",
                        color=(0, 0, 0, 1),
                        size_hint_y=None,
                        height=40
                    )
                )
                return

            for book in books:
                title = book['title']
                author = book['author'] if book['author'] else "Автор неизвестен"
                status = book['status'] if book['status'] else "Статус не указан"

                self.search_results_container.add_widget(
                    Label(
                        text=f"{title} — {author} ({status})",
                        color=(0, 0, 0, 1),
                        size_hint_y=None,
                        height=40
                    )
                )
        except Exception as e:
            self.search_results_container.add_widget(
                Label(
                    text=f"Ошибка поиска: {e}",
                    color=(1, 0, 0, 1),
                    size_hint_y=None,
                    height=40
                )
            )
            print("Ошибка поиска:", e)
