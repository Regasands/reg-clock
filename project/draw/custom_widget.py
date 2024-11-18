import sys


from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QApplication, QGridLayout, QHBoxLayout, QVBoxLayout, QMessageBox
from PyQt6.QtGui import QPainter, QPen, QFont, QColor, QIcon
from PyQt6.QtCore import Qt, QRectF, QSize



class CustomRiecent(QWidget):
    '''
    Класс создания кастомного виджета для отрисовки кнопок
    '''
    def __init__(self):
        super().__init__()
        self.setMinimumSize(200, 80)
        self.time_h = '00'
        self.time_m = '00'
        self.name = ''

    def set_time(self, time_h, time_m, name):
        self.time_h = time_h
        self.time_m = time_m
        self.name = name

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(QColor(0, 0, 0))
        pen.setWidth(2)
        painter.setPen(pen)
        square = QRectF(5, 5, 140, 40)
        font = QFont()
        font.setPointSize(15)
        painter.setFont(font)
        painter.drawRoundedRect(square, 10, 10)
        painter.drawText(square, Qt.AlignmentFlag.AlignCenter, f"{self.time_h} : {self.time_m}")
        sub_text = QRectF(5, 50, 200, 30)
        if len(self.name) > 13:
            self.name = self.name[:12] + '...'
        painter.drawText(sub_text, Qt.AlignmentFlag.AlignLeft, f'{self.name}' )
    

class TaskWidget(QWidget):
    '''
    Отображение твоих заданий
    '''
    def __init__(self, db, id, date, name, unical, topic, parent):
        super().__init__()
        uic.loadUi('project/Layout/ui/task.ui', self)
        self.db = db
        self.parent = parent
        self.tp = topic
        self.topicLabel.setText(topic)
        self.topicLabel.adjustSize()
        self.dateLabel.setText(str(date))
        self.adjustSize()
        self.descriptionEdit.setPlainText(str(name))
        self.descriptionEdit.setEnabled(False)
        self.pushButton.clicked.connect(self.add_show)
        self.check_description.clicked.connect(self.check_descriptionn)

    def add_show(self):
        try:
            self.db.cursor.execute(f'''DELETE FROM alarm_clock WHERE user_own = {self.db.id_user} and topic = '{self.tp}' ''')
            self.db.conn.commit()
            self.parent.view_tasks_update()

        except Exception as e:
            print(e)

    def check_descriptionn(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        t = self.descriptionEdit.toPlainText()
        for i in range(1, len(t) // 70):
            t = t[i * 70:] + '\n' +  t[i * 70 + 1:] 
        msg.setText(t)
        msg.setWindowTitle("Информация")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()


class ViewSoloRequest(QWidget):
    def __init__(self, parent, text):
        super().__init__()
        uic.loadUi('project/layout/ui/request.ui', self)
        icon_rej = QIcon('project/draw/svg/reject.png')
        icon_add = QIcon('project/draw/svg/add.png')
        self.img_b.setIcon(icon_rej)
        self.img_b.setIconSize(QSize(64, 64))
        self.img_b2.setIcon(icon_add)
        self.img_b2.setIconSize(QSize(25, 25))
        self.img_b.clicked.connect(self.reject)
        self.img_b2.clicked.connect(self.secses)
        self.label.setText(text)
        self.text = text
        self.label.adjustSize()
        self.parent = parent

    def secses(self):
        self.parent.accept_or_del_request(self.text, False, True)
        self.parent.accept_or_del_request(self.text, True, True)


    def reject(self):
        self.parent.accept_or_del_request(self.text, True, True)


class ViewYouRequest(QWidget):
    '''Отображенрие всех запросов которые относятся к пользователю 
'''
    def __init__(self, parent, text):
        super().__init__()
        uic.loadUi('project/layout/ui/request_your.ui', self)
        icon_rej = QIcon('project/draw/svg/reject.png')
        self.img_b.setIcon(icon_rej)
        self.img_b.setIconSize(QSize(64, 64))
        self.img_b.clicked.connect(self.reject) 
        self.label.setText(text)
        self.text = text
        self.label.adjustSize()
        self.parent = parent
    
    def reject(self):
        self.parent.accept_or_del_request(self.text, True, False)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ViewYouRequest('3wew3gvrijkoevbwvrdvmdvskvdskdvsjkdvsljvklavdsjvskjn kvqjvqvediopcd', 'l')
    window.show()
    sys.exit(app.exec())