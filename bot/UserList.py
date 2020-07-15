from bot.utils import *
import json
from bot.User import *

class UserList:
    class UserExists(Exception):
        def __init__(self): return ;
    class UserNotExists(Exception):
        def __init__(self): return;


    userList:[User] = []


    def add (self,chat_id:int , token:str ):
        for user in self.userList:
            if user.chat_id == chat_id:
                raise self.UserExists()
                return

        try:
            user = User(chat_id,token)
            self.userList.append(user)
        except Exception as exception:
            raise exception;

    def remove(self,chat_id):
        for user in self.userList:
            if user.chat_id == chat_id:
                user.stop()
                self.userList.remove(user)
                return True
        raise self.UserNotExists

    def toJSON(self):
        users = [ (user.chat_id,user.token) for user in self.userList]
        return json.dumps(users)

    def fromJSON(self,string:str):
        for user in self.userList:
            user.stop()
        users = json.loads(string)
        for user in users:
            try:
                self.userList.append(User(user[0],user[1]))
            except: pass

    def save(self):
        try:
            file = open("users.json", "w+");
            file.writelines(self.toJSON())
            file.close();
            log("saved", "")
        except:

            log("can't save");
            log(traceback.format_exc())
            pass

    def load(self):
        try:
            file = open("users.json", "r");
            json = file.readlines(1)[0]
            self.fromJSON(json)
        except:
            log(traceback.format_exc())
            pass;
