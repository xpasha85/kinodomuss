import random

import requests
import time
from datetime import datetime
from creds import CLIENTID, CLIENTSECRET, LOCKID, USERNAME, PASSWORD
import texts


def Refresh_token(clientId, clientSecret, refreshToken):
    data = {
        'clientId': clientId,
        'clientSecret': clientSecret,
        'grant_type': 'refresh_token',
        'refresh_token': refreshToken,
    }
    response = requests.post('https://euapi.ttlock.com/oauth2/token', data=data)
    r = response.json()
    access_token = r['access_token']
    refresh_token = r['refresh_token']
    expires_in = r['expires_in']
    return access_token, refresh_token, expires_in


def tokenize() -> str:
    data = {
        'clientId': CLIENTID,
        'clientSecret': CLIENTSECRET,
        'username': USERNAME,
        'password': PASSWORD,
    }
    response = requests.post('https://euapi.ttlock.com/oauth2/token', data=data)
    r = response.json()
    access_token = r['access_token']
    refresh_token = r['refresh_token']
    expires_in = r['expires_in']
    if expires_in <= 865.000:
        access_token, refresh_token, expires_in = Refresh_token(CLIENTID, CLIENTSECRET, refresh_token)
    return access_token


# def set_custom_pass(start_time: str, end_time: str, name: str, is_random=True, password='567434'):
#     """
#     :param is_random: Случайный парль из 4х цифр
#     :param start_time:  Дата в формате 29.10.2023 01:45
#     :param end_time: Дата в формате 29.10.2023 20:15
#     :param password: Пароль 4-9 символов
#     :param name: Название пароля
#     :return:
#     """
#     token = tokenize()
#     if is_random:
#         password = format(random.randint(0, 9999), '04d')
#     try:
#         start = round(datetime.strptime(start_time, '%d.%m.%Y %H:%M').timestamp() * 1000)
#     except ValueError:
#         return texts.ErrorUnpitDate
#     try:
#         end = round(datetime.strptime(end_time, '%d.%m.%Y %H:%M').timestamp() * 1000)
#     except ValueError:
#         return texts.ErrorUnpitDate
#
#     if not password.isdigit() or len(password) < 4:
#         return texts.ErrorPassword
#     now_date = round(time.time() * 1000)
#     data = {
#         'clientId': CLIENTID,
#         'accessToken': token,
#         'lockId': LOCKID,
#         'keyboardPwd': password,
#         'keyboardPwdName': name,
#         'startDate': start,
#         'endDate': end,
#         'addType': 2,
#         'date': now_date,
#     }
#     response = requests.post('https://euapi.ttlock.com/v3/keyboardPwd/add', data=data)
#     r = response.json()
#     if not r.get('keyboardPwdId') is None:
#         print(r.get('keyboardPwdId'))
#         return {
#             'status': 'ok',
#             'password': password
#         }
#     else:
#         return texts.ErrorGetPass


def set_custom_pass(start_time: datetime, end_time: datetime, name: str, is_random=True, password='567434'):
    """
    :param is_random: Случайный парль из 4х цифр
    :param start_time:  Дата в формате DateTime
    :param end_time: Дата в формате DateTime
    :param password: Пароль 4-9 символов
    :param name: Название пароля
    :return:
    """
    token = tokenize()
    if is_random:
        password = format(random.randint(0, 9999), '04d')
    try:
        start = round(start_time.timestamp() * 1000)
    except ValueError:
        return texts.ErrorUnpitDate
    try:
        end = round(end_time.timestamp() * 1000)
    except ValueError:
        return texts.ErrorUnpitDate

    if not password.isdigit() or len(password) < 4:
        return texts.ErrorPassword
    now_date = round(time.time() * 1000)
    data = {
        'clientId': CLIENTID,
        'accessToken': token,
        'lockId': LOCKID,
        'keyboardPwd': password,
        'keyboardPwdName': name,
        'startDate': start,
        'endDate': end,
        'addType': 2,
        'date': now_date,
    }
    response = requests.post('https://euapi.ttlock.com/v3/keyboardPwd/add', data=data)
    r = response.json()
    if not r.get('keyboardPwdId') is None:
        print(r.get('keyboardPwdId'))
        return {
            'status': 'ok',
            'password': password
        }
    else:
        return texts.ErrorGetPass

def del_one_pass(pass_id: str):
    token = tokenize()
    now_date = round(time.time() * 1000)
    data = {
        'clientId': CLIENTID,
        'accessToken': token,
        'lockId': LOCKID,
        'keyboardPwdId': pass_id,
        'deleteType': '2',
        'date': now_date,
    }
    response = requests.post('https://euapi.ttlock.com/v3/keyboardPwd/delete', data=data)
    return response.json()


# {'keyboardPwdId': 361936612}


def main():
    print(set_custom_pass('27.10.2023 11:24', '27.10.2023 16:32', 'Вася 5. Тест'))
    print(del_one_pass('361944756'))


if __name__ == "__main__":
    main()
