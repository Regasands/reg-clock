import psycopg2
import sys
from datetime import datetime, timedelta

import database
from PyQt6.QtWidgets import QWidget, QApplication, QCalendarWidget, QLabel
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
            a.setFixedSize(600, 100) 
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
            except Exception as e:
                print('r')
                print(e)
            
        # self.choose_date = self.findChild(QCalendarWidget, "choose_date")
        # self.dateLabel = self.findChild(QLabel, "dateLabel")

    # def update_date_label(self):
    #     selected_date = self.choose_date.selectedDate().toString("yyyy-MM-dd")
    #     self.dateLabel.setText(f"Selected Date: {selected_date}")


        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyProfile()
    ex.show()
    sys.exit(app.exec())
    ex.db.exit()