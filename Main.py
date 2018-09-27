import discord
import asyncio
import os
from random import choice
from threading import Thread
from googletrans import Translator
from flask import Flask
from random import randint
import wolframalpha
import time
from async_timeout import timeout
import websockets
import ujson
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
import re
import sys
import aiohttp
from datetime import datetime
import datetime
import imdb
import lyricwikia
import urllib.parse
from pyfiglet import Figlet
import random
import subprocess
import string
import hashlib
from discord.utils import get
import socket

app = Flask(__name__)

translator = Translator()

wolfram = wolframalpha.Client(os.getenv('APP_ID'))

loop = asyncio.get_event_loop()

RPS_WINS = {'paper':'rock','rock':'scissors','scissors':'paper'}
execsessions=[]
execstdin={}

cmdnotfound = '''
__**I don't know that command!**__\nfor a list of commands:\n**/help**\nfor info on a command:\n**/more-help <command>**
'''

helpmessage = '''
**/pins <channel_id>** - Shows pinned messages
**/help <dm/web>** - Brings up this page
**/more-help <command>** - Help on certain commands
**/lyrics <artist>, <song>** - Shows lyrics to song
**/imdb <movie>** - Shows top actors based on query
**/ascii <text>** -  Shows ascii text based on your text
**/lmgtfy <search>** - Searches lmgtfy for your query
**/youtube <search>** - Searches youtube for your query
**/translate <destlang> <text>** - Translates a word
**/stack** - Pastes stackoverflow urls based on search
**/chat <text>** - Starts an AI conversation
**/rolldie <number>** - Rolls a die
**/ask <question>** - Answers a question
**/google <search>** - Searches your query from google
**/exec <lang> <code>** - Runs code
**/rps <rock/paper/scissors>** - Plays a rps game
**/emoji <emoji>** - Pastes an emoji from your query
**/info** - Brings up status information
**/poll <desc1> +<desc2> <etc.>** - Starts a poll
**/password <length>** - creates a random password
**/reverse <text>** - reverses text you input
'''

adminhelpmessage = '''
**/stop-bot** - Stops MessengerBot
**/presence <status> <description>** - Sets a bot status
**/pins <channel_id>** - Shows pinned messages from a channel
**/help <dm/web>** - Brings up normal help page
**/admin-help** - Brings up this page
**/src <dm/web>** - Shows source code
**/imdb <movie>** - shows top ten actors of movie based on query
**/lyrics <artist>, <song>** - shows lyrics to song based on query
**/lmgtfy <search>** - Searches lmgtfy for your query
**/youtube <search>** - Searches youtube for your query
**/translate <destlang> <text>** - Translates a word
**/say <text>** - Says text you type 
**/stack** - Pastes stackoverflow urls based on your search
**/chat <text>** - Starts an AI conversation
**/rolldie <number>** - Rolls a die
**/url <search>** - Pastes urls related to your query
**/ask <question>** - Answers a question
**/google <search>** - Searches your query from google
**/exec <lang> <code>** - Runs code
**/execinput <answer>** - Answers an input statement
**/rps <rock/paper/scissors>** - Plays a rps game
**/emoji <emoji>** - Pastes an emoji from your query
**/info** - brings up status information
**/speak <text>** - Sends a text-to-speech message
'''

commands = [
"pins",
"invite",
"help",
"more-help",
"src",
"lyrics",
"imdb",
"ascii",
"lmgtfy",
"youtube",
"translate",
"stack",
"chat",
"rolldie",
"ask",
"google",
"exec",
"rps",
"emoji",
"info",
"server",
"ping",
"hello",
"execinput",
"status",
"stop-bot",
"poll",
"password",
"reverse",
"hash",
"engine",
"sleep",
"dehash",
"userinfo",
"leave",
"roles",
"embed",
"ip-addr"
]

def tp(string):
		s = list(string)
		for i in s:
				sys.stdout.write(i)
				sys.stdout.flush()
				if i == "." or i == "!" or i == "?":
						time.sleep(0.15)
				elif i == ",":
						time.sleep(0.1)
				elif i == ":" or i == ";":
						time.sleep(0.07)
				elif i == "<" or i == ">" or i == "(" or i == ")":
						time.sleep(0.03)
				else:
						time.sleep(0.01)

def image(q):
	url=(f'https://www.google.com/search?safe=active&biw=1366&bih=623&tbm=isch&source=hp&ei=lxOhW7_sJqiD0wK15pqgBQ&q={q}')
	r = requests.get(url)
	html_doc = r.text
	soup = BeautifulSoup(html_doc)
	links = []
	for link in soup.find_all('a'):
		links.append((link.get('href')))
	return(links)

def google(q):
	r=requests.get(f'https://google.com/search?q={q}').text
	soup=BeautifulSoup(r)
	for a in soup.findAll('a'):
		if not a['href'].startswith('/url?q='):continue
		r=requests.get('https://google.com'+a['href'])
		return r.url
		break
def youtube(q):
	r=requests.get(f'https://youtube.com/search?q={q}').text
	soup=BeautifulSoup(r)
	for a in soup.findAll('a'):
		if not a['href'].startswith('/url?q='):continue
		r=requests.get('https://google.com'+a['href'])
		return r.url
		break

def stack(q):
	url=(f'https://stackexchange.com/search?q={q}')
	r = requests.get(url)
	html_doc = r.text
	soup = BeautifulSoup(html_doc)
	links = []
	for link in soup.find_all('a'):
		links.append((link.get('href')))

		question_links = [k for k in links if k and 'questions' in k] # Filter links that contain the string 'questions'

	pattern = re.compile('questions/\d') # Create pattern to search for

	question_links = filter(pattern.search, question_links) # Filter links which are questions and also followed by a numerical ID
	question_links = list(set(question_links)) # Remove duplicates
		
	return(question_links)

def readgoogle(q):
	url=google(q)
	if url.startswith('https://www.google.com'):return url
	r=requests.get(url)
	soup=BeautifulSoup(r.text)
	findallp=soup.findAll('p')
	if len(soup.findAll('a')) > 100:
		return url
	paragraphs=[]
	for p in findallp:
		paragraphs.append(p.text)
	data = '\n'.join(paragraphs)
	if len(data) > 2000:return url
	return data

def readstack(q):
	url=stack(q)
	if url.startswith('https://stackoverflow.com'):return url
	r=requests.get(url)
	soup=BeautifulSoup(r.text)
	findallp=soup.findAll('p')
	if len(soup.findAll('a')) > 100:
		return url
	paragraphs=[]
	for p in findallp:
		paragraphs.append(p.text)
	data = '\n'.join(paragraphs)
	if len(data) > 2000:return url
	return data

def send_messages_thread():
	print('Thread created')
	loop = asyncio.new_event_loop()
	while True:
		try:
			newmessage = input('> ')
			task1 = client.loop.create_task(client.send_typing(messagechannel))
			task2 = client.loop.create_task(client.send_message(messagechannel, newmessage))
			asyncio.ensure_future(task1)
			asyncio.ensure_future(task2)
		except Exception as e:
			print('Error:', e)

async def runcode(code,language='python3',timeouttime=60,authorid=None):
	global execstdin
	print(1)
	try:
		async with aiohttp.ClientSession() as s:
			replittoken = await s.post('https://repl.it/data/repls/35a0ee83-68a1-416e-bafb-c45c765060bb/gen_repl_token')
			replittoken = await replittoken.json()
		async with timeout(timeouttime):
			async with websockets.connect('wss://eval.repl.it/ws') as ws:
				await ws.send(ujson.dumps({'command':'auth','data':replittoken}))
				authreturn=await ws.recv()
				await ws.send(ujson.dumps({'command':'select_language','data':language}))
				langreturn=ujson.loads(await ws.recv())
				if langreturn['command']=='error':
					yield langreturn['data']
				else:
					await ws.send(ujson.dumps({'command':'eval','data':code}))
					print('asdf')
					while True:
						try:
							#async with timeout(1):
							data=await ws.recv()
							data=ujson.loads(data)
							if data['command']=='event:loopback':
								print('ree',data)
								data=ujson.loads(data['data'])
						except Exception as e:
							print(e,type(e))
							data={}
						try:
							print(data)
							try:
								await ws.send(ujson.dumps({'command':'input','data':execstdin[authorid][0]+'\n'}))
								del execstdin[authorid][0]
								yield 'Recieved input'
							except:
								pass
							if data['command']=='output':
								yield data['data'].encode().decode('unicode_escape')
							elif data['command']=='result':
								print('result')
								try:yield data['error']
								except:pass
						except:
							pass
	except Exception as e:
		print(e)

rps = [
	"rock",
	"scissors",
	"paper",
]
			
answers = [
	"hello",
	"how are you",
	"nice to meet you",
	"glad to see you",
	"at your service",
	"we meet again",
	"how nice to see you",
	"i'm good",
	"it's wonderful talking to you",
	"welcome back",
	"how's it going",
	"yes",
	"no",
	"i don't know",
	"maybe",
	"hopefully",
	"it just is",
	"if you think so",
	"probably not",
	"why",
	"why not",
	"good",
	"great",
	"bleh",
	"whatever",
	"oh, ok",
	"ok",
	"i am",
	"if you say i am",
	"i will",
	"i'll try",
	"it is",
	"it isn't",
	"don't say that",
	"so are you",
	"if you think so",
	"right back at you",
	"that's what i thought",
	"twinsies",
	"are we telepathic",
	"great minds think alike",
	"i don't think so",
	"how could you say that",
	"because i said",
	"it's the only way",
	"i don't know",
	"the world will never know",
	"glad you think so",
	"come back soon",
	"remember to never edit my code again",
	"i don't think that's very nice",
	"that's not nice",
	"meanie",
	"you made me cry",
	"why'd you do that",
	"that wasn't sincere",
	"you're not very sincere",
	"i don't like your mouth",
	"you talk to your mother with that mouth",
	"wash your mouth with soap",
	"wash it out with soap",
	"you're being mean",
	"you're mean",
	"why are you being mean",
	"why are you mean",
	"english again",
	"it's english",
	"english yay",
	"it's english again yay",
	"what do you mean",
	"what are you trying to say",
	"dang it",
	"oh dang it",
	"gosh dang it",
	"darn it",
	"oh darn it",
	"gosh darn it"
]

client = discord.Client()

@app.route('/')
def run_forever():
		return 'Server Started!'

@client.event
async def on_message(message):
	await client.change_presence(game=discord.Game(name="/help"))
	global execsessions
	global execstdin
	if message.channel.id == messagechannel.id:print(f'{message.author}: {message.content}')
	prefix = '/'
	if not message.content.startswith(prefix):return
	if message.author.bot:return
	print(message.content)
	rawinput = message.content[len(prefix):]
	args = rawinput.split()
	cmd = args[0]
	args = args[1:]
	args1,args2=None,None
	try:
		args1 = rawinput.split(maxsplit=1)[1:][0]
		args2 = rawinput.split(maxsplit=2)[2:][0]
		args3 = rawinput.split(maxsplit=3)[3:][0]
	except:
		pass
		
	if cmd not in commands:
		cmdnotfoundmsg = discord.Embed(title='Error', description=f':no_entry_sign: Command `{cmd}` not found :no_entry_sign:', color=0xff0000)
		await client.send_message(message.channel, embed=cmdnotfoundmsg)
		
	elif cmd == "poll":
		regionalindicators = '🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯'
		letters = 'ABCDEFGHIJ'
		pollargs = ' '.join(args).split(' +')
		pollmsgargs=[]
		i=0
		for arg in pollargs:
			pollmsgargs.append(f'**{letters[i]}**: {arg}')
			i+=1
		pollmsgargs='\n'.join(pollmsgargs)
		pollmessage = f'''
		__{message.author.name}__ started a poll.
		{pollmsgargs}
		'''
		pollembed = discord.Embed(title=f"{message.author.name}'s poll".upper(), description="", color=0x0004ff)
		pollembed.add_field(name=f"#{message.channel.name}", value=pollmessage, inline=False)
		poll = await client.send_message(message.channel, embed=pollembed)
		i=0
		for _ in pollargs:
			await client.add_reaction(poll,regionalindicators[i])
			i+=1
			
	elif cmd == "engine":
		_, search = message.content.split(' ',1)

		text = search

		text = urllib.parse.quote_plus(text)

		url = 'https://www.google.com/search?q=' + text

		response = requests.get(url)

		soup = BeautifulSoup(response.text, 'html.parser')
		for g in soup.find(class_='g'):
			await client.send_message(message.channel, f"```{g.text}```")
			await client.send_message(message.channel, "```-------```")
	
	elif cmd == "sleep":
		_, amount = message.content.split(' ',1)
		amount = int(amount)
		await client.send_message(message.channel, f"{client.user.name} is **SLEEPING** for {amount} seconds!")
		time.sleep(amount)
		await client.send_message(message.channel,
		"""
:sunny:
**DONE SLEEPING!**
		""")

	elif cmd == 'hello':
		await client.send_message(message.channel, f'```Hello, {message.author.name}! Welcome to the {message.server.name} server! I am {client.user.name}! I was created by replitcode#9220 & mat#6207! Enjoy! :D```')
	
	elif cmd == "reverse":
		_, text = message.content.split(' ',1)
		await client.send_message(message.channel, str(text[::-1]))

	elif cmd == 'rolldie':
		_, num = message.content.split(' ',2)

		await client.send_typing(message.channel)

		await client.send_message(message.channel, "You rolled a " +	str(randint(1, int(num))))
	
	elif cmd == 'time':
		utc_datetime = datetime.datetime.utcnow()
		await client.send_message(message.channel, utc_datetime.strftime("%A, %B %d, %Y. %I:%M %p"))
	
	elif cmd == 'speak':
		_, desc = message.content.split(" ",1)
		await client.send_typing(message.channel)
		await client.send_message(message.channel, desc, tts=True)
	
	elif cmd == "userinfo":
		_, clientid = message.content.split(' ',1)
		await client.get_user_profile(clientid)
	
	elif cmd == "leave":
		await client.leave_server(client.get_server("437048931827056642"))

	elif cmd == 'src':
		await client.send_message(message.channel, 'Here is the source for MessengerBot:\nhttps://repl.it/@replitcode/MessengerBot-20')

	elif cmd == 'stack':
		_, q = message.content.split(' ',1)
		await client.send_typing(message.channel)
		await client.send_message(message.channel, stack(q))
	
	elif cmd == 'say':
		if message.author.id=='440231799533338634' or message.author.id=='224588823898619905' or message.author.id =='404813853851910155':
			_, say = message.content.split(' ',1)

			await client.send_typing(message.channel)

			await client.send_message(message.channel, say)
		else:
			await client.send_message(message.channel, "You can't use this command!")

	elif cmd == 'chat':
		_, chat = message.content.split(' ',1)

		await client.send_message(message.channel, "**TIP**: After you do the initial `/chat` you can say stuff without doing that command")
		
		while True:
			await client.send_typing(message.channel)
			await client.send_message(message.channel, choice(answers))
			msg = await client.wait_for_message(author=message.author)
			if msg.content.lower().startswith("bye"):
				await client.send_message(message.channel, message.author.name + "'s conversation has successfully ended")
				break
	
	elif cmd == 'imdb':
		_, q = message.content.split(' ',1)
		await client.send_message(message.channel, "**ACTORS IN: **" + q.upper())
		ia = imdb.IMDb()
		search_movie = q
		search_results = ia.search_movie(search_movie)

		if search_results:
			movieID = search_results[0].movieID
			movie = ia.get_movie(movieID)
			if movie:
				cast = movie.get('cast')
				topActors = 10
				for actor in cast[:topActors]:
					await client.send_message(message.channel, "{0}".format(actor['name'], actor.currentRole))
	
	elif cmd == 'lyrics':
		print('parsing message')
		artist, song = ' '.join(args).split(',')
		await client.send_message(message.channel, "Sent lyrics for **" + song.upper() + "** by **" + artist.upper() + "**")
		print('getting lyrics')
		lyrics = lyricwikia.get_lyrics(artist, song)
		print(f'got lyrics, {len(lyrics)} chars long')
		for chunk in [lyrics[i:i+1999] for i in range(0, len(lyrics), 1999)]:
			print('sending lyric chunk')
			await client.send_message(message.author, "**LYRICS:\n**" + "```" + chunk + "```")

	elif cmd == 'rps':
		_, role = message.content.split(' ',1)
		if role.lower() not in rps:
			await client.send_message(message.channel, "that's not allowed " + message.author.name)
			return
		comp = choice(rps)
		await client.send_message(message.channel, comp)
		if role.lower() == comp:
			await client.send_message(message.channel, "we tied " + message.author.name)
		elif RPS_WINS[role.lower()] == comp:
			await client.send_message(message.channel,	message.author.name + " wins")
		elif RPS_WINS[comp] == role.lower():
			await client.send_message(message.channel, message.author.name + " loses")
		
	elif cmd == 'translate':
		_, destlang, text = message.content.split(' ',2)

		yourlang = translator.detect(text).lang
		
		answer = translator.translate(text, src=yourlang, dest=destlang).text

		await client.send_typing(message.channel)

		await client.send_message(message.channel, answer)
	
	elif cmd == "help":
		helpembed = discord.Embed(title="", description="", color=0x00ffcb)
		helpembed.add_field(name="COMMANDS", value=helpmessage, inline=False)
		await client.send_message(message.channel, embed=helpembed)
	
	elif cmd == 'more-help':
		_, cmd = message.content.split(' ',1)
		helpembed = discord.Embed(title="", description="", color=0x00ffcb)
		helpembed.add_field(name="COMMANDS", value=helpmessage, inline=False)
	
		if cmd=="pins":
			await client.send_message(message.channel, """
This command allows you to see the pinned messages in a certain channel!
__HOW TO USE:__
**/pins <channel_id>**
			""")
		elif cmd=="invite":
			await client.send_message(message.channel, """
This command allows you to invite MessengerBot to your server!!
__HOW TO USE:__
**/invite**
			""")
		elif cmd=="help":
			await client.send_message(message.channel, """
This command allows you to see the commands for MessengerBot!
__HOW TO USE:__
**/help <optional_command>**
			""")
		elif cmd=="more-help":
			await client.send_message(message.channel, """
This command allows you to further your knowledge of MessengerBot's commands
__HOW TO USE:__
**/more-help <command>**
			""")
		elif cmd=="src":
			await client.send_message(message.channel, """
This command allows you to see the source for MessengerBot
__HOW TO USE:__
**/src**
			""")
		elif cmd=="ping":
			await client.send_message(message.channel, """
This command allows you to see if MessengerBot is active or not!
__HOW TO USE:__
**/ping**
			""")
		elif cmd=="lyrics":
			await client.send_message(message.channel, """
This command allows you to see lyrics for a certain song!
__HOW TO USE:__
**/lyrics <artist>, <song>**
			""")
		elif cmd=="imdb":
			await client.send_message(message.channel, """
This command allows you to see actors in a certain movie!
__HOW TO USE:__
**/imdb <movie>**
			""")
		elif cmd=="ascii":
			await client.send_message(message.channel, """
This command allows you to get the ascii version of text you send!
__HOW TO USE:__
**/ascii <text>**
			""")
		elif cmd=="lmgtfy":
			await client.send_message(message.channel, """
This command gives a lmgtfy url for the query you gave.
__HOW TO USE:__
**/lmgtfy <query>**
			""")
		elif cmd=="youtube":
			await client.send_message(message.channel, """
This command gives a url for youtube for the query you gave
__HOW TO USE:__
**/youtube <query>**
			""")
		elif cmd=="translate":
			await client.send_message(message.channel, """
This command allows you to translate text into almost a hundred languages
__HOW TO USE:__
**/translate <destlang> <text>**
			""")
		elif cmd=="stack":
			await client.send_message(message.channel, """
This command allows you to see stack overflow urls for the query you gave.
__HOW TO USE:__
**/stack <query>**
			""")
		elif cmd=="chat":
			await client.send_message(message.channel, """
This command allows you to have an AI conversation with MessengerBot
__HOW TO USE:__
**/chat <text>**
**TIP: after you do the initial */chat* you can do text without it!
			""")
		elif cmd=="rolldie":
			await client.send_message(message.channel, """
This command allows you to roll a die.
__HOW TO USE:__
**/rolldie <number>**
			""")
		elif cmd=="ask":
			await client.send_message(message.channel, """
This command allows you to ask a question from the search engine Wolfram|Alpha
__HOW TO USE:__
**/ask <question>**
			""")
		elif cmd=="google":
			await client.send_message(message.channel, """
This command allows you to search google for a query you give.
__HOW TO USE:__
**/google <search>**
			""")
		elif cmd=="exec":
			await client.send_message(message.channel, """
This command allows you to run code for any language not run on javascript.
__HOW TO USE:__
**/exec <language> <code>**
			""")
		elif cmd=="rps":
			await client.send_message(message.channel, """
This command allows you to play an rps game with MessengerBot
__HOW TO USE:__
**/rps <rock/paper/scissors>**
			""")
		elif cmd=="emoji":
			await client.send_message(message.channel, """
This command allows you to send an emoji on discord.
__HOW TO USE:__
**/emoji <emoji>**
			""")
		elif cmd=="info":
			await client.send_message(message.channel, """
This command allows you to see current info for the discord channel/server and even about you and MessengerBot.
__HOW TO USE:__
**/info**
			""")
		elif cmd=="server":
			await client.send_message(message.channel, """
This command allows you to join MessengerBot's support server.
__HOW TO USE:__
**/server**
			""")
		elif cmd=="poll":
			await client.send_message(message.channel, """
This command allows you to start a poll on discord!
__HOW TO USE:__
**/poll +<desc1> +<desc2>**
			""")
		elif cmd=="password":
			await client.send_message(message.channel, """
This command creates a random password for you!
__HOW TO USE:__
**/password <length>**
			""")
		elif cmd=="reverse":
			await client.send_message(message.channel, """
This command reverses text you input!
__HOW TO USE:__
**/reverse <text>**
			""")
		
	elif cmd == "ip-addr":
		ip = socket.gethostbyname(socket.gethostname())
		await client.send_message(message.channel, str(ip))

	elif cmd == 'hash':
		_, word = message.content.split(' ',1)
		byte_pass = word.encode("utf-8")
		printit = hashlib.sha512(byte_pass).hexdigest()
		await client.send_message(message.channel, "```" + printit + "```")

	elif cmd == "password":
		_, length = message.content.split(' ',1)
		s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
		passlen = int(length)
		print('')
		p = "".join(random.sample(s, passlen))
		await client.send_message(message.channel, f"**Here is your password:**\n{p}")


	elif cmd == "pins":
		_, q = message.content.split(' ',1)
		printit=[]
		for msg in await client.pins_from(client.get_channel(q)):
 			printit.append(f'`{msg.author}: {msg.content}`')
		await client.send_message(message.channel, '\n'.join(printit))
	
	elif cmd == 'admin-help':
		adminembed = discord.Embed(title="", description="", color=0x00ff00)
		adminembed.add_field(name="COMMANDS", value=adminhelpmessage, inline=False)

		if message.author.id=='440231799533338634' or message.author.id=='224588823898619905':
			await client.send_message(message.author, embed=adminembed)
		else:
			await client.send_message(message.channel, "You can't use this command!")
	
	elif cmd == 'ask':
		_, q = message.content.split(' ',1)
		content = None
		if 'replit' in q or 'repl.it' in q:
			if 'what' in q or 'whats' in q or 'what\'s' in q or 'what is' in q:
				content = 'Replit is a coding website'
			else:
				content = 'idk what you mean but replit is a coding website'
		if content == None:
			await client.send_typing(message.channel)
			res = await loop.run_in_executor(None, wolfram.query, q)
			try:
				content=next(res.results).text
			except:
				content='Invalid Question'
		await client.send_typing(message.channel)
		await client.send_message(message.channel,f'```{content}```')
	elif cmd == 'google':
		_, q = message.content.split(' ',1)
		await client.send_typing(message.channel)
		await client.send_message(message.channel, readgoogle(q))
	
	elif cmd == 'stop-bot':
		if message.author.id=='440231799533338634' or message.author.id=='224588823898619905':
			await client.send_message(message.channel, client.user.name + " stopped!")
			exit()
		else:
			await client.send_message(message.channel,'You can\'t use this command')
	
	elif cmd == 'ping':
		startping=time.time()
		pongmsg=await client.send_message(message.channel,'Pong!')
		endping=time.time()
		await client.edit_message(pongmsg,f'Pong! `{int((endping-startping)*1000)} ms`')
	elif cmd == 'info':
		online=0
		offline=0
		dnd=0
		idle=0
		for member in message.server.members:
			if member.status == 		discord.Status.online:online+=1
			elif member.status == discord.Status.offline:offline+=1
			elif member.status == discord.Status.dnd:dnd+=1
			elif member.status == discord.Status.idle:idle+=1
		infomsg = f'**Your Name: ** {message.author.name}\n**Bot Name: ** {client.user.name}\n**Current Server: ** {message.server.name}\n**Current Channel:** {message.channel.name} \n**Online Members:** {online}\n**Offline Members:** {offline}\n**Idle Members:** {idle}\n**DnD Members:** {dnd}'
		infoembed = discord.Embed(title="", description="", color=0xff00ee)
		infoembed.add_field(name="INFO", value=infomsg, inline=False)
		await client.send_message(message.channel, embed=infoembed)
	
	elif cmd == "server":
		await client.send_message(message.channel, "**JOIN MESSENGERBOT'S SERVER**\nhttps://discord.gg/edUaxdn")

	elif cmd == 'youtube':
		_, q = message.content.split(' ',1)
		
		query_string = urllib.parse.urlencode({"search_query" : q})
		html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
		search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
		await client.send_message(message.channel, "http://www.youtube.com/watch?v=" + search_results[0])

	elif cmd == 'lmgtfy':
		_, q = message.content.split(' ',1)

		query=q
		query=query.strip().split()
		query="+".join(query)

		await client.send_typing(message.channel)
		await client.send_message(message.channel, "https://lmgtfy.com/?q=" + query)

	elif cmd == 'ascii':
		_, name = message.content.split(" ",1)
		if len(name) <= 12:
			f = Figlet(font='univers')
			text = f.renderText(name)
			text = text.replace("`", "`​") # there's a zero-width space in there
			print(text)
			await client.send_message(message.channel, "```\n" + text + "```")
		else:
			await client.send_message(message.channel, ":writing_hand:" + "__**message is TOO LONG! Try again!**__".upper() + ":writing_hand:")

	elif cmd == "status":
		_, pres, desc = message.content.split(' ',2)

		if message.author.id=='440231799533338634' or message.author.id=='224588823898619905':
			if pres == "playing":
				status="p"
				presence = desc
				await client.send_message(message.channel, "Status Successfully Changed!")
			elif pres == "streaming":
				status="s"
				presence = desc
				await client.send_message(message.channel, "Status Successfully Changed!")		
			elif pres == "listening":
				status="l"
				presence = desc
				await client.send_message(message.channel, "Status Successfully Changed!")
			elif pres == "watching":
				status="w"
				presence = desc
				await client.send_message(message.channel, "Status Successfully Changed!")
		else:
			await client.send_message(message.channel, "you can't use this command!")
	
	elif cmd == 'invite':
		await client.send_message(message.channel, "**You can invite me here:**\nhttps://discordapp.com/oauth2/authorize?client_id=484837921141030962&scope=bot&permissions=0")
	
	elif cmd == "emoji":
		_, emoji = message.content.split(' ',1)

		await client.send_message(message.channel, ':' + emoji + ':')

	elif cmd== 'exec':
		if message.author.id == "440231799533338634" or message.author.id == "224588823898619905":
			try:
				lang = args[0]
			except:
				await client.send_message(message.channel,'Invalid language')
				return
			toexec = args2
			totalsent=0
			if lang=='py':lang='python3'
			elif lang=='js':lang='nodejs'
			elif lang=='rb':lang='ruby'
			execsessions.append(message.author.id)
			print('lang:',lang)
			print('code:',toexec)
			try:
				async for line in runcode(toexec,lang,authorid=message.author.id):
					totalsent+=1
					if totalsent > 15:
						await client.send_message(message.channel, '```...```')
						break
					else:
						await client.send_message(message.channel, f'```{line}```')
				if totalsent == 0:
					await client.send_message(message.channel, 'Nothing was printed.')
			except Exception as e:
				print(e)
		else:
			await client.send_message(message.channel, f'Successfully sent code to {message.author}')
			try:
				lang = args[0]
			except:
				await client.send_message(message.author,'Invalid language')
				return
			toexec = args2
			totalsent=0
			if lang=='py':lang='python3'
			elif lang=='js':lang='nodejs'
			elif lang=='rb':lang='ruby'
			execsessions.append(message.author.id)
			print('lang:',lang)
			print('code:',toexec)
			try:
				async for line in runcode(toexec,lang,authorid=message.author.id):
					totalsent+=1
					if totalsent > 15:
						await client.send_message(message.author, '```...```')
						break
					else:
						await client.send_message(message.author, f'```{line}```')
				if totalsent == 0:
					await client.send_message(message.author, 'Nothing was printed.')
			except Exception as e:
				print(e)
		execsessions.remove(message.author.id)
	elif cmd == 'execinput':
		await client.send_message(message.channel, "execinput command is currently in development!")
		#execinput = args[1:]
		#if message.author.id in execsessions:
			#try:
				#execstdin[message.author.id].append(execinput)
			#except:
				#execstdin[message.author.id]=[execinput]
		#else:
			#await client.send_message(message.author, 'You don\'t currently have an exec session open.')
		
		if status == "p":
			await client.change_presence(game=discord.Game(name=presence), type=0)
		elif status == "s":
			await client.change_presence(game=discord.Game(name=presence), type=1)
		elif status == "l":
			await client.change_presence(game=discord.Game(name=presence), type=2)
		elif status == "w":
			await client.change_presence(game=discord.Game(name=presence), type=3)
	
	elif cmd == 'userinfo':
		pass
	
	elif cmd == 'roles':
		await client.send_message(message.channel, message.author + "'s roles are: " + message.author.roles)
	
	elif cmd == 'embed':
		_, color, name, desc = message.content.split(' +',3)
		if color == "red":
			color = 0xff0000
		elif color == "blue":
			color = 0x0011ff
		elif color == "green":
			color = 0x00ff15
		elif color == "brown":
			color = 0xad501f
		elif color == "pink":
			color = 0xff009d
		elif color == "purple":
			color = 0xb71478
		realembed = discord.Embed(title="", description="", color=color)
		realembed.add_field(name=name, value=desc, inline=False)
		await client.send_message(message.channel, embed=realembed)
	

def selectchannelsync():
	loop = asyncio.new_event_loop()
	loop.run_until_complete(selectchannel())
async def selectchannel():
	# repl.it server id: 437048931827056642
	# arkadyax server id: 481101701877727233
	serverid = input('Please enter server id\n> ')
	if serverid=='':serverid='437048931827056642'
	nameserver = client.get_server(serverid)
	channelstmp = nameserver.channels
	channelsdict = {}
	for channel in channelstmp:
		if channel.type == discord.ChannelType.text:
			channelsdict[channel.position] = channel.id
	channels = []
	for i in channelsdict:channels.append(None)
	x = 0
	for i in channelsdict:
		channels[x] = client.get_channel(channelsdict[i])
		x += 1
	i = 0
	for channel in channels:
		i += 1
		print(f'{i}) #{channel.name}')
	global messagechannel
	while True:
		try:
			channelnum = input('Please enter the number of the channel you would like to read from and send messages to\n> ')
			messagechannel = channels[int(channelnum) - 1]
			print(f'Set channel to #{messagechannel.name}')
			break
		except:
			print('Invalid channel number.')
	Thread(target=send_messages_thread).start()
	
@client.event
async def on_ready():
	global messagechannel
	messagechannel=client.get_channel('455493537580974090')
	print(messagechannel)
	await loop.run_in_executor(None, selectchannelsync)



def run_bot():
	client.run(os.getenv('TOKEN'))
	print("bot running")
def run_app():
	app.run('0.0.0.0',8080)
	print("web running")
Thread(target=run_app).start()
run_bot()
