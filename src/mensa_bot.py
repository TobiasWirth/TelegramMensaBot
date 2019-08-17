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

bot.getMe()

session = HTMLSession()

def getCurrentWeekMenu():
    r = session.get('https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/speiseplaene/interimsmensa-markusplatz-bamberg.html')
    weekMenu = r.html.find('.week.currentweek', first=True)

    dailyMenu = weekMenu.find('.title')

    menu = ''
    for dish in dailyMenu:
        menu += dish.text + '\nl'
        
        #print(dish.text)
    #print(dailyMenu.text)

    sendMessage(menu)

def handle(msg):
    pprint(msg)
    print(msg['text'])

    msg_text = msg['text']
    
    if(msg_text is 'menu' or 'Menu'):
        getCurrentWeekMenu()


def sendMessage(text):
    bot.sendMessage('678522773', text)

MessageLoop(bot, handle).run_as_thread()




dailyScheduler = BlockingScheduler()

#run requestBitcoin() function once every 60 seconds
#dailyScheduler.add_job(requestBitCoin, 'interval', seconds=60)

#dailyScheduler.start()
