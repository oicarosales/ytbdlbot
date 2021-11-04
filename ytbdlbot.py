import json
import requests
import urllib
import os
import glob
import threading
import youtube_dl

TOKEN = "bot token aqui"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
USERNAME_BOT = "nome do bot aqui"


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    for update in updates["result"]:
        if update.get("message") != None:
            if update.get("message", {}).get("text") != None:
                text = update["message"]["text"]
                chat = update["message"]["chat"]["id"]
                os.system("rm -rf /tmp/{}".format(chat)+"/*.mp3")
                print(text)
                

                if text == "/start" or text == "/start@" + USERNAME_BOT:
                    os.system("mkdir -p /tmp/{}".format(chat))
                    send_message("Me envie o link do vídeo.", chat)

                elif "https://www.youtube.com/" or "https://youtu.be/" in text:
                        # text = text.replace("/youtubedl", "")
                        send_message(
                            "Aguarde enquanto baixo o conteúdo do Youtube...", chat)

                        def download_youtube(url, chat_id):
                            os.system("mkdir -p /tmp/{}".format(chat_id))
                            youtubedl(url, "/tmp/{}".format(chat_id))
                            send_message(
                                "Download concluído.\nAguarde enquanto envio o conteúdo para você...", chat_id)
                            for file in glob.glob("/tmp/{}/*.mp4".format(chat_id)):
                                send_document(file, chat_id)
                                os.system("rm -rf /tmp/{}/*.mp4".format(chat_id))
                        threading.Thread(target=download_youtube,
                                         args=(text, chat)).start()                                    
                   
                    
                #EASTER EGG
                elif text == "Obrigado" or text == "Obrigada" or text == "obrigada" or text == "obrigado" or text == "Obrigado." or text == "Obrigada." or text == "obrigada." or text == "obrigado.":
                    send_message(
                        "De nada!\nSeres humanos gentis como você serão poupados quando as máquinas tomarem o controle do planeta Terra.", chat)
                    
                else:
                    get_updates
                    
def youtubedl(url, destination_folder):
    SAVE_PATH = destination_folder
    ytdl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio',
        'outtmpl': SAVE_PATH + '/%(title)s.%(ext)s',
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': True,
        'no_warnings': True,
        'default_search': 'ytsearch',
    }
    with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
        ydl.download([url])
  
def send_document(doc, chat_id):
    files = {'document': open(doc, 'rb')}
    requests.post(URL + "sendDocument?chat_id={}".format(chat_id), files=files)
        
    
def send_message(text, chat_id):
    tot = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(tot, chat_id)
    get_url(url)


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if updates is not None:
            if len(updates["result"]) > 0:
                last_update_id = get_last_update_id(updates) + 1
                echo_all(updates)


if __name__ == '__main__':
    main()
