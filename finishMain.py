import tkinter as tk
import requests
import time
import openpyxl

def send_text_to_textru(text):
    userkey = '86defad4fd4e8a4f039b412f952f896b'
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
    userkey = '86defad4fd4e8a4f039b412f952f896b'
    url = 'https://api.text.ru/post'
    headers = {'Content-type': 'application/json'}
    body = {
        'userkey': userkey,
        'uid': uid,
        'format': 'json',
    }
    time.sleep(12)  # Задержка в 12 секунд (согласно ограничениям API text.ru)
    response = requests.post(url, json=body, headers=headers)
    if response.status_code != 200:
        raise Exception(f'Ошибка HTTP: {response.status_code}')
    result_data = response.json()
    return result_data

def send_text_to_turgenev(text):
    url = "https://turgenev.ashmanov.com/"
    api_key = "b1e9a9bb1f72d9b9ee3f72a6219789dc"
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

def process_text():
    text = text_entry.get("1.0", tk.END).strip()

    # Send text to text.ru
    textru_uid = send_text_to_textru(text)
    time.sleep(5)  # Подождать, чтобы получить uid
    textru_result = None
    while textru_result is None:
        textru_result = get_textru_result(textru_uid)
        time.sleep(1)  # Подождать 1 секунду перед повторной попыткой

    textru_unique = textru_result['text_unique']
    print(f"Уникальность текста по результатам проверки на text.ru: {textru_unique}")

    # Send text to turgenev.ashmanov.com
    turgenev_result = send_text_to_turgenev(text)
    if "error" in turgenev_result:
        print("Произошла ошибка при проверке на turgenev.ashmanov.com:", turgenev_result["error"])
    else:
        risk_score = turgenev_result["risk"]
        risk_level = turgenev_result["level"]
        print("Оценка риска от turgenev.ashmanov.com:")
        print("Оценка риска:", risk_score)
        print("Степень риска:", risk_level)

        # Save results to Excel file
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

# Create the GUI
window = tk.Tk()
window.title("Text Analysis")
window.geometry("400x300")

# Text Entry
text_entry = tk.Text(window, height=10, width=40)
text_entry.pack()

# Submit Button
submit_button = tk.Button(window, text="Submit", command=process_text)
submit_button.pack()

window.mainloop()