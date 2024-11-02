import psycopg2
import sys

import database
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt
from PyQt6 import uic

from project.layout.custom_layout_widget.layout import CustomLayoutProfile


class MyProfile(QWidget, CustomLayoutProfile):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi('project/Layout/ui/profile.ui', self)
        self.parent = parent

        '''
        То самое нудное позиционирование элементов  help me
        '''
        self.custom_layout = CustomLayoutProfile()
        main_layout = self.custom_layout.setup_main_layout()
        self.custom_layout.button_layout_home_nav.addWidget(self.add_clock_button, 0, 0)
        self.custom_layout.button_layout_home_nav.addWidget(self.view_friends_button, 0, 1)
        self.custom_layout.button_layout_home_nav.addWidget(self.home_button, 0, 2)
        self.custom_layout.layout_from_top_button.addWidget(self.check_request_button, 0, 1)
        self.setLayout(main_layout)


        '''Обработка событий кнопки'''
        self.add_clock_button.clicked.connect(self.create_new_clock)

    
    def create_new_clock(self):
        self.parent.stacked_widget.setCurrentIndex(3)


class CreateClock(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        uic.loadUi('project/Layout/ui/create_clock.ui', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyProfile()
    ex.show()
    sys.exit(app.exec())
    ex.db.exit()