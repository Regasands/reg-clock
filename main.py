import sys
from project.main_page import CustomApplication, MainWindow
import time

if __name__ == '__main__':
    try:
        app = CustomApplication(sys.argv)
        ex = MainWindow(app.db, app.login)
        ex.show()
        sys.exit(app.exec())
        ex.db.exit()
    except Exception as e:
        print(e)
        time.sleep(100)