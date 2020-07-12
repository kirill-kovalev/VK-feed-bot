import telebot
import vk
from threading import Thread
import time, datetime, sys, urllib , json
import re
import os.path
import tempfile
import subprocess
import requests
import traceback
from io import StringIO


bot = telebot.TeleBot(sys.argv[1]);
users = []

def log(data):
    print(data)
    try:
        logFile = open("bot.log","a+")
        logFile.writelines(data);
        logFile.close();
    except: print("cant log"); pass;
    return



regex = "https.*key.pub"
regex_2 = '"https.*pub?.*"'
regex_3 = 'ts?.*'


def parse_m3u8(url):
    urldir = os.path.dirname(url)
    playlist = requests.get(url).text
    keyurl = re.findall(regex, playlist)[0]
    key = requests.get(keyurl).text

    for match in re.finditer(regex_2, playlist, re.MULTILINE):
        playlist = playlist.replace(match.group(), 'key.pub')

    for match in re.finditer(regex_3, playlist):
        playlist = playlist.replace(match.group(), 'ts')

    return playlist, key, urldir


def download_m3u8(playlist, key, urldir, output='out.mp3'):
    ts_list = [x for x in playlist.split('\n') if not x.startswith('#')]

    with tempfile.TemporaryDirectory(output) as dir_:
        os.chdir(dir_)
        for file in ts_list[:-1]:
            with open(file, 'wb') as audio:
                audio.write(requests.get(os.path.join(urldir, file)).content)
        with open('key.pub', 'w') as keyfile:
            keyfile.write(key)
        with open('index.m3u8', 'w') as playlist_file:
            playlist_file.write(playlist)

        subprocess.call(['ffmpeg', '-allowed_extensions', "ALL", '-protocol_whitelist',
                         "crypto,file", '-i', 'index.m3u8', '-c', 'copy', f'{output}'])

        return open(output, 'rb').read()





def getSourceName(sources, source_id):
    sourceName = ""
    if source_id > 0:
        for user in sources['profiles']:
            if user['id'] == source_id:
                sourceName = user['first_name'] + ' ' + user['last_name']
                break
    else:
        for g in sources['groups']:
            if g['id'] == (-1 * source_id):
                sourceName = g['name']
                break
    # time.sleep(0.3)
    return sourceName

def sendPost(post,chat_id,vkFeed):
    sourceName = getSourceName(vkFeed, post['source_id'])
    postTime = datetime.datetime.fromtimestamp(post['date'])
    bot.send_message(chat_id, '⁣⁣⁣⁣⁣\n\n\n⁣⁣⁣⁣⁣')
    text = '<b>[' + sourceName + ']  ' + postTime.strftime(
        "<i>%d/%m</i> в <i>%H:%M</i>") + ':</b>\n' + post['text'] + "\n"
    bot.send_message(chat_id,text,parse_mode='html');


    log(text)

    try:
        attachments = {
            'photo' : [],
            'video': [],
            'doc': [],
            'audio' :[],
            'link': [],
            'any' : []
        }
        for attachment in post['attachments']:
            try:
                if attachment['type'] == 'photo':
                    link = attachment['photo']['sizes'][-1]['url']
                    file = urllib.request.urlopen(link).read()
                    attachments['photo'].append(file)
                elif attachment['type'] == 'video':
                    link = "https://vk.com/id1?z=video" + str(attachment['video']['owner_id']) + "_" + str(attachment['video']['id'])
                    bot.send_message(chat_id, "<b><i>" + link + "</i></b>", parse_mode='html')
                elif attachment['type'] == 'doc':
                    link = attachment['doc']['url']
                    data = urllib.request.urlopen(link).read()
                    tmpFile = open(attachment['doc']['title'],"wb")
                    tmpFile.write(data)
                    tmpFile.close()
                    tmpFile = open(attachment['doc']['title'], "rb")
                    bot.send_document(chat_id, tmpFile)
                    bot.send_document(chat_id, attachment['doc']['title'])


                elif attachment['type'] == 'audio':
                    link = attachment['audio']['url']
                    result = parse_m3u8(link)
                    bot.send_audio(chat_id, download_m3u8(*result),
                                   title=attachment['audio']['title'],
                                   performer = attachment['audio']['artist'] )
                elif attachment['type'] == 'link':
                    link = attachment['link']['url']
                    bot.send_message(chat_id,"["+attachment['link']['title'] +"] ("+link+") \n" , parse_mode='html')
                else:
                    bot.send_message(chat_id, "[" + attachment['type']+ "]")
            except:
                print(traceback.format_exc())
                pass;
        #end of for attachment in post['attachments']:
        if len(attachments['photo']) > 1:
            bot.send_media_group(chat_id,
                                 [telebot.types.InputMediaPhoto(photo) for photo in attachments['photo']])
        elif len(attachments['photo']) > 0:
            bot.send_photo(chat_id,attachments['photo'][0])
    except:
        print(traceback.format_exc())
        pass
    time.sleep(1)


def watchFeed(token, chat_id):
    log("_____________________________________________\nStart watching\n");
    log("chat_id: " + str(chat_id));
    log("token: " + str(token))
    log("_____________________________________________")
    bot.send_message(chat_id,"chat_id: "+str(chat_id))


    VKSession = vk.Session(access_token=token)
    VKapi = vk.API(VKSession, v='5.111')
    last_time = time.time() - 60
    while (True):
        vkFeed = VKapi.newsfeed.get(
            filters='post',
            return_banned=0,
            start_time = last_time
        )
        last_time = time.time()

        list = vkFeed["items"]
        for post in list[::-1]:
            try:
                sendPost(post,chat_id,vkFeed)
            except: pass;
        # end of for post in vkFeed["items"]

        time.sleep(10)
    # end of while(true)



def saveUserList():
    usersJson = json.dumps(users)
    file = open("users.json","w")
    file.writelines(usersJson)
    file.close()

def loadUserList():
    try:
        file = open("users.json", "r")
        usersJson = file.readlines(1)[0]
        file.close()

        decoded = json.load(StringIO(usersJson))
        for i in decoded:
            users.append(i)
    except: pass

def addUser(chat_id,token):
    users.append((chat_id,token))
    log("added " + str(chat_id))
    saveUserList()

def removeUser(chat_id):
    return
    for i,item in enumerate(users):
        if item[0] == chat_id:
            users.remove(users[i])
            log("removed " + str(chat_id))
            saveUserList()
            return




if __name__ == '__main__':
    print("hello")
    loadUserList()
    for user in users:
        log("started thread for " + str(user[0]) + "  with token  " + user[1])
        thread = Thread(target=watchFeed, args=(user[1],user[0]))
        thread.start()
        thread.join()



    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        if message.text == "/start":
            bot.send_message(message.from_user.id,"Отправь сгенерированный токен https://oauth.vk.com/authorize?client_id=6146827&scope=1073737727&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1")
        else:
            log(message.text)
            try:
                addUser(message.from_user.id, message.text)
                watchFeed(message.text, message.from_user.id)
            except vk.exceptions.VkAPIError:
                removeUser(message.from_user.id)
                bot.send_message(message.from_user.id, "неверный токен")
        return


    bot.polling(none_stop=True, interval=1)
