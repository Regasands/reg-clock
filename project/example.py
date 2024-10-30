import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QStackedWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Создаем стек виджетов
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Создаем экраны (виджеты)
        self.screen1 = Screen1(self)
        self.screen2 = Screen2(self)

        # Добавляем экраны в стек
        self.stacked_widget.addWidget(self.screen1)
        self.stacked_widget.addWidget(self.screen2)

        # Устанавливаем начальный экран
        self.stacked_widget.setCurrentIndex(0)

    def switch_to_screen1(self):
        self.stacked_widget.setCurrentIndex(0)

    def switch_to_screen2(self):
        self.stacked_widget.setCurrentIndex(1)

class Screen1(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Макет и кнопка для перехода на экран 2
        layout = QVBoxLayout()
        button = QPushButton("Перейти на экран 2")
        button.clicked.connect(self.main_window.switch_to_screen2)
        layout.addWidget(button)

        self.setLayout(layout)

class Screen2(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Макет и кнопка для перехода на экран 1
        layout = QVBoxLayout()
        button = QPushButton("Вернуться на экран 1")
        button.clicked.connect(self.main_window.switch_to_screen1)
        layout.addWidget(button)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
