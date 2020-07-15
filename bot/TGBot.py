
import traceback
import urllib,datetime
import tempfile
from utils import *

from telebot import *
from AudioProc import AudioProc




class TGBot:
    bot:TeleBot = None
    def __init__(self, token:str):
        try:
            self.bot = TeleBot(token);
        except:
            log(traceback.format_exc())
            pass;

    def getSourceName(self,sources, source_id):
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

        return sourceName

    def getAttachments(self,post):
        attachments = {
            'photo': [],
            'video': [],
            'doc': [],
            'audio': [],
            'link': [],
            'any': []
        }


        for attachment in post['attachments']:

            if attachment['type'] == 'photo':
                link = attachment['photo']['sizes'][-1]['url']
                file = urllib.request.urlopen(link).read()
                photo = types.InputMediaPhoto(file)
                attachments['photo'].append(photo)
            # end of if attachment['type'] == 'photo':
            elif attachment['type'] == 'video':
                link = "https://vk.com/id1?z=video" + str(attachment['video']['owner_id']) + "_" + str(
                    attachment['video']['id'])
            # end of elif attachment['type'] == 'video':
            elif attachment['type'] == 'doc':
                link = attachment['doc']['url']
                data = urllib.request.urlopen(link).read()

                with tempfile.TemporaryDirectory(attachment['doc']['title']) as dir_:
                    tmpFile = open(dir_ + attachment['doc']['title'], "wb")
                    tmpFile.write(data)
                    tmpFile.close()
                    attachments['doc'].append(dir_ + attachment['doc']['title'])
                # end of with

            # end of elif attachment['type'] == 'doc':
            elif attachment['type'] == 'audio':
                link = attachment['audio']['url']
                result = AudioProc().parse_m3u8(link)
                attachments['audio'].append({
                    'data' : AudioProc().download_m3u8(*result),
                    'title' : attachment['audio']['title'],
                    'performer' : attachment['audio']['artist']
                })
            # end of elif attachment['type'] == 'audio':
            elif attachment['type'] == 'link':
                link = attachment['link']['url']
                attachments['link'].append(link)
            #end of elif attachment['type'] == 'link':
            else:
                attachments['any'].append( "[" + attachment['type'] + "]")
            # end of

        # end of for attachment in post['attachments']
        return attachments



    def sendPost(self,post, chat_id, vkFeed):
        sourceName = self.getSourceName(vkFeed, post['source_id'])
        postTime = datetime.datetime.fromtimestamp(post['date'])
        # self.bot.send_message(chat_id, '⁣⁣⁣⁣⁣\n\n\n⁣⁣⁣⁣⁣')
        text = '<b>[' + sourceName + ']  ' + postTime.strftime(
            "<i>%d/%m</i> в <i>%H:%M</i>") + ':</b>\n' + post['text'] + "\n"


        log(text , chat_id)


        attachments = self.getAttachments(post)

        for video in attachments['video']:
            text+= "\n"+ video

        for link in attachments['link']:
            text+= "\n"+ link


        if not len(attachments['photo']) == 0:
            attachments['photo'][0].parse_mode = 'html'
            attachments['photo'][0].caption = text
            self.bot.send_media_group(chat_id,attachments['photo'])
        else:
            self.bot.send_message(chat_id, text, parse_mode='html');

        for doc in attachments['doc']:
            self.bot.send_document(chat_id,doc)
        for audio in attachments['audio']:
            self.bot.send_audio(chat_id,audio['data'],
                                performer=audio['performer'],
                                title=audio['title'])



TG = TGBot(sys.argv[1])