import requests
import json
import os
import datetime

from requests_html import HTMLSession

from apscheduler.schedulers.blocking import BlockingScheduler
import logging;logging.basicConfig()

import telepot
from telepot.loop import MessageLoop
from pprint import pprint

#create Bot
bot = telepot.Bot('838947615:AAH6WV9wKS-EIOmRL04zgHOSPgBih09fUWE')

json_weekMenu = None

bot.getMe()

session = HTMLSession()

def getCurrentWeekMenu():
    r = session.get('https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/speiseplaene/interimsmensa-markusplatz-bamberg.html')
    weekMenu = r.html.find('.week.currentweek', first=True)

    global json_weekMenu

    weekDays = weekMenu.find(".day")

    for day in weekDays:
        t = day.find(".title")
        for tt in t:
            print(tt.text)

              
    
    j = json.dumps({
        "monday": {
            "date": "19.08.",
            "mensas": [
                {
            "name":  "Mensa Markusgebäude",
            "title": "Food1",
            "price": "2.80€"
                  },
                {
            "name":  "Cafeteria Markusgebäude",
            "title": "Food2",
            "price": "3.80€"
                  },
                {
            "name":  "Feki",
            "title": "Food2",
            "price": "3.80€"
                  },
                {
            "name":  "Erba",
            "title": "Food2",
            "price": "3.80€"
                  }
                ]
            }
        })

    #print(j)

    jj = json.loads(j)
    

    #print(jj['monday'])
                                    
             
        
            
    
    
    dailyMenu = weekMenu.find('.title')

    menu = ''
    for dish in dailyMenu:
        menu += dish.text + '\nl'
        
        #print(dish.text)
    #print(dailyMenu.text)

    

def handle(msg):
    pprint(msg)
    print(msg['text'])

    msg_text = msg['text']

    user_id = msg['from']['id']

    print(user_id)
    
    if 'menu' in msg_text or 'Menu' in msg_text:
        #getCurrentWeekMenu()
        sendMessage(user_id, msg_text)


def sendMessage(user_id, text):
    bot.sendMessage(user_id, text)

MessageLoop(bot, handle).run_as_thread()




dailyScheduler = BlockingScheduler()

#run requestBitcoin() function once every 60 seconds
#dailyScheduler.add_job(requestBitCoin, 'interval', seconds=60)

#dailyScheduler.start()
