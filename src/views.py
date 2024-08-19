import datetime


def greeting():
    """Функция вывода сообщения приветствия в зависимости от времени суток"""
    opts = {"greeting": ('доброе утро', 'добрый день', 'добрый вечер', 'доброй ночи')}
    current_time = datetime.datetime.now()
    if current_time.hour >= 4 and current_time.hour <= 12:
        greet = opts['greeting'][0]
    elif current_time.hour >= 12 and current_time.hour <= 16:
        greet = opts['greeting'][1]
    elif current_time.hour >= 16 and current_time.hour <= 24:
        greet = opts['greeting'][2]
    else:
        greet = opts['greeting'][3]
    print(greet)