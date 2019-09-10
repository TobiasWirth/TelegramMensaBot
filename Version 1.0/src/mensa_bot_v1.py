import requests
import json
import os
import datetime

from requests_html import HTMLSession
import requests_html
from apscheduler.schedulers.blocking import BlockingScheduler
import logging

logging.basicConfig()

import telepot
from telepot.loop import MessageLoop
from pprint import pprint
import datetime

# create Bot
bot = telepot.Bot('838947615:AAH6WV9wKS-EIOmRL04zgHOSPgBih09fUWE')

bot.getMe()

session = HTMLSession()

# def returnFood(day):

r = session.get(
    'https://web.archive.org/web/20171017053414/http://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/speiseplaene.html?tx_thmensamenu_pi2%5Bmensen%5D=3&tx_thmensamenu_pi2%5Baction%5D=show&tx_thmensamenu_pi2%5Bcontroller%5D=Speiseplan&cHash=c3fe5ebb35e5fba3794f01878e798b7c')
currentWeekFeki = r.html.find('.week.currentweek', first=True)

# weekDaysMarkushaus = currentWeekMarkushaus.find(".day")
weekDaysFeki = currentWeekFeki.find(".day")

#day = r.html.find(".day [data-day~=Dienstag]")

#w = weekDaysFeki.find("[data-day~=Dienstag]")

now = datetime.datetime.now()

today = now.today()


today = r.html.find("#thecurrentday")

if "Dienstag" in str(today[0]):
    print('yes')


menu = ""

for day in weekDaysFeki:

    if day.find("div[data-day~=Dienstag]"):
        currentday = day.find("div[data-day~=Dienstag]")
        for fooditem in currentday:
            titles = fooditem.find(".title")
            prices = fooditem.find(".price")
            i = 1
            for title in titles:

                menu += title.text + " " + prices[i].text + "\n"
                i += 1

print(menu)








def getCurrentWeekMenu():
    # r = session.get('https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/speiseplaene/interimsmensa-markusplatz-bamberg.html')

    # currentWeekMarkushaus = r.html.find('.week.currentweek', first=True)

    # r = session.get('https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/speiseplaene/mensa-feldkirchenstrasse-bamberg.html')

    r = session.get(
        'https://web.archive.org/web/20171017053414/http://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/speiseplaene.html?tx_thmensamenu_pi2%5Bmensen%5D=3&tx_thmensamenu_pi2%5Baction%5D=show&tx_thmensamenu_pi2%5Bcontroller%5D=Speiseplan&cHash=c3fe5ebb35e5fba3794f01878e798b7c')
    currentWeekFeki = r.html.find('.week.currentweek', first=True)

    # weekDaysMarkushaus = currentWeekMarkushaus.find(".day")
    weekDaysFeki = currentWeekFeki.find(".day")

    # dayListMarkushaus = []
    dayListFeki = []

    now = datetime.datetime.now()

    # Build JSON for Fekimensa menu
    for day in weekDaysFeki:

        titles = day.find(".title")
        prices = day.find(".price span")

        menu = ""
        i = 0
        for title in titles:
            # menu += "{ title: " + title.text + ", price: " + prices[i].text + "€ },"
            menu += "{" + '\'title\':' + title.text + "," + "\'price\': 2,80€" + "}" + ","
            menu = menu.strip('"\'')
            i += 1

        menu = menu[:-1]
        menu = menu.strip('\"\'')


def handle(msg):
    pprint(msg)
    print(msg['text'])

    msg_text = msg['text']

    user_id = msg['from']['id']

    print(user_id)

    if 'menu' in msg_text or 'Menu' in msg_text:
        msg = ""

        sendMessage(user_id, msg)


def sendMessage(user_id, text):
    bot.sendMessage(user_id, text)


MessageLoop(bot, handle).run_as_thread()

# def main():


dailyScheduler = BlockingScheduler()

# run requestBitcoin() function once every 60 seconds
# dailyScheduler.add_job(requestBitCoin, 'interval', seconds=60)

# dailyScheduler.start()

# if __name__== "__main__":
#	main()
