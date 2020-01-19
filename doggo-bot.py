# Work with Python 3.6
import random
import asyncio
import aiohttp
import json
from discord import Game
from discord.ext.commands import Bot
from discord import ChannelType
from discord import Channel
import numpy as np
import subprocess as sb

BOT_PREFIX = ("?", "*")
TOKEN = 'NjY3NzM5NzEyNzY4NzA0NTIz.XiSOXA.-ASOJyHe9D-4hhKqY24axCao6L0'  # Get at discordapp.com/developers/applications/me

client = Bot(command_prefix=BOT_PREFIX)

@client.event
async def on_message(message):

    # Getting the actual server and all channels on him
    actualServer = message.channel.server
    todos_canal = []
    i = 0
    for canal in actualServer.channels:
        if canal.type == ChannelType.text:
            todos_canal.insert(i, canal.id)
            i = i + 1

    # We do not want the bot to reply to itself
    if message.author == client.user:
        return

    # An If sequence lookalike a one "Switch Case"  for the bot commands, because the client.command code doesn't work
    if message.content.startswith("-d"):
        # Command -dh = Got a JSON with the complete list of the Dictator Bot commands and send a Message with them
        if message.content.startswith("-dh"):
            url = 'https://gist.githubusercontent.com/JvDev-hash/7b08167ea5c794dc6a0767169c4dd86d/raw/4e76ae7872ff336ba35240edac65fef0a19bed10/commands_dictator.json'
            async with aiohttp.ClientSession() as session:  # Async HTTP request
                raw_response = await session.get(url)
                response = await raw_response.text()
                response = json.loads(response)
            await client.send_message(message.channel, "Bork!! Oookay hooman, am doin a send the list of my tricks..")
            await client.send_message(message.channel, response['list']['commands'])

        # Command -dt = Insert the chosen channel and the tags chosen to him, because the verification will compare this tags on this and other channels        
        elif message.content.startswith("-dt"):
            stringContent = message.content[4:]
            arrayTags = np.array(stringContent.split(", "))
            littleChannel = arrayTags[0]
            newArrayTags = np.delete(arrayTags, 0)
            mydict = {}
            keys = len(newArrayTags)
            for i in range(keys):

                tag = "tag"+str(i)
                mydict[tag] = newArrayTags[i]
                
            mydict["channel"] = littleChannel

            archiveName = actualServer.name + "-" + str(arrayTags[0]) + ".json"
            with open(archiveName, 'w') as fp:
                json.dump(mydict, fp)

            sb.call("./permit.sh")
            await client.send_message(message.channel, "Oookay hooman {0.author.mention}, am doin a boop in this bork letters place for you".format(message))

        # Condicional to permit the other members send messages normally, without the bot annoying they
        elif message.content.find("-d") == -1 or message.content.find("-d") != 0:
            pass
        
        # Joke to a member which send a message with the bot prefix with a random message
        else:
            await client.send_message(message.channel, "~A Not Understanding face..~ Hooman {0.author.mention}, am no understand wat you doin".format(message))
    
    else:
        # Verification if the message contains a blacklisted word in this channel, and moving her to the right place
        for canal in actualServer.channels:
            if canal.type == ChannelType.text:
                jsonName = actualServer.name + "-" + str(canal.name) + ".json"
                outputChannels = sb.check_output(["./list.sh", actualServer.name]).decode("utf-8").split("\n")
                outputChannels.remove("")
                if jsonName in outputChannels:
                    with open(jsonName, 'r') as f:
                        open_dict = json.load(f)
                        idTags = len(open_dict) - 1
                        for i in range(idTags):
                            newTags = "tag"+str(i)
                            dictValue = open_dict.get(newTags)
                            if dictValue.upper() in message.content.upper():
                                msg = "AWOOOOO! Hey fren {0.author.mention}, your bork doesn't belongs here: {0.channel}".format(message)
                                sending = "Bork! The hooman {0.author.mention} borked this on wrong place".format(message)

                                await client.send_message(message.channel, msg)
                                await client.delete_message(message)
                                await client.send_message(client.get_channel(canal.id), sending)
                                await client.send_message(client.get_channel(canal.id), message.content)

                                break

                            else:
                                pass
            

 
@client.event
async def on_ready():
    await client.change_presence(game=Game(name="For commands, type -dh"))
    #await client.change_presence(game=Game(name="Keeping an eye on humans"))
    print("Logged in as " + client.user.name)

async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)

async def testCall():
    await client.wait_until_ready()
    #x = sb.call(["ls", "|", "grep", "json"])
    #x = sb.Popen("./script.sh", stdout=sb.PIPE, shell=True)
    #(output, err) = x.communicate()
    #output = sb.check_output(["./list2.sh", "incles"]).decode("utf-8").split("\n")
    #output.remove("")
    for actualServer in client.servers:
        for canal in actualServer.channels:
            if canal.type == ChannelType.text:
                print(canal.name)
    await asyncio.sleep(600)


client.loop.create_task(list_servers())
#client.loop.create_task(testCall())
client.run(TOKEN)