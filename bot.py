# -*- coding: utf-8 -*-
import redis
import os
import telebot
# import some_api_lib
# import ...

# Example of your code beginning
#           Config vars
token = os.environ['token']
#some_api_token = os.environ['SOME_API_TOKEN']
#             ...

# If you use redis, install this add-on https://elements.heroku.com/addons/heroku-redis
#r = redis.from_url(os.environ.get("REDIS_URL"))

#       Your bot code below
bot = telebot.TeleBot(token)
# some_api = some_api_lib.connect(some_api_token)
#              ...
tgadmin=385390931
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
	print("welcome triggered")
	bot.reply_to(message, "*Help and Start Triggered*",parse_mode='Markdown')
@bot.message_handler(content_types=['new_chat_members'])
def user_joined_greet(message):
	print("group Joined Welcome triggered")
	if message.new_chat_member.id != bot.get_me().id:
		print("group Joined Welcome triggered 2")
		f_name = message.new_chat_member.first_name
		title = message.chat.title
		try:
			l_name=message.new_chat_member.last_name
			newmember=str(f_name+" "+l_name)
		except:
			l_name=" "
			newmember=str(f_name)
		bot.send_message(message.chat.id, "`ආයුබෝවන්` " + "_"+newmember+ "_"+ "`..  ඔබව` "+ "*"+title+"*" + "` වෙත සාදරයෙන් පිළිගනිමු 🙏`",parse_mode='Markdown')
	else:
		title = message.chat.title
		print("added to a new group named "+title)
		bot.send_message(tgadmin, "*I was added by someone to group* "+title,parse_mode='Markdown')
		
@bot.message_handler(content_types=['left_chat_member'])
def user_leave_greet(message):
	if message.left_chat_member.id != bot.get_me().id:
		print("group left curse triggered")
		f_name = message.left_chat_member.first_name
		title = message.chat.title
		try:
			l_name=message.left_chat_member.last_name
			leftmember=str(f_name+" "+l_name)
		except:
			l_name=" "
			leftmember=str(f_name)
		bot.send_message(message.chat.id, "*"+title+"*` හි සිටි `_"+leftmember+"_` වන තෝ හිටියත් එකයි! නැතත් එකයි!  👋..`",parse_mode='Markdown')
	else:
		title = message.chat.title
		print("kicked the bot by some one from a group named "+title)
		bot.send_message(tgadmin, "*I was kicked by someone from group* "+title,parse_mode='Markdown')
		
@bot.message_handler(func=lambda message: True)
def check_all(message):
	print("check_all triggered")
     tgtext=message.text
     splitwords=tgtext.split()
     for i in splitwords
	 bot.reply_to(message, i)

bot.polling()
