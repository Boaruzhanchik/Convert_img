import requests

def add_text_for_uniqueness_check(text, userkey, exceptdomain='', excepturl='', visible='', copying='', callback=''):
    text_ru_url = 'http://api.text.ru/post'

    data = {
        'text': text,
        'userkey': userkey,
        'exceptdomain': exceptdomain,
        'excepturl': excepturl,
        'visible': visible,
        'copying': copying,
        'callback': callback
    }

    response = requests.post(text_ru_url, data=data)

    if response.status_code == 200:
        result = response.json()
        if 'text_uid' in result:
            text_uid = result['text_uid']
            date_check = result.get('date_check')
            unique = result.get('unique')
            urls = result.get('urls', [])
            
            print(f"Text UID: {text_uid}")
            if date_check:
                print(f"Date Check: {date_check}")
            if unique is not None:
                print(f"Unique: {unique:.2f}%")

            for url_info in urls:
                url = url_info.get('url')
                plagiat = url_info.get('plagiat')
                words = url_info.get('words', [])
                clear_text = url_info.get('clear_text', '')

                print(f"URL: {url}")
                if plagiat is not None:
                    print(f"Plagiarism: {plagiat:.2f}%")
                if words:
                    print("Matching Words:")
                    for word_pos in words:
                        print(clear_text[word_pos])
                print("-" * 20)

            return text_uid
        else:
            print('Error: Text was not added for uniqueness check')
    else:
        print('Error adding text for uniqueness check')
    
    return None

# Пример использования функции
api_key = '8c55a5e74f0d54a2dae378e5da451cb6'
text_to_check = "Старая береза – это великолепное дерево, которое с годами приобретает особое очарование и характер. Березы в России и других странах с холодным климатом часто растут в течение многих десятилетий, и их внешний вид меняется под воздействием времени и природных факторов."
text_uid = add_text_for_uniqueness_check(text_to_check, api_key)
