# -*- coding: utf-8 -*-
import redis
import os
import telebot
import re
import psycopg2
import sys
from datetime import datetime

# import some_api_lib
# import ...
from ibm_botocore.client import Config
import ibm_boto3
api_key = os.environ['cos_api_key']
service_instance_id = os.environ['cos_resource_instance_id']
auth_endpoint = 'https://iam.bluemix.net/oidc/token'
service_endpoint = 'https://s3.us-east.objectstorage.softlayer.net'
cos_client = ibm_boto3.client('s3',
                      ibm_api_key_id=api_key,
                      ibm_service_instance_id=service_instance_id,
                      ibm_auth_endpoint=auth_endpoint,
                      config=Config(signature_version='oauth'),
                      endpoint_url=service_endpoint)
Buckets_list=cos_client.list_buckets()
print(Buckets_list)
object_list=cos_client.list_objects(Bucket="kvsh")
print(object_list)
def get_bucket_contents(bucket_name):
    print("Retrieving bucket contents from: {0}".format(bucket_name))
    try:
        files = cos_client.Bucket(bucket_name).objects.all()
        for file in files:
            print("Item: {0} ({1} bytes).".format(file.key, file.size))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve bucket contents: {0}".format(e))
get_bucket_contents(bucket_name="kvsh")
# Example of your code beginning
#           Config vars
token = os.environ['token']
tgadmin = os.environ['adminkey']
DATABASE_URL = os.environ['DATABASE_URL']

#some_api_token = os.environ['SOME_API_TOKEN']
#             ...

# If you use redis, install this add-on https://elements.heroku.com/addons/heroku-redis
#r = redis.from_url(os.environ.get("REDIS_URL"))

#       Your bot code below
bot = telebot.TeleBot(token)
# some_api = some_api_lib.connect(some_api_token)
#              ...
conn = None
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
		todbsendtext("*"+title+"*` හි සිටි `_"+leftmember+"_` වන තෝ හිටියත් එකයි! නැතත් එකයි!  👋..`",message)
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
	todbtext(message)
	data="https://images5.alphacoders.com/836/836124.jpg"
	bot.send_document(message.chat.id, data)
	todbsendtext(data,message)


@bot.message_handler(func=lambda message: True)
def findwords(message):
	todbtext(message)
	print("find words triggered!")
	bot.send_chat_action(message.chat.id, 'typing')
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
		todbsendtext(data,message)
	elif owo_words.search(message.text):
		print("The OwO word Found")
		data = "*OwO*"
		bot.send_message(message.chat.id, data,parse_mode='Markdown')
		todbsendtext(data,message)
	elif (joreh_hi.search(message.text) and message_chat_type =="private"):
		print("Hi word in priavte chat Found")
		try:
			gfromusr_lname = message.from_user.last_name
		except:
			gfromusr_lname = "  - "
		data = "*"+" "+ str(joreh_hi_match[0])+"! "+message.from_user.first_name+" "+gfromusr_lname +"*"
		bot.reply_to(message, data,parse_mode='Markdown')
		todbsendtext(data,message)
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
		todbsendtext(data,message)
	else :
		print("Nothing Found")


bot.polling(none_stop= True)
