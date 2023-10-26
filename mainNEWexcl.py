import os
import requests
import time
import openpyxl
from dotenv import load_dotenv
load_dotenv()


def send_text_to_textru(text):
    userkey = os.getenv("userkey")
    url = 'https://api.text.ru/post'
    headers = {'Content-type': 'application/json'}
    body = {
        'userkey': userkey,
        'text': text,
    }
    response = requests.post(url, json=body, headers=headers)
    if response.status_code != 200:
        raise Exception(f'Ошибка HTTP: {response.status_code}')
    data = response.json()
    uid = data['text_uid']
    return uid


def get_textru_result(uid):
    userkey = os.getenv("userkey")
    url = 'https://api.text.ru/post'
    headers = {'Content-type': 'application/json'}
    body = {
        'userkey': userkey,
        'uid': uid,
        'format': 'json',
    }
    time.sleep(12)
    response = requests.post(url, json=body, headers=headers)
    if response.status_code != 200:
        raise Exception(f'Ошибка HTTP: {response.status_code}')
    result_data = response.json()
    return result_data


def send_text_to_turgenev(text):
    url = "https://turgenev.ashmanov.com/"
    api_key = os.getenv("api_key")
    params = {
        "api": "risk",
        "key": api_key,
        "text": text
    }
    try:
        response = requests.post(url, data=params)
        response_data = response.json()
        return response_data
    except requests.exceptions.RequestException as e:
        print("Произошла ошибка при отправке запроса:", e)


text = input("Напишите текст для проверки на уникальность: ")


textru_uid = send_text_to_textru(text)
time.sleep(5)
textru_result = get_textru_result(textru_uid)
textru_unique = textru_result['text_unique']
print(f"Уникальность текста по результатам проверки на text.ru: {textru_unique}")


turgenev_result = send_text_to_turgenev(text)
if "error" in turgenev_result:
    print("Произошла ошибка при проверке на turgenev.ashmanov.com:", turgenev_result["error"])
else:
    risk_score = turgenev_result["risk"]
    risk_level = turgenev_result["level"]
    print("Оценка риска от turgenev.ashmanov.com:")
    print("Оценка риска:", risk_score)
    print("Степень риска:", risk_level)

    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet["A1"] = "Отправляемый текст"
    sheet["B1"] = "Уникальность текста (text.ru)"
    sheet["C1"] = "Оценка риска (turgenev.ashmanov.com)"
    sheet["D1"] = "Степень риска (turgenev.ashmanov.com)"
    sheet["A2"] = text
    sheet["B2"] = textru_unique
    sheet["C2"] = risk_score
    sheet["D2"] = risk_level
    wb.save("results.xlsx")
    print("Результаты сохранены в файл results.xlsx")
