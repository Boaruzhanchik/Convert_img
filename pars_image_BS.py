import requests
import xml.etree.ElementTree as ET
import os


url = "https://tvoe.ru/bitrix/catalog_export/export_yVi.xml"
response = requests.get(url)

if response.status_code == 200:
    root = ET.fromstring(response.content)
    if not os.path.exists("images"):
        os.makedirs("images")

    for index, offer in enumerate(root.findall(".//offer")):
        image_url = offer.find(".//picture").text
        if image_url:
            try:
                response = requests.get(image_url)
                if response.status_code == 200:
                    with open(f"images/image_{index + 1}.jpg", "wb") as f:
                        f.write(response.content)
                    print(f"Изображение {index + 1} сохранено.")
                else:
                    print(f"Не удалось загрузить изображение {index + 1}. Статус код: {response.status_code}")
            except Exception as e:
                print(f"Ошибка при сохранении изображения {index + 1}: {str(e)}")
else:
    print("Не удалось загрузить XML-файл.")
