import psycopg2


def connect_to_bd():
    try:
        con = psycopg2.connect(
            dbname = DataBd.DBNAME,
            user = DataBd.USER,
            password = DataBd.PASSWORD,
            host = DataBd.HOST,
            port = DataBd.PORT,
        )
        return con
    except Exception as e:
        print(e)


def create_table(cursor, number):
    if number == 1:
        query = '''
        CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        login VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(20) NOT NULL
        );
        '''
    elif number == 2:
        query = '''
        CREATE TABLE alarm_clock(
        user_own VARCHAR(100) NOT NULL,
        FOREIGN KEY (user_own) REFERENCES users (login) ON DELETE SET NULL,
        alarm_clock_date TIMESTAMP NOT NULL,
        alarm_clock_name VARCHAR(255)
        );
        '''
    elif number == 3:
        query = '''
        CREATE TABLE friends(
        user_id INT REFERENCES users(id) ON DELETE CASCADE,
        friend_id INT REFERENCES users(id) ON DELETE CASCADE,
        PRIMARY KEY (user_id, friend_id),
        CHECK (user_id != friend_id))
        '''
    elif number == 4:
        query = '''
        CREATE TABLE request(
        user_id INT REFERENCES users(id) ON DELETE CASCADE,
        friend_id INT REFERENCES users(id) ON DELETE CASCADE,
        PRIMARY KEY (user_id, friend_id),
        CHECK (user_id != friend_id))
        '''
    else:
        raise ValueError('Переданы не правильные параметры')
    cursor.execute(query)
    print('Таблица успешно создана')


# def create_table_for_time_zone(cursor):
#     query = '''
#         CREATE TABLE timezone(
#         id SERIAL PRIMARY KEY,
#         name_zone VARCHAR(100),
#         time_zone_h VARCHAR(3),
#         time_zone_m VARCHAR(3))
#         '''
#     cursor.execute(query)
#     print('Таблица успешно создана')




con = connect_to_bd()
cursor = con.cursor()
create_table(cursor, 4)
# create_table_for_time_zone(cursor)
con.commit()
# print('not error')