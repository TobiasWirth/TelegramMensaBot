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
import datetime

#create Bot
bot = telepot.Bot('838947615:AAH6WV9wKS-EIOmRL04zgHOSPgBih09fUWE')

bot.getMe()

session = HTMLSession()


#def returnFood(day):

jsonCurrentWeekMarkushaus = None
jsonCurrentWeekFeki       = None


def getCurrentWeekMenu():
    #r = session.get('https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/speiseplaene/interimsmensa-markusplatz-bamberg.html')
    
    #currentWeekMarkushaus = r.html.find('.week.currentweek', first=True)

    #r = session.get('https://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/speiseplaene/mensa-feldkirchenstrasse-bamberg.html')
    r = session.get('https://web.archive.org/web/20171017053414/http://www.studentenwerk-wuerzburg.de/bamberg/essen-trinken/speiseplaene.html?tx_thmensamenu_pi2%5Bmensen%5D=3&tx_thmensamenu_pi2%5Baction%5D=show&tx_thmensamenu_pi2%5Bcontroller%5D=Speiseplan&cHash=c3fe5ebb35e5fba3794f01878e798b7c')
    currentWeekFeki = r.html.find('.week.currentweek', first = True)

  
    #weekDaysMarkushaus = currentWeekMarkushaus.find(".day")
    weekDaysFeki       = currentWeekFeki.find(".day")

    #dayListMarkushaus = []
    dayListFeki       = []


    now = datetime.datetime.now()

    
    

    #Build JSON for Markushaus menu
    #for day in weekDaysMarkushaus:
       
     #   title = day.find(".title", first=True)
      #  price = day.find(".price span", first=True)

        

       # dayJson = json.dumps({
        #    "title": title.text,
         #   "price": price.text + "€"
            
          #  })

        #dayListMarkushaus.append(dayJson)

    #Build JSON for Fekimensa menu
    for day in weekDaysFeki:

         titles = day.find(".title")
         prices = day.find(".price span")

    

        dict_feki = {
            "monday" : [["Fisch", "2,80"], ["Fleisch", "3,40"], ["Burger", "3,20"]],
            "tuesday": [[],[],[],[]]
            "wednesday": [[],[],[],[]]
            "thursday": [[],[],[],[]]
            "friday": [[],[],[],[]]
         

         menu = ""
         i = 0
         for title in titles:
             #menu += "{ title: " + title.text + ", price: " + prices[i].text + "€ },"
             menu += "{" + '\'title\':' + title.text + "," + "\'price\': 2,80€"+ "}" +","
             menu = menu.strip('"\'')
             i+=1


         #print(menu)
         #print(menu[:-1])

         print(type(menu))

         menu = menu[:-1]
         menu = menu.strip('\"\'')

         print(type(menu))

         dayJson = json.dumps({
             "menu": [  menu  ]
            })

         print(dayJson)

         dayListFeki.append(dayJson)

        
             
    
    #global jsonCurrentWeekMarkushaus
    global jsonCurrentWeekFeki

    #jsonCurrentWeekMarkushaus = dayListMarkushaus[0]

    jsonCurrentWeekFeki = dayListFeki[0]


    #print(dayListFeki)

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

        

def handle(msg):
    pprint(msg)
    print(msg['text'])

    msg_text = msg['text']


    user_id = msg['from']['id']

    print(user_id)
    
    if 'menu' in msg_text or 'Menu' in msg_text:
        getCurrentWeekMenu()
        #global jsonCurrentWeekMarkushaus
        global jsonCurrentWeekFeki

        #jsonCurrentWeekMarkushaus = json.loads(jsonCurrentWeekMarkushaus)
        jsonCurrentWeekFeki = json.loads(jsonCurrentWeekFeki)
        #jsonCurrentWeekFeki = jsonCurrentWeekFeki

        #testitest = jsonCurrentWeekMarkushaus['title'] + " " + jsonCurrentWeekMarkushaus['price']

        feki = jsonCurrentWeekFeki['title'] + " " + jsonCurrentWeekFeki['price']

        sendMessage(user_id, feki)


def sendMessage(user_id, text):
    bot.sendMessage(user_id, text)

MessageLoop(bot, handle).run_as_thread()


#def main():
    






dailyScheduler = BlockingScheduler()

#run requestBitcoin() function once every 60 seconds
#dailyScheduler.add_job(requestBitCoin, 'interval', seconds=60)

#dailyScheduler.start()

#if __name__== "__main__":
#	main()
