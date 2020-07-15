
import sys
from bot.utils import *
from bot.TGBot import *
from bot.User import *
from bot.UserList import *


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
            log(userList.toJSON())
        else:
            try:
                userList.add(message.from_user.id,message.text);
                userList.save()
                TG.bot.send_message(message.from_user.id, "Вы подписались на новости")
            except User.WrongToken:
                TG.bot.send_message(message.from_user.id, "Неверный токен")
                pass;
            except UserList.UserExists:
                TG.bot.send_message(message.from_user.id, "Вы уже подписались на рассылку")
                pass;

        return


    TG.bot.polling(none_stop=True, interval=1)
