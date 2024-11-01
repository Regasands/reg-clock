import psycopg2
from datetime import datetime, timezone
from config.const import DataBd


class DatabaseConnection:
    '''
    Основной класс для подключения и работы с бд
    '''
    def __init__(self, login, password):
        self.conn = None
        self.login = login
        self.password = password

    def check_profile(self):
        query = f'''
            SELECT password FROM users WHERE login = '{self.login}'
            '''
        self.cursor.execute(query)
        try:
            result = self.cursor.fetchone()[0]
            if result == self.password:
                return True
        except TypeError as e:
            raise TypeError('Данные не верны, такого пользователя не существует')
        raise TypeError('Данные не верны, пароль не верный, в подключение отказано')
        
    def conect(self):
        try:
            self.conn =  psycopg2.connect(
                dbname = DataBd.DBNAME,
                user = DataBd.USER,
                password = DataBd.PASSWORD,
                host = DataBd.HOST,
                port = DataBd.PORT,
            )
            self.cursor = self.conn.cursor()
            if self.check_profile():
                    print("Подключение к базе данных успешно")
                    return True

        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Ошибка подключения к базе данных: {e}")

    def get_request (self, query=None):
        query = f'''
        SELECT alarm_clock_date, alarm_clock_name, user_own FROM alarm_clock WHERE user_own = '{self.login}'
        '''
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except psycopg2.Error as e:
            print(e)
    
    def set_request(self, date: datetime, query=None, date_name=None):
        query = f'''
        INSERT INTO alarm_clock (user_own, alarm_clock_date, alarm_clock_name) VALUES ('{self.login}', '{date}', '{date_name}')
        '''
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except psycopg2.Error as e:
            print(e)
            self.conn.rollback()
            return False

    def disconect(self):
        try:
            self.conn.close()
            self.cursor.close()
            print('Успешное отключение базы данных')
            return True
        except psycopg2.Error as e:
            print(e)
            return False


class DatabaseUser:
    def __init__(self):
        self.con = psycopg2.connect(
            dbname = DataBd.DBNAME,
            user = DataBd.USER,
            password = DataBd.PASSWORD,
            host = DataBd.HOST,
            port = DataBd.PORT,
        )
        self.cur = self.con.cursor()

    def create_user(self, login, password):
        query = '''INSERT INTO users(login, password) VALUES (%s, %s)'''
        try:
            self.cur.execute(query, (str(login), str(password), ))
            self.con.commit()
            return True
        except Exception as e:
            print(e)
            return False