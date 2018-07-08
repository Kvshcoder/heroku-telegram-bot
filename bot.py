# -*- coding: utf-8 -*-
import redis
import os
import telebot
import re
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

# import some_api_lib
# import ...

# Example of your code beginning
#           Config vars
token = os.environ['token']
tgadmin = os.environ['adminkey']
#some_api_token = os.environ['SOME_API_TOKEN']
#             ...

# If you use redis, install this add-on https://elements.heroku.com/addons/heroku-redis
#r = redis.from_url(os.environ.get("REDIS_URL"))

#       Your bot code below
bot = telebot.TeleBot(token)
# some_api = some_api_lib.connect(some_api_token)
#              ...

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
		print("kicked the bot by some one from a group named "+message.chat.title)
		bot.send_message(tgadmin, "*I was kicked by someone from group* "+message.chat.title,parse_mode='Markdown')
		
'''@bot.message_handler(func=lambda message: True)
def totext_all(message):
	print("writing to text")
	gtext=message.text
	gchatid =message.chat.id
	gchat_fname = message.chat.first_name
	try:
		gchat_lname = message.chat.last_name
	except:
		gchat_lname = " - "
	try:
		gchatusrname = message.chat.username
	except:
		gfchatusrname = "  - "
	try:
		gtitle = message.chat.title
	except:
		gtitle = ("*its_empty*")
	gfromusr_id	= message.from_user.id
	gfromusr_fname = message.from_user.first_name
	try:
		gfromusr_lname = message.from_user.last_name
	except:
		gfromusr_lname = "  - "
	try:
		gfromusrname = message.from_user.username
	except:
		gfromusrname = " - "
	
	dumping_data=("| "+str(gtitle)+" "+str(gchatid)+" "+str(gchatusrname)+" "+str(gchat_fname)+" "+str(gchat_lname)+" "+str(gfromusr_id)+" "+str(gfromusrname)+" "+gfromusr_fname+" "+str(gfromusr_lname)+" \n "+gtext+" |  \n \n")
	
	bot.send_message(tgadmin, dumping_data,parse_mode='Markdown')
'''	
@bot.message_handler(func=lambda message: True)
def findwords(message):
	print("find words triggered!")
	uwu_words= re.compile('uwu',re.IGNORECASE)
	owo_words= re.compile('owo',re.IGNORECASE)
	joreh_words = re.compile('joreh',re.IGNORECASE)
	joreh_hi= re.compile('hi|hello|hola|bonjour|ahoy|howdy|aloha|whats up',re.IGNORECASE)
	joreh_hi_match = re.findall(r'hi|hello|hola|bonjour|ahoy|howdy|aloha|whats up',message.text,re.IGNORECASE)
	try:
		message_chat_type = message.chat.type
	except:
		message_chat_type = "-"
	if uwu_words.search(message.text):
		print("The UwU word Found")
		data = "*UwU*"
		bot.send_message(message.chat.id, data,parse_mode='Markdown')
	elif owo_words.search(message.text):
		print("The OwO word Found")
		data = "*OwO*"
		bot.send_message(message.chat.id, data,parse_mode='Markdown')
	elif (joreh_hi.search(message.text) and message_chat_type =="private"):
		print("Hi word in priavte chat Found")
		try:
			gfromusr_lname = message.from_user.last_name
		except:
			gfromusr_lname = "  - "
		data = "*"+" "+ str(joreh_hi_match[0])+"! "+message.from_user.first_name+" "+gfromusr_lname +"*"
		bot.reply_to(message, data,parse_mode='Markdown')
	elif joreh_words.search(message.text):
		print("The Joreh words Found")
		if joreh_hi.search(message.text):
			print("Hi word Found")
			try:
				gfromusr_lname = message.from_user.last_name
			except:
				gfromusr_lname = "  - "
			data = "*"+" "+ str(joreh_hi_match[0])+"! "+message.from_user.first_name+" "+gfromusr_lname +"*"
		else:
			data = "*I am Here!*"
		bot.reply_to(message, data,parse_mode='Markdown')
	else :
		print("Nothing Found")
		
	
bot.polling()
