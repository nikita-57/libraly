class UIControls:
    def __init__(self, manager):
        self.manager = manager
        self.history = []

    def open_screen(self, screen_name):
        if screen_name in self.manager.screen_names:
            self.history.append(self.manager.current)
            self.manager.current = screen_name
        else:
            print(f"Экран '{screen_name}' не найден")
    def go_back(self, instance=None):
        if self.history:
            previous_screen = self.history.pop()
            self.manager.current = previous_screen
        else:
            self.manager.current = 'main'