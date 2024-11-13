import psycopg2
import sys
from datetime import datetime, timedelta

import database
from PyQt6.QtWidgets import QWidget, QApplication, QCalendarWidget, QLabel, QTableWidgetItem
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt
from PyQt6 import uic


from project.layout.custom_layout_widget.layout import CustomLayoutProfile
from project.draw.custom_widget import TaskWidget

class MyProfile(QWidget, CustomLayoutProfile):
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
        print('e')


        '''Обработка событий кнопки'''
        self.add_clock_button.clicked.connect(self.create_new_clock)
        self.view_friends_button.clicked.connect(self.view_friend)


    def view_friend(self):
        self.parent.stacked_widget.setCurrentIndex(4)

    def add_vidget(self):
        pass

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
            a.setFixedSize(500, 200) 
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
        # self.choose_date = self.findChild(QCalendarWidget, "choose_date")
        # self.dateLabel = self.findChild(QLabel, "dateLabel")

    # def update_date_label(self):
    #     selected_date = self.choose_date.selectedDate().toString("yyyy-MM-dd")
    #     self.dateLabel.setText(f"Selected Date: {selected_date}")




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
        print(self.combo_sp)
        self.fiend_user.addItems(self.combo_sp)
        self.create_update_table()
        self.fiend_user.currentTextChanged.connect(self.changed_table)
        self.leaveprof.clicked.connect(self.leave_prof)

    def changed_table(self):
        self.create_update_table()

    def create_update_table(self):
        self.tableWidget.setRowCount(0)
        self.combo_sp = ['Все'] + list(map(lambda x: x[0], self.db.get_friends()))
        log_n = self.fiend_user.currentText()
        try:
            if log_n == 'Все':
                x = tuple(self.combo_sp[1:])
                print(x)
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
        print(res)
        self.tableWidget.setRowCount(len(res))
        for i, e in enumerate(res):
            for j, e_2 in enumerate(e):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(e_2)))


    def leave_prof(self):
        setting = self.parent.settings
        setting.setValue('username', None)
        setting.setValue('password', None)
        sys.exit()
        


        
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ViewTaskFriend('E')
    window.show()
    sys.exit(app.exec())