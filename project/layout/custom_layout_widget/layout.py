from PyQt6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QScrollArea, QHBoxLayout
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
        self.scrol = QScrollArea()
        self.grid_layout = self.create_grid_layout()

    def create_grid_layout(self):
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(10)
        grid_layout.setVerticalSpacing(40)
        grid_layout.setContentsMargins(20, 20, 20, 20)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        return grid_layout

    def setup_main_layout(self):
        widget = QWidget()
        widget.setStyleSheet('border: 1px solid black')
        widget.setLayout(self.grid_layout)
        self.scrol.setWidgetResizable(True)
        self.scrol.setWidget(widget)
        main_layout = QVBoxLayout()
        self.scrol.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        main_layout.addWidget(self.scrol)
        main_layout.addLayout(self.button_layout_home_nav)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        central_widget.setFixedWidth(1200)
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


        
class CustomLayoutProfile(ParentLayout):
    def __init__(self):
        super().__init__()
        self.scrol = QScrollArea()
        self.inner_layout = self.create_inner_layout()
        self.layout_from_top_button = self.create_grid_button_add_top()

    def create_grid_button_add_top(self):
        button_box_layout = QGridLayout()
        button_box_layout.setHorizontalSpacing(50)
        button_box_layout.setVerticalSpacing(20)
        button_box_layout.setContentsMargins(10, 10, 10, 10)
        button_box_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        return button_box_layout

    def create_inner_layout(self):
        inner_layout = QVBoxLayout()
        return inner_layout

    def setup_main_layout(self):
        widget = QWidget()
        widget.setStyleSheet('border: 1px solid black')
        widget.setLayout(self.inner_layout)
        self.scrol.setWidgetResizable(True)
        self.scrol.setWidget(widget)
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.layout_from_top_button)
        main_layout.addWidget(self.scrol)
        main_layout.addLayout(self.button_layout_home_nav)
        return main_layout



class CustomLayotRequest:
    def __init__(self, parent):
        self.scrol_1 = parent.scrollArea

        self.scrol_2 = parent.scrollArea_2
        self.in_1 = self.create_inner_layout()
        self.in_2 = self.create_inner_layout()
        self.top = parent.gridLayout_2
        self.b = parent.home_button
        self.two_p = parent.gridLayout


    def create_inner_layout(self):
        inner_layout = QVBoxLayout()
        inner_layout.setContentsMargins(10, 10, 10, 10)
        return inner_layout
        

    def setup_main_layout(self):
        widget_1 = QWidget()
        widget_2 = QWidget()

        widget_1.setStyleSheet('border: 1px solid black')
        widget_1.setLayout(self.in_1)
        self.scrol_1.setWidget(widget_1)
        self.scrol_1.setWidgetResizable(True)
        widget_2.setStyleSheet('border: 1px solid black')
        widget_2.setLayout(self.in_2)
        self.scrol_2.setWidgetResizable(True)
        self.scrol_2.setWidget(widget_2)
        self.main_layout = QVBoxLayout()
        # self.main_layout.addLayout(self.top)
        # self.main_layout.addLayout(self.two_p)
        return self.main_layout
