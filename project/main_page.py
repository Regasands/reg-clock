import sys
import json
from datetime import datetime, timezone, UTC, timedelta

from PyQt6 import uic, QtMultimedia
from PyQt6.QtWidgets import QWidget, QApplication, QPushButton, QLineEdit, QLabel, QCheckBox, QStackedWidget, QLayout, QStackedWidget
from PyQt6.QtWidgets import QMainWindow, QInputDialog, QDialog
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import QSettings, Qt, QTimer, QUrl

from database.connect_bd import DatabaseConnection
from project.dialogs import Login, AddTimeZone
from project.draw import custom_widget
from project.layout.custom_layout_widget.layout import CustomLayoutMainWidget
from config.decorators import format_date
from project.window_friends import MyProfile, CreateClock, ViewTaskFriend, ViewRequest
from config.decorators import resource_path


class CustomApplication(QApplication):
    '''
    Проврека на регистрацию перед входом
    '''
    def __init__(self, argv):
        super().__init__(argv)
        
        setting = QSettings('23', "Reg'clock")
        login = setting.value('username', None)
        password = setting.value('password', None)
        # login, password = None, None
        while True:
            if not login or not password:
                    login_window = Login()
                    if login_window.exec() == QDialog.DialogCode.Accepted:
                        login, password = login_window.get_login_password()
                    else:
                        sys.exit()

            try:
                self.db = DatabaseConnection(login, password)
                self.db.conect()

                setting.setValue('username', login)
                setting.setValue('password', password)
                self.login = login 
                break
            except Exception as e:
                print(e)
                
                login, password = None, None
         
        
class MainWindow(QMainWindow,  ):
    '''
    Основное меню
    '''
    def __init__(self, db, login):
        super().__init__()
        self.move(10, 10)
        uic.loadUi(resource_path('project/layout/ui/main_page.ui'), self)

        self.db = db

        self.settings = QSettings('23', "Reg'clock")

        '''
        Работа с часовыми поясами 
        '''
        now_local = datetime.now(timezone.utc).astimezone()
        offset = now_local.utcoffset()
        self.formatted_offset_h = f'{int(offset.total_seconds() // 3600):+03d}'
        self.formatted_offset_h = self.formatted_offset_h if self.formatted_offset_h[1] != '0' and len(self.formatted_offset_h) > 2 else f'{self.formatted_offset_h[0]} {self.formatted_offset_h[-1]}'
        self.formatted_offset_m = f'{abs(int((offset.total_seconds() % 3600) // 60)):02d}' 
        self.def_timzone = datetime.now().astimezone() - datetime.now(UTC)
        self.time_zone = json.loads(self.settings.value('timezones', '{}'))

        """
        Подключение основных кнопок
        """
        self.add_time.clicked.connect(self.add_new_time_zone)
        self.profil_button.clicked.connect(self.view_profile)


        """
        Позиционирование всех элементов
        """
        self.custom_layout = CustomLayoutMainWidget()
        self.central_widget = self.custom_layout.setup_main_layout()
        self.setCentralWidget(self.central_widget)
        self.custom_layout.button_layout_home_nav.addWidget(self.profil_button, 0, 0)
        self.custom_layout.button_layout_home_nav.addWidget(self.add_time, 0,   1)
        self.create_widget()


        """
        Первые попытки настроить нормальные стек виджетов
        """
        self.stacked_widget = QStackedWidget()

        self.add_time_zone = AddTimeZone(self.time_zone)
        self.profle = MyProfile(self)
        self.create_clock = CreateClock(self)
        self.view_profile = ViewTaskFriend(self)
        self.view_request = ViewRequest(self)

        self.stacked_widget.addWidget(self.central_widget)
        self.stacked_widget.addWidget(self.add_time_zone)
        self.stacked_widget.addWidget(self.profle)
        self.stacked_widget.addWidget(self.create_clock)
        self.stacked_widget.addWidget(self.view_profile)
        self.stacked_widget.addWidget(self.view_request)


        self.setCentralWidget(self.stacked_widget)
        self.add_time_zone.main_widget_button.clicked.connect(self.home)
        self.view_profile.home_button.clicked.connect(lambda x: self.home(index_page=2))
        self.add_time_zone.save_widget_button.clicked.connect(self.save_update_main)
        self.profle.home_button.clicked.connect(self.home)
        self.create_clock.home_button.clicked.connect(lambda x: self.home(index_page=2))
        self.view_request.home_button.clicked.connect(lambda x: self.home(index_page=2))
        '''
        Первые попытки сделать таймер, для обновления виджетов
        '''
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_main_views)
        self.timer.start(10000)


        self._audio_output = QtMultimedia.QAudioOutput()
        self._player = QtMultimedia.QMediaPlayer()
        self._player.setAudioOutput(self._audio_output)
        self._audio_output.setVolume(100)
        self.play_melodiy(resource_path('project/draw/start_app.mp3'))

    def play_melodiy(self, filename):
        media = QUrl.fromLocalFile(filename)
        self._player.setSource(media)
        self._player.play()

    
    def update_main_views(self):
        self.delete_widget_timezone()
        self.create_widget()

    def save_update_main(self):
        # сохраняем  и перезаписываем часовые пояса
        self.stacked_widget.setCurrentIndex(0)
        self.time_zone = json.loads(self.settings.value('timezones', '{}'))
        # вызываем функцию обновления экрана
        self.update_main_views()
        print(self.time_zone)
    
    def home(self, index_page=0):
        # Перемещение на главный экран
        self.stacked_widget.setCurrentIndex(index_page)


    def add_new_time_zone(self):
        # Добавление новых элементов часовых поясов
        self.stacked_widget.setCurrentIndex(1)

    def view_profile(self):
        self.stacked_widget.setCurrentIndex(2)

    def create_widget(self):
        x, y = 0, 0
        for key, values in self.time_zone.items():
            offset_hours, offset_minutes = map(str, values.split(':'))
            new_hour = eval(f"{datetime.now().hour} + {max(offset_hours, self.formatted_offset_h)} - {min(offset_hours, self.formatted_offset_h)} ")
            new_minute =  eval(f" {datetime.now().minute} + {max(offset_minutes, self.formatted_offset_m)} - {min(offset_minutes, self.formatted_offset_m)}")
            if int(new_hour) < 0:
                new_hour = 24 + new_hour 
            elif int(new_hour) >= 24:
                new_hour -= 24
            if new_minute >= 60:
                new_hour += new_minute // 60
                new_minute = new_minute % 60
            elif new_minute < 0:
                new_hour -= 1
                new_minute = 60 + new_minute
            if len(str(new_minute)) == 1:
                new_minute = str(f'0{new_minute}')
                
            a = custom_widget.CustomRiecent()
            a.set_time(str(new_hour), new_minute, key)
            a.setFixedSize(200, 100) 
            self.custom_layout.grid_layout.addWidget(a, y, x)
            x += 1
            if x > 4:
                x, y = 0, y + 1
        self.update()
        print('widget_update')
        self.statusBar().showMessage('Поле обновлено успешно', 40000)

    def delete_widget_timezone(self):
        while self.custom_layout.grid_layout.count():
            item = self.custom_layout.grid_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        print('Виджет успшено удален')
        


