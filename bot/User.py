import vk
import traceback
from utils import *
from TGBot import TG



class User:
    class WrongToken(Exception):
        def __init__(self): return;

    stop = None
    API: vk.API = None
    chat_id: int = None
    token: str = ""
    last_upd_time = None
    upd_timeout = 60


    def __init__(self, chat_id: int, token: str , upd_time = time.time() - 300 ):
        log("started user " + str(chat_id) + " with token " + token)
        try:
            VKSession = vk.Session(access_token=token)
            self.API = vk.API(VKSession, v='5.111')
            self.token = token
            self.chat_id = chat_id
            self.last_upd_time = upd_time
            TG.bot.send_message(chat_id, "Начинаю отправку новостей...")
            self.start()

        except Exception:
            trace_exc()
            raise self.WrongToken()
            pass;

    def start(self):
        self.stop = call_repeatedly(self.upd_timeout, self.watch)

    def __del__(self):
        log("stoped user " + str(self.chat_id) + " with token " + self.token)

    def watch(self):
        log("check user "+ str(self.chat_id))
        vkFeed = self.API.newsfeed.get(
            filters='post',
            return_banned=0,
            start_time=self.last_upd_time
        )

        self.last_upd_time = time.time()

        postList = vkFeed["items"]
        for post in postList[::-1]:
            try:
                TG.sendPost(post, self.chat_id, vkFeed)
            except:
                trace_exc()
                TG.bot.send_message(self.chat_id,traceback.format_exc())

        # end of for post in vkFeed["items"]

        return;
