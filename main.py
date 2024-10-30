import sys
from project.main_page import CustomApplication, MainWindow

if __name__ == '__main__':
    app = CustomApplication(sys.argv)
    ex = MainWindow(app.db, app.login)
    ex.show()
    sys.exit(app.exec())
    ex.db.exit()