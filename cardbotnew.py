import requests
import datetime

from time import sleep

token = "472709917:AAGpe6iH3ORSP7CyzKUusXUuGfgcWLXUhLg"
url = "https://api.telegram.org/bot" + token


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=2):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def send_html_message(self, chat_id, text, parse_mode, disable_web_page_preview):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': parse_mode, 'disable_web_page_preview': disable_web_page_preview}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def send_photo(self, chat_id, photo):
        params = {'chat_id': chat_id, 'photo': photo}
        method = 'sendPhoto'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = None

        return last_update


botik = BotHandler(token)
sym1 = "$"
sym2 = "&&"


def main():  
    new_offset = None


    while True:
        botik.get_updates(new_offset)
        
        last_update = botik.get_last_update()
        if not last_update:
            continue
        try:
            last_update_id = last_update['update_id']
            last_chat_text = last_update['message']['text']
            last_chat_id = last_update['message']['chat']['id']
            last_chat_name = last_update['message']['from']['first_name']
            last_chat_person_id = last_update['message']['from']['id']
            print (last_chat_person_id, last_chat_name, last_update)
        except:
            None
        if last_chat_name == "romawkka":
            botik.send_message(last_chat_id, "На инквизиторов не работаю")
        elif sym1 in last_chat_text:
            try:
                a = last_chat_text.split(sym1)[1]
                a1 = "https://topdeck.ru/apps/cards/"+ a
                print (a1)
                botik.send_photo(last_chat_id, photo=a1)
            except:
                botik.send_message(last_chat_id, "I can't find that card :(")
        elif sym2 in last_chat_text:
            try:
                e = last_chat_text.split(sym2)
                print (e)
                sent = "Cards:\n"
                for i in range(len(e)):
                    if i>0 and len(e[i]) > 2:
                        sent += '<a href="https://topdeck.ru/apps/cards/'+ e[i] + '">' + e[i] + '</a>\n'
                print (sent)
                if len(sent)> 8:
                    botik.send_html_message(last_chat_id, sent, 'HTML', True)   
            except:
                botik.send_message(last_chat_id, "I can't find any cards :(")

        new_offset = last_update_id + 1

if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()

