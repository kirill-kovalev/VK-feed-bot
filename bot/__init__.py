import telebot
import vk
import time, datetime, sys, urllib

bot = telebot.TeleBot(sys.argv[1]);


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
    bot.send_message(chat_id, '⁣⁣⁣⁣⁣\n\n\n─────────────────────────────────────────────────────────────────────────────────\n\n\n⁣⁣⁣⁣⁣')
    text = '<b>[' + sourceName + ']  ' + postTime.strftime(
        "<i>%d/%m</i> в <i>%H:%M</i>") + ':</b>\n' + post['text'] + "\n"
    bot.send_message(chat_id,text,parse_mode='html');


    print(text)
    try:
        for attachment in post['attachments']:

            try:
                if attachment['type'] == 'photo':
                    link = attachment['photo']['sizes'][-1]['url']
                    file = urllib.request.urlopen(link).read()
                    bot.send_photo(chat_id, file)

                elif attachment['type'] == 'video':
                    link = "https://vk.com/id1?z=video" + str(attachment['video']['owner_id']) + "_" + str(attachment['video']['id'])
                    bot.send_message(chat_id, "<b><i>" + link + "</i></b>", parse_mode='html')
                elif attachment['type'] == 'doc':
                    link = attachment['doc']['url']
                    file = urllib.request.urlopen(link).read()
                    bot.send_document(chat_id, file)
                elif attachment['type'] == 'audio':
                    link = attachment['audio']['url']
                    file = urllib.request.urlopen(link).read()
                    bot.send_document(chat_id, file)
                elif attachment['type'] == 'link':
                    link = attachment['link']['url']
                    bot.send_message(chat_id,"["+attachment['link']['title'] +"] ("+link+") \n" , parse_mode='html')
                else:
                    bot.send_message(chat_id, "[" + attachment['type']+ "]")
            except: pass;
        #end of for attachment in post['attachments']:

    except:
        pass
    time.sleep(1)


def watchFeed(token, chat_id):
    print("_____________________________________________\nStart watching\n");
    print("chat_id: "+str(chat_id));
    print("token: "+token)
    print("_____________________________________________")
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










if __name__ == '__main__':

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        if message.text == "/start":
            bot.send_message(message.from_user.id,"Отправь сгенерированный токен https://oauth.vk.com/authorize?client_id=6146827&scope=1073737727&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1")
        else:
            print(message.text)
            try:
                watchFeed(message.text, message.from_user.id)
            except vk.exceptions.VkAPIError:

                bot.send_message(message.from_user.id, "неверный токен")
        return


    bot.polling(none_stop=True, interval=1)
