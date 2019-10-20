from config import token
from time import sleep
import urllib.request, urllib.parse, json, codecs

last_status = None
# Telegram
tgUrl = 'https://api.telegram.org/bot' + token + '/'
userId = 72025926
updateId = 0

def tgMessage(chatId, text):
    try:
        data = urllib.parse.urlencode({'chat_id': format(chatId), 'text': text})
        urllib.request.urlopen(tgUrl +  'sendMessage', data.encode('utf-8'))
    except:
        return

while True:
    with urllib.request.urlopen('http://192.168.2.1/goform/getImgInfo') as url:
        data = json.loads(url.read().decode())

        chg_states = {
            0: 'CARGANDO',
            1: 'COMPLETO',
            2: 'BATERIA'
        }
        bat_levels = {
            0: '0%',
            1: '25%',
            2: '50%',
            3: '75%',
            4: '100%'
        }

        chg_state = chg_states[data['chg_state']]
        bat_level = bat_levels[data['bat_level']]
        status_message = '%s %s' % (chg_state, bat_level)

        if last_status != (chg_state, bat_level):
            tgMessage(userId, status_message)
            last_status = (chg_state, bat_level)
            continue

        data = urllib.parse.urlencode({'offset': format(updateId), 'limit': '100', 'timeout': '60'})
        response = urllib.request.urlopen(tgUrl + 'getUpdates', data.encode('utf-8'))
        reader = codecs.getreader("utf-8")
        data = json.load(reader(response))

        if data['ok']:
            for update in data['result']:
                updateId = update['update_id'] + 1
                message = update['message']

                if 'text' in message:
                    messagetext = str(message['text'])

                    if messagetext == 'st':
                        tgMessage(userId, status_message)

    sleep(10)
