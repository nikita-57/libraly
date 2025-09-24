class UIControls:
    def __init__(self, manager, db=None):
        self.manager = manager
        self.history = []  # стек экранов для кнопки "Назад"
        self.db = db       # объект базы данных

    def open_screen(self, screen_name):
        """Открывает указанный экран и добавляет текущий в историю."""
        if screen_name in self.manager.screen_names:
            # Добавляем в историю только если текущий экран не пустой и отличается
            if self.manager.current and self.manager.current != screen_name:
                self.history.append(self.manager.current)
            self.manager.current = screen_name
        else:
            print(f"[Ошибка] Экран '{screen_name}' не найден")

    def go_back(self, instance=None):
        """Возврат на предыдущий экран или на главный, если история пуста."""
        if self.history:
            previous_screen = self.history.pop()
            self.manager.current = previous_screen
            print(f"[Навигация] Возврат на экран: {previous_screen}")
        else:
            self.manager.current = 'main'
            print("[Навигация] История пуста. Возврат на главный экран.")