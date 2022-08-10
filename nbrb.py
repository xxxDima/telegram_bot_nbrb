import requests
from json import loads
import matplotlib.pyplot as plt
from datetime import timedelta
from datetime import date


def curse_per_week():
    x = []
    y = []
    y_usd = []
    data_days = -29

    for i in range(data_days, 2):
        data = str(date.today() + timedelta(i))  # дата за неделю + 1 день
        url = 'https://www.nbrb.by/api/exrates/rates/Cur_Abbreviation=EUR?ondate=' + data + '&Cur_ID=451'
        url_usd = 'https://www.nbrb.by/api/exrates/rates/Cur_Abbreviation=USD?ondate=' + data + '&Cur_ID=431'
        response_usd = requests.get(url_usd)
        response = requests.get(url)  # print(response) 200, если все ок

        if response.ok and response_usd.ok:
            response_text_usd = response_usd.text
            response_text = response.text  # текст дата, валюта, курс и т.д. type str
            dic_response_text_usd = loads(response_text_usd)
            dic_response_text = loads(response_text)  # response_text type str в type dict
            curs_response_usd = dic_response_text_usd['Cur_OfficialRate']
            curs_response = dic_response_text['Cur_OfficialRate']  # вывод курса евро в переменную type(float)
            y.append(curs_response)  # переводим значение курса в type(list)
            y_usd.append(curs_response_usd)
            slice_data = dic_response_text['Date']
            slice_data = slice_data[0:10]
            x.append(slice_data)  # вывод даты в переменную type(list)
        else:
            break

    eur = plt.subplot(2, 1, 1)
    plt.plot(x, y, '-ob')
    plt.legend(['Курс EUR'])
    eur.tick_params(pad=1,  # Расстояние между черточкой и ее подписью
                    labelsize=6,  # Размер подписи
                    labelcolor='b',  # Цвет подписи
                    labelrotation=60)  # Поворот подписей
    plt.subplots_adjust(hspace=0.4)

    usd = plt.subplot(2, 1, 2)
    plt.plot(x, y_usd, '-og')
    plt.legend(['Курс USD'])
    usd.tick_params(pad=1,  # Расстояние между черточкой и ее подписью
                    labelsize=6,  # Размер подписи
                    labelcolor='g',  # Цвет подписи
                    labelrotation=60)  # Поворот подписей

    eur.grid()
    usd.grid()
    plt.suptitle('Курсы валют EUR и USD по отношению к BYN')
    plt.savefig('Schedule.png')
    # plt.show()


# curse_per_week()
