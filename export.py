# -*- coding: utf-8 -*-
import requests
import json
import re
import urllib

client_id="170237838334492682" #seems to be the blarg.xyz client id
serverid=""
blargauthdone=False
session = requests.Session()


def blargauth():
	global serverid
	global session
	print("doing blargauth")
	f=open("credentials.txt")
	login=f.readline().strip()
	password=f.readline().strip()
	if serverid=="":
		serverid=f.readline().strip()
	f.close()
	headers={"Content-Type":"application/json"}
	payload="{{\"email\":\"{}\",\"password\":\"{}\"}}".format(login,password)

	r = session.post('https://discordapp.com/api/v6/auth/login', data=payload,headers=headers)
	token=json.loads(r.text)["token"]

	headers["Authorization"]=token
	payload2="{\"permissions\":0,\"authorize\":true}"
	r = session.post('https://discordapp.com/api/v6/oauth2/authorize?client_id=170237838334492682&redirect_uri=https%3A%2F%2Fblargbot.xyz%2Fcallback&response_type=code&scope=identify%20guilds&prompt=consent',data=payload2,headers=headers)
	callbackurl=json.loads(r.text)["location"]

	session.get(callbackurl)

def save(tagname,content,session,serverid):
	global blargauthdone
	if not blargauthdone:
		blargauth()
		blargauthdone=True
	headersblarg={"Content-Type":"application/x-www-form-urlencoded"}
	payload3="tagName={}&newname=&action={}&destination={}&fontsize=20&content={}".format(tagname,"save",serverid,urllib.parse.quote(content)).encode("utf-8")
	r=session.post('https://blargbot.xyz/tags/editor',data=payload3,headers=headersblarg)
	print("save response {}".format(r.status_code))

def load(tagname,session,serverid):
	global blargauthdone
	if not blargauthdone:
		blargauth()
		blargauthdone=True
	headersblarg={"Content-Type":"application/x-www-form-urlencoded"}
	payload3="tagName={}&newname=&action={}&destination={}&fontsize=20".format(tagname,"load",serverid)
	r= session.post('https://blargbot.xyz/tags/editor',data=payload3,headers=headersblarg)
	#print(r.text)
	result = re.search('let startText = "(.*)";', r.text)
	f=open("{}.bbtag".format(tagname),"w")
	f.write(result.group(1).replace("\\r\\n","\n"))

def gitsave(giturl,session,serverid,tagname=[]):
	r=requests.get(giturl)
	gitjson=json.loads(r.text)
	for tag in gitjson:
		if "bbtag" in tag["name"]:
			name=tag["name"].split(".")[0]
			if len(tagname)==0 or name in tagname:
				print("saving {}".format(name))
				r2=requests.get(tag["download_url"])
				save(name,r2.text,session,serverid)

def backup(list,session,serverid):
	for item in list:
		load(item,session,serverid)



#load("getfromgit",session,serverid)
#save("getfromgit2","test321",session,serverid)
gitsave("https://api.github.com/repos/spirgiuz/bso_discord/contents/blargbot",session,serverid,["adjustrs"])
#backup(["afk","jordan","joined"],session,serverid)

