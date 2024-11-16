class Constant:
    PASSWORD = ''

# class QuerySet:
#     QUERY_BD = {
#         'get_alarm': '''SELECT''',
#     }

class TimeZone:
    ALLTIMEZONE = {
        "Россия/Москва": "+3:00",
        "США/Вашингтон": "-5:00",
        "Канада/Оттава": "-5:00",
        "Великобритания/Лондон": "+0:00",
        "Франция/Париж": "+1:00",
        "Германия/Берлин": "+1:00",
        "Италия/Рим": "+1:00",
        "Испания/Мадрид": "+1:00",
        "Китай/Пекин": "+8:00",
        "Япония/Токио": "+9:00",
        "Южная Корея/Сеул": "+9:00",
        "Индия/Нью-Дели": "+5:30",
        "Бразилия/Бразилиа": "-3:00",
        "Аргентина/Буэнос-Айрес": "-3:00",
        "Австралия/Канберра": "+10:00",
        "Новая Зеландия/Веллингтон": "+12:00",
        "ЮАР/Претория": "+2:00",
        "Египет/Каир": "+2:00",
        "Саудовская Аравия/Эр-Рияд": "+3:00",
        "Турция/Анкара": "+3:00",
        "ОАЭ/Дубай": "+4:00",
        "Иран/Тегеран": "+3:30",
        "Вьетнам/Ханой": "+7:00",
        "Таиланд/Бангкок": "+7:00",
        "Индонезия/Джакарта": "+7:00",
        "Филиппины/Манила": "+8:00",
        "Пакистан/Исламабад": "+5:00",
        "Россия/Санкт-Петербург": "+3:00",
        "Россия/Новосибирск": "+7:00",
        "Россия/Екатеринбург": "+5:00",
        "Россия/Казань": "+3:00",
        "Россия/Нижний Новгород": "+3:00",
        "Россия/Челябинск": "+5:00",
        "Россия/Омск": "+6:00",
        "Россия/Самара": "+4:00",
        "Россия/Ростов-на-Дону": "+3:00",
        "Россия/Уфа": "+5:00",
        "Россия/Красноярск": "+7:00",
        "Россия/Воронеж": "+3:00",
        "Россия/Пермь": "+5:00",
        "Россия/Волгоград": "+3:00",
        "Россия/Краснодар": "+3:00",
        "Россия/Тюмень": "+5:00",
        "Россия/Иркутск": "+8:00",
        "Россия/Хабаровск": "+10:00",
        "Россия/Владивосток": "+10:00",
        "Россия/Якутск": "+9:00",
        "Россия/Саратов": "+3:00",
        "Россия/Тольятти": "+4:00",
        "Россия/Барнаул": "+7:00",
        "Россия/Ижевск": "+4:00",
        "Россия/Ульяновск": "+4:00",
        "Россия/Липецк": "+3:00",
        "Россия/Кемерово": "+7:00",
        "Россия/Томск": "+7:00",
        "Мексика/Мехико": "-6:00",
        "США/Нью-Йорк": "-5:00",
        "США/Лос-Анджелес": "-8:00",
        "США/Чикаго": "-6:00",
        "США/Денвер": "-7:00",
        "Бразилия/Сан-Паулу": "-3:00",
        "Бразилия/Рио-де-Жанейро": "-3:00",
        "Аргентина/Кордова": "-3:00",
        "Чили/Сантьяго": "-3:00",
        "Колумбия/Богота": "-5:00",
        "Перу/Лима": "-5:00",
        "Венесуэла/Каракас": "-4:00",
        "Уругвай/Монтевидео": "-3:00",
        "Эквадор/Кито": "-5:00",
        "Парагвай/Асунсьон": "-4:00",
        "Индонезия/Бали": "+8:00",
        "Индонезия/Сурабая": "+7:00",
        "Сингапур/Сингапур": "+8:00",
        "Малайзия/Куала-Лумпур": "+8:00",
        "Мьянма/Янгон": "+6:30",
        "Бангладеш/Дакка": "+6:00",
        "Шри-Ланка/Коломбо": "+5:30",
        "Пакистан/Карачи": "+5:00",
        "Непал/Катманду": "+5:45",
        "Иран/Мешхед": "+3:30",
        "Израиль/Иерусалим": "+2:00",
        "Турция/Стамбул": "+3:00",
        "Греция/Афины": "+2:00",
        "Норвегия/Осло": "+1:00",
        "Швеция/Стокгольм": "+1:00",
        "Дания/Копенгаген": "+1:00",
        "Нидерланды/Амстердам": "+1:00",
        "Бельгия/Брюссель": "+1:00",
        "Швейцария/Цюрих": "+1:00",
        "Австрия/Вена": "+1:00",
        "Португалия/Лиссабон": "+0:00",
        "Ирландия/Дублин": "+0:00",
        "Финляндия/Хельсинки": "+2:00",
        "Польша/Варшава": "+1:00",
        "Чехия/Прага": "+1:00",
        "Словакия/Братислава": "+1:00",
        "Венгрия/Будапешт": "+1:00",
        "Сербия/Белград": "+1:00",
        "Румыния/Бухарест": "+2:00",
        "Болгария/София": "+2:00",
        "ЮАР/Кейптаун": "+2:00",
        "Марокко/Рабат": "+0:00",
        "Нигерия/Лагос": "+1:00",
        "Кения/Найроби": "+3:00",
        "Танзания/Дар-эс-Салам": "+3:00",
        "Египет/Александрия": "+2:00",
        "Алжир/Алжир": "+1:00",
        "Гана/Аккра": "+0:00",
        "США/Финикс": "-7:00",
        "Канада/Ванкувер": "-8:00",
        "Канада/Монреаль": "-5:00",
        "Китай/Шанхай": "+8:00",
        "Китай/Гуанчжоу": "+8:00",
        "Австралия/Сидней": "+10:00",
        "Австралия/Мельбурн": "+10:00",
        "Австралия/Брисбен": "+10:00",
        "Австралия/Перт": "+8:00",
        "Филиппины/Себу": "+8:00"
    }


class DataBd:
    DBNAME = "clock"
    USER = 'postgres'
    PASSWORD = '92349234Regqwe!'
    HOST = 'localhost'
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