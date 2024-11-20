import csv


class Constant:
    PASSWORD = ''

# class QuerySet:
#     QUERY_BD = {
#         'get_alarm': '''SELECT''',
#     }
class TimeZone:
    ALLTIMEZONE = {}
    with open('all_timezones.csv', 'r', encoding='utf-8') as f:
        file = csv.reader(f)
        next(file)  # Пропускаем строку с заголовками
        for row in file:
            location, timezone = row
            ALLTIMEZONE[location] = timezone


class DataBd:
    DBNAME = "clock"
    USER = 'postgres'
    PASSWORD = 'reg_clock2308'
    HOST = '194.87.102.160'
    PORT = '5432'


class TooLongValue(Exception):
    pass


class YouHaveThisFriend(Exception):
    pass


class BdDontHaveThisUser(Exception):
    pass


class YouHaveThisRequest(Exception):
    pass


class ThisYourLogin(Exception):
    pass