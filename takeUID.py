import requests
import time
userkey = '86defad4fd4e8a4f039b412f952f896b'
text = "Старая береза – это великолепное дерево, которое  других странах,ид меняется под воздействием времени и природных факторов."

body = {
    'userkey': userkey,
    'text': text,
}

url = 'https://api.text.ru/post'
headers = {'Content-type': 'application/json'}
response = requests.post(url, json=body, headers=headers)

if response.status_code != 200:
    raise Exception(f'Ошибка HTTP: {response.status_code}')

data = response.json()
uid = data['text_uid']  # Извлекаем UID из ключа 'text_uid' в JSON-ответе
print(uid)
time.sleep(60)
# Теперь у вас есть UID, который вы можете использовать во втором коде
userkey = '86defad4fd4e8a4f039b412f952f896b'  # Замените на ваш реальный ключ пользователя

# Создаем тело запроса для получения результата анализа
result_body = {
    'userkey': userkey,
    'uid': uid,
    'format': 'json',  # Указываем формат результата как JSON
}

result_url = 'https://api.text.ru/post'
result_response = requests.post(result_url, json=result_body, headers=headers)

if result_response.status_code != 200:
    raise Exception(f'Ошибка HTTP: {result_response.status_code}')

result_data = result_response.json()

# Выводим информацию о результатах проверки на уникальность (result_json)
print(result_data)
