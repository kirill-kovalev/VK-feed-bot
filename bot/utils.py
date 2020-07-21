import time
from threading import Event, Thread
import traceback
import re


def log(message , source = None):
    data = "["+str(time.time())+"] ------------------\n"+ message + "\n\n["+str(source)+"]----------------------"
    print(data)
    try:
        logFile = open("bot.log","a+")
        logFile.writelines(data);
        logFile.close();
    except:

        trace_exc()
        pass;
    return



def call_repeatedly(interval, func, *args):
    stopped = Event()
    def loop():
        while not stopped.wait(interval): # the first call is in `interval` secs
            func(*args)
    Thread(target=loop).start()
    return stopped.set

def trace_exc():
    err = str(time.time()) +"\n"+traceback.format_exc()
    try:
        logFile = open("errors.log","a+")
        logFile.writelines(err);
        logFile.close();
    except:

        print(err)
        pass;
    return

def getToken(string:str):
    tokenRegexp = "[a-f0-9]{85}"
    return re.findall(tokenRegexp,string)[0]

def str_split(string:str, size:int):
    return re.findall('.{%s}' % size, string)