# from telegram import Update
# from telegram.ext import *
# import firebase_admin
# from firebase_admin import credentials, db, firestore

# cred = credentials.Certificate("castornow.json")
# firebase_admin.initialize_app(cred, name='app')
# DEFAULT_APP = firebase_admin.initialize_app(cred, {
#     'databaseURL': "https://castor-order-booking-bot-default-rtdb.firebaseio.com"
# })
# firestore_client = firestore.client()
# ref_menu = db.reference("/Menu")
# ref_combo = db.reference("/Combo")
# # API_TOKEN = "5742295256:AAF4wpyXMjuQcbXH-mARmjOK7BjmbPiR9Oc"

# async def start(update, context):
#     await update.message.reply_text("Hello, Welcome to the Cafe")

# async def menu(update,context):
#     arr='''Here's the menu\n'''
#     cafe_menu=ref_menu.get()
#     for key in cafe_menu:
#         menu_key=cafe_menu[key]
#         ans+=menu_key['Name']+'\n'
#     await update.message.reply_text(ans)

# async def combo(update,context):
#     ans='''Here's are combos\n'''
#     count=1
#     combo_menu=ref_combo.get()
#     for key in combo_menu:
#         ans+='COMBO'+str(count)
#         combo=combo_menu[key]
#         ans+='\n'+'\t'+combo['i1']+'\n'+combo['i2']+'\n'+combo['i3']+'\n'
#         count+=1
#     await update.message.reply_text(ans)

# async def reply(update, context):
#     query = update.message.text.lower()
#     user_name = update.effective_user.first_name
#     replies1 = {
#         "hi": f"Hello, {user_name}",
#         "how are you?": "I'm fine thank you.",
#         "how are you": "I'm fine thank you",
#         "what's your name?": "My name is CodeCafe.",
#         "whats your name": "My name is CodeCafe.",
#         "what's your name?": "My name is CodeCafe.",
#         "bye": "See you!"
#     }
#     replies2 = [
#         "whats the menu",
#         "Whats all you have in menu",
#         "Please display menu"
#     ]
#     flag=0
#     for key, value in replies1.items():
#         if flag==0 and query in key :
#             flag=1
#             await update.message.reply_text(value)
#             break
#     for key in replies2:
#         if flag==0 and query in key:
#             flag=1
#             # await menu(update,context)
#             await combo(update,context)
#             break
#     if flag==0 :
#         await update.message.reply_text("I didn't get you")


# def main():
#     global api
#     api = "5742295256:AAF4wpyXMjuQcbXH-mARmjOK7BjmbPiR9Oc"
#     updater = Updater(api, True)
#     app = Application.builder().token(api).build()
#     app.add_handler(CommandHandler('start', start))
#     app.add_handler(MessageHandler(filters.TEXT, reply))
#     app.run_polling(1.0)
#     app.idle()

import telebot
from apscheduler.schedulers.blocking import BlockingScheduler
from telebot import types
import re
from datetime import datetime
from bob_telegram_tools.bot import TelegramBot
import matplotlib.pyplot as plt
import firebase_admin
from firebase_admin import credentials,db,firestore

cred = credentials.Certificate("castornow.json")
firebase_admin.initialize_app(cred,name='app')
DEFAULT_APP = firebase_admin.initialize_app(cred, {
  'databaseURL': "https://castor-order-booking-bot-default-rtdb.firebaseio.com"
})
firestore_client = firestore.client()
ref_menu = db.reference("/Menu")
ref_combo = db.reference("/Combo")
ref_order = db.reference("/Order")
API_TOKEN = "5742295256:AAF4wpyXMjuQcbXH-mARmjOK7BjmbPiR9Oc"

bot = telebot.TeleBot(API_TOKEN)

def reply(message):
    global msg
    query = message.text.lower()
    # user_name = message.first_name
    replies1 = {
        "hi": "Hello",
        "how are you?": "I'm fine thank you.",
        "how are you": "I'm fine thank you",
        "what's your name?": "My name is CodeCafe.",
        "whats your name": "My name is CodeCafe.",
        "what's your name?": "My name is CodeCafe.",
        "bye": "See you!"
    }
    replies2 = [
        "whats the menu",
        "Whats all you have in menu",
        "Please display menu"
    ]
    flag=0
    for key, value in replies1.items():
        if flag==0 and query in key :
            flag=1
            msg=bot.send_message(message.chat.id,value)
            break
    for key in replies2:
        if flag==0 and query in key :
            flag=1
            ans='''Here's the menu\n'''
            cafe_menu=ref_menu.get()
            for key in cafe_menu:
                menu_key=cafe_menu[key]
                ans+=menu_key['Name']+'\n'
            msg=bot.send_message(message.chat.id,ans)
                    # bot.register_next_step_handler(message,menu)
            break
def menu(message):
    ans='''Here's the menu\n'''
    cafe_menu=ref_menu.get()
    for key in cafe_menu:
        menu_key=cafe_menu[key]
        ans+=menu_key['Name']+'\n'
    msg=bot.send_message(message.chat.id,ans)
    # bot.register_next_step_handler(msg,combo)


def place_order(message):
    global today_date
    today_date=str(datetime.now())
    global ms
    order_tab=ref_order.get()
    for key in order_tab:
        ms=key
    global length
    length=order_tab[ms]['Order-id']
    msg=bot.send_message(message.chat.id,"What's your mobile number ")
    bot.register_next_step_handler(msg,take_mobile)
    
def take_mobile(message):
    global value
    value=message.text
    msg=bot.send_message(message.chat.id,"Enter your order ")
    bot.register_next_step_handler(msg,take_choice)

def take_choice(message):
    global choice
    choice=message.text.lower()
    # msg=bot.send_message(message.chat.id,"Enter your order ")
    bot.register_next_step_handler(message,take_order)
    

def take_order(message):
    global size_arr
    size_arr=''
    order_arr=''
    order_val=message.text
    order_arr+=order_val+','
    if(choice=="yes"):
        msg=bot.send_message(message.chat.id,"Enter the size ")
        bot.register_next_step_handler(msg,enter_size)
        choice=take_choice(msg).lower()
    else:
        added={"Date":today_date,"Order-id":length+1,"Phone-no":value,"Order":{"Order-value":order_arr,"Size":size_arr}}
        ref_order.push(added)
        msg=bot.send_message(message.chat.id,"Your order is placed ") 
        # msg=bot.send_message(message.chat.id,"Thanku for the order ")

def enter_size(message):
    size_val=message.text
    size_arr+=size_val+','
    msg=bot.send_message(message.chat.id,"Do you want anything else ? (YES/NO) ")
    bot.register_next_step_handler(msg,take_choice)

# def combo(message):
#     a='''Here's the combos\n'''
#     count=1
#     combo_menu=ref_combo.get()
#     for key in combo_menu:
#         a+='COMBO'+str(count)
#         combo=combo_menu[key]
#         a+='\n'+'\t'+combo['i1']+'\n'+combo['i2']+'\n'+combo['i3']+'\n'
#         count+=1
#     msg=bot.send_message(message.chat.id,a)

@bot.message_handler(func=place_order)
def display(message):
  pass
bot.enable_save_next_step_handlers(delay=2)
bot.polling()