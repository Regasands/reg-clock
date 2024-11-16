import psycopg2
import sys
from datetime import datetime, timedelta

import database
from PyQt6.QtWidgets import QWidget, QApplication, QCalendarWidget, QLabel, QTableWidgetItem
from PyQt6.QtWidgets import QMessageBox, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6 import uic


from config.const import *
from project.layout.custom_layout_widget.layout import CustomLayoutProfile, CustomLayotRequest
from project.draw.custom_widget import TaskWidget, ViewSoloRequest, ViewYouRequest


class MyProfile(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi('project/Layout/ui/profile.ui', self)
        self.parent = parent
        self.db = self.parent.db if self.parent.db else None

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
        self.view_tasks_update()
        '''Обработка событий кнопки'''
        self.add_clock_button.clicked.connect(self.create_new_clock)
        self.view_friends_button.clicked.connect(self.view_friend)
        self.check_request_button.clicked.connect(self.check_request)

    def view_friend(self):
        self.parent.stacked_widget.setCurrentIndex(4)

    def check_request(self):
        self.parent.stacked_widget.setCurrentIndex(5)

    def create_new_clock(self):
        self.parent.stacked_widget.setCurrentIndex(3)

    def view_tasks_update(self):
        '''Уже сложно все держать в голове...'''
        while self.custom_layout.inner_layout.count():
            item = self.custom_layout.inner_layout.takeAt(0)
            inner_layout = item.widget()
            if inner_layout is not None:
                inner_layout.deleteLater()
        db_id = self.db.id_user
        self.db.cursor.execute(f'''SELECT * FROM alarm_clock WHERE user_own = {db_id}''')
        res = self.db.cursor.fetchall()
        for i, e in enumerate(res):
            a = TaskWidget(self.db, db_id, str(e[1]), e[2], e[3], e[4], self)
            a.setStyleSheet("margin: 0px; padding: 0px;")
            self.custom_layout.inner_layout.addWidget(a)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_F5:
            self.view_tasks_update()
            self.update()

    
class CreateClock(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.db = self.parent.db if self.parent.db else None
        uic.loadUi('project/Layout/ui/create_clock.ui', self)
        self.create_button.clicked.connect(self.save_button_event)

    def save_button_event(self):
        name = self.choose_topic.text()
        descriptions = self.choose_text.toPlainText()
        date = self.choose_date.selectedDate().toPyDate()
        time = self.choose_time.time().toPyTime()
        unical = True if self.choose_unical.currentText() == 'View friends' else False
        dates = datetime.combine(date, time)
        if dates >= datetime.now():
            try:
                self.db.set_alarm_clock(dates, descriptions, name, unical)
                self.parent.stacked_widget.setCurrentIndex(2)

            except Execption as e:
                print(e)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return:
            self.save_button_event()
            self.parent.stacked_widget.setCurrentIndex(2)
        super().keyPressEvent(event)

class ViewTaskFriend(QWidget):
    '''
    Виджет для отображения друзей и  их заданий
    '''
    def __init__(self,  parent):
        super().__init__()
        uic.loadUi('project/Layout/ui/taskfriend.ui', self)
        self.db = parent.db
        self.parent = parent
        self.login.setText(self.db.login)
        self.login.setEnabled(False)
        self.password.setText(self.db.password)
        self.password.setEnabled(False)
        self.combo_sp = ['Все'] + list(map(lambda x: x[0], self.db.get_friends()))
        self.fiend_user.addItems(self.combo_sp)
        self.create_update_table(True)
        self.fiend_user.currentTextChanged.connect(self.changed_table)
        self.leaveprof.clicked.connect(self.leave_prof)

    def changed_table(self):
        self.create_update_table()

    def create_update_table(self, need_update=False):
        '''need update - нужен из-за того, что currentTextChanged вызывается бесконечно, а значит программа, может принять за рекурсию это деяние'''
        self.tableWidget.setRowCount(0)
        log_n = self.fiend_user.currentText()
        self.combo_sp = ['Все'] + list(map(lambda x: x[0], self.db.get_friends()))
        if need_update:
            self.fiend_user.clear()
            self.fiend_user.addItems(self.combo_sp)
            self.fiend_user.setCurrentText(log_n)
        try:
            if log_n == 'Все':
                x = tuple(self.combo_sp[1:])
                if x:
                    query = '''SELECT users.login, alarm_clock.topic, alarm_clock.alarm_clock_date, alarm_clock.alarm_clock_name
                    FROM users INNER JOIN alarm_clock on  users.id = alarm_clock.user_own WHERE users.login IN %s AND alarm_clock.unical = TRUE'''
                    self.db.cursor.execute(query, (x,))
            else:
                query = f'''SELECT users.login, alarm_clock.topic, alarm_clock.alarm_clock_date, alarm_clock.alarm_clock_name
                FROM users INNER JOIN alarm_clock on  users.id = alarm_clock.user_own WHERE users.login = '{log_n}' AND alarm_clock.unical = TRUE'''
                self.db.cursor.execute(query)
            res = self.db.cursor.fetchall()
        except Exception as e:
            res = []
            print(e)
        self.tableWidget.setRowCount(len(res))
        for i, e in enumerate(res):
            for j, e_2 in enumerate(e):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(e_2)))

    def leave_prof(self):
        setting = self.parent.settings
        setting.setValue('username', None)
        setting.setValue('password', None)
        sys.exit()


class ViewRequest(QWidget):
    '''
    Класс для отображения запросов как пользователя, так и отправленных пользователем
    '''
    def __init__(self, parent):
        super().__init__()
        uic.loadUi('project/layout/ui/request_user.ui', self)
        self.db = parent.db
        self.parent = parent
        self.customLayout = CustomLayotRequest(self)
        main_layout = self.customLayout.setup_main_layout()
        self.setLayout(main_layout)
        self.update_tome_request()
        self.update_forme_request()
        self.search.clicked.connect(self.get_login_for_request)
        self.push_request.clicked.connect(self.push_requests)
    
    def update_forme_request(self):
        '''
        Запросы которые прислал пользователь
        '''
        while self.customLayout.in_2.count():
            item = self.customLayout.in_2.takeAt(0)
            inner_layout = item.widget()
            if inner_layout is not None:
                inner_layout.deleteLater()
        query = '''SELECT DISTINCT users.login FROM request INNER JOIN users ON request.friend_id = users.id WHERE request.user_id = %s'''
        try:
            self.db.cursor.execute(query, (self.db.id_user, ))
            res = self.db.cursor.fetchall()
            for e in res:
                a = ViewYouRequest(self, e[0])
                self.customLayout.in_2.addWidget(a)
        except Exception as e:
            print(e)


    def update_tome_request(self):
        '''
        Обработка запросов, направленная на меня
        '''
        while self.customLayout.in_1.count():
            item = self.customLayout.in_1.takeAt(0)
            inner_layout = item.widget()
            if inner_layout is not None:
                inner_layout.deleteLater()
        query = '''SELECT DISTINCT users.login FROM request INNER JOIN users ON request.user_id = users.id WHERE request.friend_id = %s'''
        try:
            self.db.cursor.execute(query, (self.db.id_user, ))
            res = self.db.cursor.fetchall()
            for e in res:
                a = ViewSoloRequest(self, e[0])
                self.customLayout.in_1.addWidget(a)
        except Exception as e:
            print(e)

    def accept_or_del_request(self, text, bools_d, bools_you):
        '''Обработка правильности запроса в друзья'''
        try:
            self.db.cursor.execute(f'''SELECT id FROM users WHERE login = '{text}' ''')
            id_friend = self.db.cursor.fetchone()[0]
            if bools_d:
                query = '''DELETE FROM request WHERE user_id = %s and friend_id = %s'''
                if bools_you:
                    print(id_friend, self.db.id_user)
                    self.db.cursor.execute(query, (id_friend, self.db.id_user))
                else:
                    self.db.cursor.execute(query, (self.db.id_user, id_friend))
                self.db.conn.commit()
            else:
                query = '''INSERT INTO friends(user_id, friend_id) VALUES(%s, %s)'''
                self.db.cursor.execute(query, (self.db.id_user, id_friend))
                self.db.conn.commit()
            self.update_forme_request()
            self.update_tome_request()
            self.parent.view_profile.create_update_table(True)
        except Exception as e:
            print(e)
            
    def get_login_for_request(self):
        def f(text_error):
            e = QMessageBox()
            e.setText(text_error)
            e.setWindowTitle('Error')
            e.exec()

        try:
            text = self.lineEdit.text()
            print(text)
            if text == '' or len(text) > 15:
                raise TooLongValue

            querry = '''SELECT * FROM friends INNER JOIN users on friends.friend_id = users.id WHERE friends.user_id = %s and users.login = %s'''

            self.db.cursor.execute(querry, (self.db.id_user, str(text)))
            res = self.db.cursor.fetchall()

            if res:
                raise YouHaveThisFriend

            querry = '''SELECT * FROM users WHERE login = %s'''
            self.db.cursor.execute(querry, (text, ))
            res = self.db.cursor.fetchall()

            if not res:
                raise BdDontHaveThisUser

            if res[0][1] == self.db.login:
                raise ThisYourLogin
            querry = '''SELECT * FROM request INNER JOIN users on request.friend_id = users.id WHERE request.user_id = %s and users.login = %s'''
            self.db.cursor.execute(querry, (self.db.id_user, text))
            res = self.db.cursor.fetchall()
            if res:
                raise YouHaveThisRequest
                
            self.push_request.setEnabled(True)
            
        except TooLongValue:
            f('Пожалуйста введите реальные данные')

        except YouHaveThisFriend as e:
            f('Этот юезер уже у тебя в друзьях!!')

        except BdDontHaveThisUser as e:
            f('Такого пользователя нет!!')

        except YouHaveThisRequest:
            f('Не сапамь запросами!!!!')

        except ThisYourLogin:
            f('Это твой логин!')

        except Exception as e:
            f(f"Незивестная ошибка {e}")

    def push_requests(self):
        text = self.lineEdit.text()
        query = '''INSERT INTO request(user_id, friend_id) VALUES(%s, %s)'''
        try:
            self.db.cursor.execute(f'''SELECT id FROM users WHERE login = '{text}' ''')
            res = self.db.cursor.fetchone()[0]
            self.db.cursor.execute(query, (self.db.id_user, res))
            self.db.conn.commit()
        except Exception as e:
            print(e)
            print('here')
        self.update_forme_request()
        self.push_request.setEnabled(False)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return:
            self.update_tome_request()
            self.update_forme_request()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ViewTaskFriend('E')
    window.show()
    sys.exit(app.exec())