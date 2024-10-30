import io
import sys
import json

from PyQt6 import uic
from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QDialog, QApplication, QLineEdit, QDialogButtonBox, QHBoxLayout, QWidget, QCheckBox

from config.const import TimeZone


from project.layout.custom_layout_widget.layout import CustomLayoutAddTimeZone

class Register(QDialog):
    '''
    Диалог Входа пользователя
    '''
    def __init__(self):
        super().__init__()
        uic.loadUi('project/Layout/ui/register.ui', self)
        self.enter_password.setEchoMode(QLineEdit.EchoMode.Password)

    def get_login_password(self):
        return self.enter_login.text(),  self.enter_password.text()


class AddTimeZone(QWidget):
    '''
     добавления часовых поясов
    '''
    def __init__(self, time_zone):
        super().__init__()
        uic.loadUi('project/Layout/ui/add_time_zone02.ui', self)
        '''
        Все таже настройка и работа с паметью к сожалению как не дублировать это тминимальный код, я не предумывал,
        считаю что мексины сделают логику приложения более сложной из-за этого подход в данном случае исключаю
        '''
        self.setting = QSettings('23', "Reg'clock")

        '''
        Настройка и позиционриование кнопок окна диалога 
        '''

        self.costom_layout = CustomLayoutAddTimeZone()
        main_layout = self.costom_layout.setup_main_layout()

        button_home = self.main_widget_button
        button_save = self.save_widget_button
        self.costom_layout.button_layout_home_nav.addWidget(button_home, 0, 0)
        self.costom_layout.button_layout_home_nav.addWidget(button_save, 0, 1)

        # button_box.setParent(None)
        # button_layout = QHBoxLayout()
        # button_layout.addWidget(button_box)
        print("Yes, this comand start")

        self.setLayout(main_layout)



        '''
        Работа с паметью и часовыми поясами
        '''
        self.timezone = time_zone
        self.all_time_zone = TimeZone.ALLTIMEZONE
        self.sp_checkbox = []
        self.create_view_for_timezone()


        '''
        Настройка связий кнопок
        '''
        button_save.clicked.connect(self.save_timezone)


    def create_view_for_timezone(self):
        x, y = 0, 0
        for key, value  in self.all_time_zone.items():
            q = QCheckBox(f'{key}, {value}')
            q.setStyleSheet('color: black; border-radius: 5px; border: 2px solid black;')
            q.setFixedSize(350, 40)
            if key in self.timezone:
                q.setChecked(True)
            self.costom_layout.inner_layout.addWidget(q, y, x)
            if x > 1:
                x, y = 0, y + 1
            else:
                x += 1
            self.sp_checkbox.append(q)

    def save_timezone(self):
        new_timezones = {}
        for elem in self.sp_checkbox:
            key, value = elem.text().split(', ')
            if elem.isChecked():
                new_timezones[key] = value
        self.setting.setValue('timezones', json.dumps(new_timezones))
        
            


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AddTimeZone()
    ex.show()
    sys.exit(app.exec())