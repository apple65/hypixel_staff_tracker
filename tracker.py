import threading, requests, sys, os
from bs4 import BeautifulSoup

usernames = sys.argv[2:]
refreshrate = int(sys.argv[1])


def set_interval(sec):
    def func_wrapper():
        set_interval(sec)
        get_lastlogin()

    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


def saveline(filename, mode, login):
    with open(filename, mode) as fd:
        fd.write(login)


def get_lastlogin():
    for username in usernames:
        filename = username + ".txt"

        # Get login from website
        r = requests.get('http://hypixel.net/player/' + username)
        soup = BeautifulSoup(r.content, 'html.parser')
        candidates = soup.findAll(class_="DateTime")
        login = candidates[0]['title']+"\n"

        print(username + " logged on " + login)

        # If file does not exist, create it
        mode = 'a'
        if not os.path.exists(filename):
            mode = 'w'

        # Get last stored login
        if mode != 'w':
            with open(filename) as f:
                data = f.readlines()
                lastline = ""
                if not data:
                    mode = 'w'
                else:
                    lastline = data[-1]

                # Save new login
                if lastline != login:
                    saveline(filename, mode, login)
        else:
            saveline(filename, mode, login)


set_interval(refreshrate)
