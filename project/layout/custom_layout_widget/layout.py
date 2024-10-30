from PyQt6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QScrollArea
from PyQt6.QtCore import Qt


class ParentLayout:
    '''
    Т.к логика приложения предполагает , что оконки меню и навигации будут снизу, то я решил сделать  родительский элемент для них
    '''
    def __init__(self):
        self.button_layout_home_nav = self.create_grid_button_add()

    def create_grid_button_add(self):
        button_box_layout = QGridLayout()
        button_box_layout.setHorizontalSpacing(50)
        button_box_layout.setVerticalSpacing(20)
        button_box_layout.setContentsMargins(10, 30, 50, 20)
        button_box_layout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
        return button_box_layout


class CustomLayoutMainWidget(ParentLayout):
    '''
    Использую отдельную логику для размещения элементов 
    '''
    def __init__(self):
        super().__init__()
        self.grid_layout = self.create_grid_layout()

    def create_grid_layout(self):
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(10)
        grid_layout.setVerticalSpacing(40)
        grid_layout.setContentsMargins(40, 40, 40, 40)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        return grid_layout

    def setup_main_layout(self):
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.grid_layout)
        main_layout.addLayout(self.button_layout_home_nav)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        return central_widget


class CustomLayoutAddTimeZone(ParentLayout):
    '''
    Расположение временных зон для окна диалога AddTimeZone
    '''
    def __init__(self):
        super().__init__()
        self.scrol = QScrollArea()
        self.inner_layout = self.create_inner_layout()

    def create_inner_layout(self):
        inner_layout = QGridLayout()
        inner_layout.setHorizontalSpacing(5)
        inner_layout.setVerticalSpacing(10)
        inner_layout.setContentsMargins(10, 10, 10, 10)
        return inner_layout

    def setup_main_layout(self):
        widget = QWidget()
        widget.setStyleSheet('border: 1px solid black')
        widget.setLayout(self.inner_layout)
        self.scrol.setWidgetResizable(True)
        self.scrol.setWidget(widget)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.scrol)
        main_layout.addLayout(self.button_layout_home_nav)
        return main_layout


        
        