
import sys
from utils import *
from TGBot import *
from User import *
from UserList import *


userList = UserList()




if __name__ == '__main__':

    userList.load()

    @TG.bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        if message.text == "/start":
            TG.bot.send_message(message.from_user.id,
            """
Инструкция:
    1.Перейдите по ссылке vk.cc/auMNXq
    2.Затем нажмите "разрешить"
    3.Скопируйте часть адресной строки от access_token= до &expires_in
    4.Отправьте скопированный текст боту
    
    Можно отправить ссылку из адресной строки целиком (функция тестируется)
            """)
        elif message.text == "/stop":
            try:
                userList.remove(message.from_user.id)
                userList.save()
                TG.bot.send_message(message.from_user.id, "Остановлено")
            except UserList.UserNotExists:
                TG.bot.send_message(message.from_user.id, "Новости не отправляются")
                pass

        elif message.text == "/help":
            TG.bot.send_message(message.from_user.id, "Та зачем тебе....")
        elif message.text == "/restart":
            token = userList.get(message.from_user.id).token
            userList.remove(message.from_user.id)
            userList.add(message.from_user.id,token)
            userList.save()
        else:
            try:
                userList.add(message.from_user.id,getToken(message.text))
                userList.save()
                TG.bot.send_message(message.from_user.id, "Вы подписались на новости")
            except User.WrongToken:
                TG.bot.send_message(message.from_user.id, "Неверный токен")
                pass;
            except UserList.UserExists:
                TG.bot.send_message(message.from_user.id, "Вы уже подписались на рассылку")
                pass;
            except:
                TG.bot.send_message(message.from_user.id, "Это не похоже на токен");
                pass;

        return

    while(True):
        try:
            TG.bot.polling(none_stop=True, interval=1)
        except: pass
