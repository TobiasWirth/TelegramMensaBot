import requests
import json
import os
import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from requests_html import HTMLSession
import requests_html
from apscheduler.schedulers.blocking import BlockingScheduler
import logging

logging.basicConfig()

import telepot
from telepot.loop import MessageLoop
from pprint import pprint
import datetime

from os import environ
from flask import Flask

app = Flask(__name__)
app.run(host= '0.0.0.0', port=environ.get('PORT'))



# create Bot
bot = telepot.Bot('838947615:AAH6WV9wKS-EIOmRL04zgHOSPgBih09fUWE')

bot.getMe()

session = HTMLSession()

users = []


# return menu for cafeteria at Markusstrasse
def returnMarkusMenu():
    r = session.get("https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/speiseplaene/interimsmensa-markusplatz-bamberg.html")
    currentWeekMarkus = r.html.find(".week.currentweek", first=True)

    weekDaysMarkus = currentWeekMarkus.find("day")

    #retrieve today's date
    today = r.html.find("#thecurrentday")

    # Example element: [<Element 'div' id='thecurrentday' data-day='Dienstag 17.10.'>]
    # slice and split so that only the current day as a string ('Dienstag') remains
    today = str(today[0]).split("data-day='")[1][:-2].split(" ")[0]
    #a = a.split(" ")[0]

    # build return string containing menu information
    menu = "Heute in der Markusstraße: \n"

    for day in weekDaysMarkus:

        if day.find("div[data-day~="+today+"]"):
            currentday = day.find("div[data-day~="+today+"]")
            for fooditem in currentday:
                titles = fooditem.find(".title")
                prices = fooditem.find(".price")
                i = 1
                for title in titles:

                    menu += title.text + " " + prices[i].text + "\n"
                    i += 1



    menu += ("\n" + returnCafeteriaMenu("markus"))

    print(menu)

    return menu

# return menu for cafeteria at Feldkirchenstrasse
def returnFekiMenu():

    r = session.get(
        'https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/speiseplaene/mensa-feldkirchenstrasse-bamberg.html')
    currentWeekFeki = r.html.find('.week.currentweek', first=True)


    weekDaysFeki = currentWeekFeki.find(".day")

    #retrieve today's date
    today = r.html.find("#thecurrentday")

    # Example element: [<Element 'div' id='thecurrentday' data-day='Dienstag 17.10.'>]
    # slice and split so that only the current day as a string ('Dienstag') remains
    today = str(today[0]).split("data-day='")[1][:-2].split(" ")[0]
    #a = a.split(" ")[0]

    # build return string containing menu information
    menu = "Heute an der Feki: \n"

    for day in weekDaysFeki:

        if day.find("div[data-day~="+today+"]"):
            currentday = day.find("div[data-day~="+today+"]")
            for fooditem in currentday:
                titles = fooditem.find(".title")
                prices = fooditem.find(".price")
                i = 1
                for title in titles:

                    menu += title.text + " " + prices[i].text + "\n"
                    i += 1

    print(menu)
    return menu

# return menu of alternative cafeteria located at Erba or Markusstrasse
def returnCafeteriaMenu(cafeteria):

    if cafeteria == "erba":
        r = session.get("https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/sonderspeiseplaene/cafeteria-erba-insel.html")
        menu = "Heute in der Erba-Cafeteria: \n"
    else:
        r = session.get("https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/sonderspeiseplaene/cafeteria-markusplatz.html")
        menu = ""

    content = r.html.find("article p")

    today_date = str(datetime.date.today().day)

    today_date = datetime.date.today().day

    today_date = today_date + 1

    today_date = str(today_date)

    menu = ""

    for p_element in content:
        if today_date in p_element.text:
            menu += p_element.text[7:]


    return menu


# handle incoming messages and send messages containing menu information to requesting user
def handle(msg):
    pprint(msg)
    print(msg['text'])

    msg_text = msg['text']

    user_id = msg['from']['id']

    print(user_id)

    if 'feki' in msg_text or 'Feki' in  msg_text:
        sendMessage(user_id, returnFekiMenu())
    else:
        if 'markus' in msg_text or 'Markus' in  msg_text:
            sendMessage(user_id, returnMarkusMenu())
        else:
            if 'alles' in msg_text or 'Alles' in msg_text:
                msg = returnMarkusMenu() + "\n" + "\n" + returnFekiMenu()
                sendMessage(user_id, msg)
            else:
                if 'täglich' in msg_text or 'Täglich' in msg_text:
                    users.append(user_id)
                    sendMessage(user_id, "Du bekommst jetzt täglich Infos über das Essen an der Feki, Erba und in der Innenstadt! "
                                         "Um keine täglichen Nachrichten mehr zu erhalten, sende \"stop\" an mich.")




def sendMessage(user_id, text):
    bot.sendMessage(user_id, text)


MessageLoop(bot, handle).run_as_thread()

def main():
    MessageLoop(bot, handle).run_as_thread()
    returnFekiMenu()
    returnMarkusMenu()
    returnCafeteriaMenu("markus")


dailyScheduler = BackgroundScheduler()


def sendScheduledMessages():
    for user_id in users:
        sendMessage(user_id, "text")



dailyScheduler.add_job(sendScheduledMessages, 'cron', day_of_week='mon-fri', hour=10, minute=0)


# run requestBitcoin() function once every 60 seconds
# dailyScheduler.add_job(requestBitCoin, 'interval', seconds=60)

dailyScheduler.start()


@app.route("/")
def index():
    #do whatevr here...
    return "Hello Heruko"

if __name__== "__main__":
	main()
