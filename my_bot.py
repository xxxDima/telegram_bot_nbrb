import telebot
from bot_config import token
import nbrb
import requests
from mysql_config import *


bot = telebot.TeleBot(token)


def bot_id_and_name_user():
    """
    функция возвращает словарь с ключами 'chat_id' и 'name' юзера, который последний написал боту в л/с
    """
    response = requests.get(f'https://api.telegram.org/bot{token}/getupdates')
    dict_jsn = response.json()
    # преобразовали response в класс dict
    spis = dict_jsn['result']
    # вытянули вложеный список из словаря с ключем 'result' (1 итерация списка это 1 сообщение пользователя)
    #pprint(spis)
    for i in spis:
        if 'message' in i:
            # если есть ключ 'message' в списке сообщений от пользователя выводим ID и Имя пользователя
            chat_id = int(i['message']['from']['id'])  # int
            chat_name = i['message']['from']['first_name']  # str
        else:
            # если есть нет ключа 'message', пропускаем итерацию
            continue
    return dict(chat_id=chat_id, name=chat_name)


def db_add_users(result):
    """
    функция добавляет в БД юзеров которые написали боту в л/с, если такие отсутствуют в БД
    """
    try:
        connection = pymysql.connect(host=host,
                                     user=user,
                                     port=3306,
                                     password=password,
                                     database=database,
                                     charset=charset,
                                     cursorclass=cursorclass)
        print("connect... OK")

        try:
            with connection.cursor() as cursor:
                cursor.execute('select * from users;')
                rows = cursor.fetchall()
                print(rows)  # вывод в консоль список добавленых юзеров в базу данных
                for row in rows:
                    # если юзер, который написал боту существует в БД, тогда пропускаем. иначе добавляем его в БД
                    if row == result:
                        break
                    else:
                        cursor.execute('use test;')
                       # selec = cursor.execute('select * from users;')
                        cursor.execute(
                            f'insert into users (chat_id, name) values ({result["chat_id"]},'
                                       f' \'{result["name"]}\');'
                                       )  # добавляем запись в таблицу
                        connection.commit()  # метод для сохранения изменений
                        print("новый user успешно добавлен в  таблицу")

        finally:
            connection.close()
            print("connection close... OK")

    # Если ошибка в подключении, то выводим тип ошибки
    except Exception as ex:
        print("no connect...")
        print(ex)


def users_list_db():
    """
    возвращает список id добавленных в БД
    """
    chat_id = []
    try:
        connection = pymysql.connect(host=host,
                                     user=user,
                                     port=3306,
                                     password=password,
                                     database=database,
                                     charset=charset,
                                     cursorclass=cursorclass)
        try:
            with connection.cursor() as cursor:
                cursor.execute('select * from users;')
                rows = cursor.fetchall()
                for row_id in rows:
                    chat_id.append(row_id['chat_id'])
                # print(rows)  # вывод в консоль список добавленых юзеров в базу данных
        finally:
            connection.close()

    except Exception as ex:
        print("no connect...")
        print(ex)
    return chat_id


def answer(users_id):
    """
    функция отправляет сообщение от бота с графиком курса валют в л/с юзера
    """
    nbrb.curse_per_week()
    for user in users_id:
        photo = open('.\Schedule.png', 'rb')
        print(user)
        bot.send_photo(user, photo)


if __name__ == '__main__':
    answer(users_list_db())
