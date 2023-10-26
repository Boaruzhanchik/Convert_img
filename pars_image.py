from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from io import BytesIO
from PIL import Image
import os

driver = webdriver.Chrome()

driver.get("https://fishcanal.ru/catalog/udilishcha/")

wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.TAG_NAME, "img")))

image_elements = driver.find_elements(By.TAG_NAME, "img")

if not os.path.exists("images"):
    os.makedirs("images")

for index, image_element in enumerate(image_elements):
    image_url = image_element.get_attribute("src")

    if image_url:
        try:
            response = requests.get(image_url)
            if response.headers.get("content-type", "").startswith("image"):
                image = Image.open(BytesIO(response.content))
                image_path = os.path.join("images", f"image_{index+1}.jpg")
                image.save(image_path)
        except Exception as e:
            print(f"Ошибка при сохранении изображения: {str(e)}")

driver.quit()
