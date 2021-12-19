import discord
import os
import requests
import json
import random
from replit import db
from alive import alive
sad_words=['sad','depressed','angry','miserable','depressing']
basic_encouragement=['Hang in there!','cheer up','you are a great person','fuck everyone']
client =discord.Client()


def update_encouragement(encouraging_message):
  if "encouragement" in db.keys():
    encouragement=db["encouragement"]
    encouragement.append(encouraging_message)
    db["encouragement"]=encouragement
  else:
    db["encouragement"]=[encouraging_message]


def delete_encouragement(index):
  encouragement=db['encouragement']
  if len(encouragement)>index:
    del encouragement[index]
    db['encouragement']=encouragement


def get_quotes():
  response=requests.get("https://zenquotes.io/api/random")
  json_data=json.loads(response.text)
  quote=json_data[0]['q']+' -'+json_data[0]['a']
  return(quote)


if 'responding' not in db.keys():
    db['responding']=True
    

@client.event
async def on_ready():
  print('we have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author==client.user:
    return
  
  msg=message.content

  if msg.startswith('./quote'):
    quotes=get_quotes()
    await message.channel.send(quotes)
  
  if db['responding']:
    option=basic_encouragement
    if 'encouragement' in db.keys():
      option.extend(db['encouragement'])
    
    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(option))

  if msg.startswith('./new'):
    encouraging_message=msg.split('./new ',1)[1]
    update_encouragement(encouraging_message)
    await message.channel.send('new encouraging message added successfully :)')

  if msg.startswith('./del'):
    encouragement =[]
    if 'encouragement' in db.keys():
      index=int(msg.split('./del',1)[1])
      delete_encouragement(index)
      encouragement=db['encouragement']
    await message.channel.send(encouragement)

  if msg.startswith('./list'):
    encouragement=[]
    if 'encouragement' in db.keys():
      encouragement=db[encouragement]
    await message.channel.send(encouragement)
  
  if msg.startswith('./responding'):
    value=msg.split('./responding ',1)[1]
    if value.lower=='true':
      db['responding']=True
      await message.channel.send('Responding is on :)')
    else:
      db['responding']=False
      await message.channel.send('Responding is off :(')

alive()
client.run(os.getenv('TOKEN'))