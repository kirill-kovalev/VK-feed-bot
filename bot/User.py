import vk
import traceback
from utils import *
from TGBot import TG



class User:
    class WrongToken(Exception):
        def __init__(self): return;

    API: vk.API = None
    chat_id: int = None
    token: str = ""
    last_upd_time = time.time() - 300

    def __init__(self, chat_id: int, token: str):
        log("started user " + str(chat_id) + " with token " + getToken(token))
        try:
            VKSession = vk.Session(access_token=token)
            self.API = vk.API(VKSession, v='5.111')
            self.token = token
            self.chat_id = chat_id

            self.start()

        except:
            trace_exc()
            raise self.WrongToken()
            pass;

    def start(self):
        self.stop = call_repeatedly(10, self.watch)

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

        list = vkFeed["items"]
        for post in list[::-1]:
            TG.sendPost(post, self.chat_id, vkFeed)

        # end of for post in vkFeed["items"]

        return;
