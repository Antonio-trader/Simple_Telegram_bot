import requests
import misc
from yobit import get_btc
from time import sleep


token = misc.token

# https://api.telegram.org/bot711820426:AAFuhlgZDJmrvFeWK3VKByTLnq_63ENIDXE/sendmessage?chat_id=634010695&text=hi
URL = 'https://api.telegram.org/bot' + token + '/'

global last_update_id
last_update_id = 0


def get_updates():
    url = URL + 'getupdates'
    r = requests.get(url)
    return r.json()


def get_message():
    """
    . Отвечать только на новые сообщения
    . получаем update_id, каждого обновления
    . записываем в переменную, а затем сравниваем с update_id элемента в
    . списке result
    """

    data = get_updates()

    last_object = data['result'][-1]
    current_update_id = last_object['update_id']

    global last_update_id
    if last_update_id != current_update_id:
        last_update_id = current_update_id

        chat_id = data['result'][-1]['message']['chat']['id']
        message_text = last_object['message']['text']

        message = {'chat_id': chat_id,
                   'text': message_text}

        return message
    return None


def send_message(chat_id, text='Wait a second, please...'):
    url = URL + 'sendmessage?chat_id={}&text={}'.format(chat_id, text)
    requests.get(url)


def main():
    #d = get_updates()




    while True:
        answer = get_message()

        if answer != None:
            chat_id = answer['chat_id']
            text = answer['text']

            if text == '/btc':
                send_message(chat_id, get_btc())
        else:
            continue

        sleep(2)


if __name__ == '__main__':
    main()