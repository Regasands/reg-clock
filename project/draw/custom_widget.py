from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPainter, QPen, QFont, QColor
from PyQt6.QtCore import Qt, QRectF


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
    

if __name__ == "__main__":
    app = QApplication([])
    window = CustomRiecent()
    window.show()
    app.exec()