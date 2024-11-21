import io
import sys
import json

from PyQt6 import uic
from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QDialog, QApplication, QLineEdit, QDialogButtonBox, QHBoxLayout, QWidget, QCheckBox
from PyQt6.QtWidgets import QMessageBox
from config.const import TimeZone
from database.connect_bd import DatabaseUser


from project.layout.custom_layout_widget.layout import CustomLayoutAddTimeZone
from config.decorators import resource_path


class Register(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(resource_path('project/layout/ui/register.ui'), self)
        self.buttonBox.accepted.connect(self.accept)  # Обработка кнопки "Вход"
        self.buttonBox.rejected.connect(self.reject)

    def get_login_password_register(self):
        return self.enter_login.text(), self.enter_password.text()


class Login(QDialog):
    '''
    Диалог Входа пользователя
    '''
    def __init__(self):
        super().__init__()
        uic.loadUi(resource_path('project/layout/ui/login_window.ui'), self)
        self.enter_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.register_button.clicked.connect(self.register)
        self.buttonBox_2.accepted.connect(self.accept)  # Обработка кнопки "Вход"
        self.buttonBox_2.rejected.connect(self.reject)


    def register(self):
        text = ''
        while True:
            register_window = Register()

            if register_window.exec() == QDialog.DialogCode.Accepted:
                try:
                    login, password = register_window.get_login_password_register()
                    if len(login) < 15 and len(password) > 6:
                        a = DatabaseUser()
                        a.create_user(login, password)
                        break
                    else:
                        text = f'Введен не правильный формат пароля или логина"'
                except Exception as e:
                    text = f'Произошла ошибка!! {e}'
                    print(e)
            else:
                break

    def get_login_password(self):
        return self.enter_login.text(),  self.enter_password.text()


class AddTimeZone(QWidget):
    '''
     добавления часовых поясов
    '''
    def __init__(self, time_zone):
        super().__init__()
        uic.loadUi(resource_path('project/layout/ui/add_time_zone02.ui'), self)
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
    ex = Login()
    ex.show()
    sys.exit(app.exec())