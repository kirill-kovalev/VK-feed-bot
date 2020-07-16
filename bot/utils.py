import time
from threading import Event, Thread
import traceback


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
        logFile = open("errors","a+")
        logFile.writelines(err);
        logFile.close();
    except:

        print(err)
        pass;
    return