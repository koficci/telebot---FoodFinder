import os
import telebot
from dotenv import load_dotenv
import sqlite3
import random

load_dotenv()
API_KEY = os.getenv("API_KEY")
bot = telebot.TeleBot(API_KEY)

#commands
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Hello, Welcome to FoodFinder!\nPlease enter a command to get started, or use /help to see the list of commands.")


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, "You may find places by using the following list of commands:\n\n/all - to see all possible places\n/location - to filter by place\n/type - to filter by type of place (cafe etc.)\n/random - to randomly suggest a place")


@bot.message_handler(commands=["all"])
def all(message):
    db = sqlite3.connect("filter.db")

    query = '''
SELECT PlaceName, PlaceLocation, StationName, PlaceType  
FROM Place
'''

    cursor = db.execute(query)
    data = cursor.fetchall()
    db.close()
    
    #if return is too long
    extra = []
    complete = False
    if len(data)>40:
        tempdata = data
        data = []
        for i in range(0,40):
            data.append(tempdata[i])
        for i in range(40,len(tempdata)):
            extra.append(tempdata[i])
            
    places = ''
    for i in data:
        temp = i[0] + "\nLocation: " + i[1] + "\nNearest Station: " + i[2] + "\nType: " + i[3] +"\n\n"
        places += temp

    if len(extra)==0:
        complete = True

    bot.send_message(message.chat.id, places) 
    
    while complete != True:
        data = extra
        extra = []
        if len(data)>40:
            tempdata = data
            data = []
            for i in range(0,40):
                data.append(tempdata[i])
            for i in range(40,len(tempdata)):
                extra.append(tempdata[i])
            
        places = ''
        for i in data:
            temp = i[0] + "\nLocation: " + i[1] + "\nNearest Station: " + i[2] + "\nType: " + i[3] +"\n\n"
            places += temp

        bot.send_message(message.chat.id, places) 
        
        if len(extra)==0:
            complete = True


@bot.message_handler(commands=["location"])
def location(message):
    msg = bot.send_message(message.chat.id, "Please provide the MRT station of the area you want to look at")
    bot.register_next_step_handler(msg,filterlocation)

def filterlocation(message):
    input = message.text
    temp = input.lower().split(' ')
    msg = []
    for i in temp:
        msg.append(i[0].upper() + i[1:])
    input = msg[0]
    if len(msg) > 1:
        for i in range(1,len(msg)):
            input += ' ' + msg[i]
    
    db = sqlite3.connect("filter.db")
    query = '''
SELECT PlaceName, PlaceLocation, StationName, PlaceType  
FROM Place
WHERE StationName = (?)
'''

    cursor = db.execute(query,(input,))
    data = cursor.fetchall()
    db.close()
    
    if len(data) == 0:
        bot.send_message(message.chat.id, "No such station exists")
        return location(message)
    
    places = ''
    for i in data:
        temp = i[0] + "\nLocation: " + i[1] + "\nNearest Station: " + i[2] + "\nType: " + i[3] +"\n\n"
        places += temp

    bot.send_message(message.chat.id, places)


@bot.message_handler(commands=["type"])
def type(message):
    msg = bot.send_message(message.chat.id, "Please choose from the following types of places:\n- Bar\n- Cafe\n- Casual Dining\n- Fancy Dining\n- Food Stall")
    bot.register_next_step_handler(msg, filtertype)

def filtertype(message):
    input = message.text
    temp = input.lower().split(' ')
    msg = []
    for i in temp:
        msg.append(i[0].upper() + i[1:])
    input = msg[0]

    if len(msg) > 1:
        for i in range(1,len(msg)):
            input += msg[i]  

    db = sqlite3.connect("filter.db")
    query = '''
SELECT PlaceName, PlaceLocation, StationName, PlaceType  
FROM Place
WHERE PlaceType = (?)
'''

    cursor = db.execute(query,(input,))
    data = cursor.fetchall()
    db.close()
   
    #if invalid type
    if len(data) == 0:
        bot.send_message(message.chat.id, "Invalid Type")
        return type(message)
    
    #if return is too long
    extra = []
    complete = False
    if len(data)>40:
        tempdata = data
        data = []
        for i in range(0,40):
            data.append(tempdata[i])
        for i in range(40,len(tempdata)):
            extra.append(tempdata[i])
            
    places = ''
    for i in data:
        temp = i[0] + "\nLocation: " + i[1] + "\nNearest Station: " + i[2] + "\nType: " + i[3] +"\n\n"
        places += temp

    if len(extra)==0:
        complete = True

    bot.send_message(message.chat.id, places) 
    
    while complete != True:
        data = extra
        extra = []
        if len(data)>40:
            tempdata = data
            data = []
            for i in range(0,40):
                data.append(tempdata[i])
            for i in range(40,len(tempdata)):
                extra.append(tempdata[i])

        places = ''
        for i in data:
            temp = i[0] + "\nLocation: " + i[1] + "\nNearest Station: " + i[2] + "\nType: " + i[3] +"\n\n"
            places += temp

        bot.send_message(message.chat.id, places) 

        if len(extra)==0:
            complete = True




@bot.message_handler(commands=["random"])
def randomplace(message):
    db = sqlite3.connect("filter.db")

    query = '''
SELECT PlaceName, PlaceLocation, StationName, PlaceType  
FROM Place
'''

    cursor = db.execute(query)
    data = cursor.fetchall()
    db.close()

    temp = random.choice(data)
    place = temp[0] + "\nLocation: " + temp[1] + "\nNearest Station: " + temp[2] + "\nType: " + temp[3]

    bot.send_message(message.chat.id, place)

bot.polling()