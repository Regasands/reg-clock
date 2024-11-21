import csv
import os
import sys

class Constant:
    PASSWORD = ''

# class QuerySet:
#     QUERY_BD = {
#         'get_alarm': '''SELECT''',
#     }

class TimeZone:
    ALLTIMEZONE = {}
    def get_resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)
    file_path = get_resource_path('config/all_timezones.csv')
    with open(file_path,  'r', encoding='utf-8') as f:
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