def check_data(self, func):
    def wrappers(*args, **kwargs):
        if self.conn is None or self.login is None:
            raise ValueError('Ошибка, даннные не могут быть None')
        return func(*args, **kwargs)
    return wrappers


def format_date(date: str) -> str:
    sp = []
    if date[0] == '-' or date[0] == '+':
        sp.append(date[0])
        date = date[1:]
    if date[0] == '0':
        date = date[1:]
    sp.append(date)
    return ' '.join(sp)
    
