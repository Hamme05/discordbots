import discord, youtube_dl, requests, asyncio, os, sys
from io import StringIO
from time import sleep


client = discord.Client()
api = 'https://api.wit.ai/message?v=20180824&q='
url = 'http://localhost:8080/add/'
players = {}
queues = {}
opts = {
            'default_search': 'auto',
            'quiet': False,
        }
savedqueue = {}

Hamme05 = ''
hgameold = ''
hgame = ''

def check_queue(id):
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        player.start()


@client.event
async def on_ready():
    print('Logged in as @{0.user}!'.format(client))
    await client.change_presence(game=discord.Game(name='By Hamme05#3819', type=3))
    await client.send_message(discord.Object(id='461121279441764382'), 'Logged in as {0.user}!'.format(client))
    for member in client.get_all_members():
        if member.id == '333910121992159232':
            Hamme05 = member
            print('Found: '+Hamme05.name+'#'+Hamme05.discriminator+' Nickname: '+Hamme05.display_name)

@client.event
async def on_message(message):
    global url
    if message.author.id == '333910121992159232' or message.author.id == '368400858926546944':
        if message.content.startswith("%cl"):
            args = message.content.split(" ")
            args = " ".join(args[1:])
            args = "<@&462937673645162506> {}".format(args)
            await client.send_message(discord.Object(id='462960552415592450'), args)

        if message.content.startswith('%stu'):
            ctx = message.content.split(" ")
            ctx = " ".join(args[1:])
            ctx = ctx.split(", ")
            statusType = ctx[0]
            statusType = int(statusType)
            ctx = ", ".join(args[1:])
            await client.change_presence(game=discord.Game(name=ctx, type=statusType))
            

    if message.content.startswith('%join'):
        uservoice = message.author.voice.voice_channel
        await client.join_voice_channel(uservoice)
        await client.delete_message(message)

    if message.content.startswith('%destroy'):
        server = message.server
        voice_client = client.voice_client_in(server)
        await voice_client.disconnect()
        await client.delete_message(message)

    if message.content.startswith('%play'):
        server = message.server
        args = message.content.split(" ")
        args = " ".join(args[1:])
        voice_client = client.voice_client_in(server)
        player = await voice_client.create_ytdl_player(args, ytdl_options=opts, after=lambda: check_queue(server.id))
        players[server.id] = player
        player.start()
        savedqueue[server.id] = []
        savedqueue[server.id].append(args)
        await client.delete_message(message)

    if message.content.startswith('%pause'):
        id = message.server.id
        players[id].pause()
        await client.delete_message(message)

    if message.content.startswith('%resume'):
        id = message.server.id
        players[id].resume()
        await client.delete_message(message)
    
    if message.content.startswith('%stop'):
        id = message.server.id
        players[id].stop()
        await client.delete_message(message)

    if message.content.startswith('%skip'):
        server = message.server
        players[server.id].stop()
        sleep(1)
        check_queue(server.id)
        await client.delete_message(message)

    if message.content.startswith('%queue'):
        args = message.content.split(" ")
        args = " ".join(args[1:])
        server = message.server
        voice_client = client.voice_client_in(server)
        player = await voice_client.create_ytdl_player(args, ytdl_options=opts, after=lambda: check_queue(server.id))

        if server.id in queues:
            queues[server.id].append(player)
        else:
            queues[server.id] = [player]

        savedqueue[server.id].append(args)
        
        await client.send_message(message.channel, queues)
        await client.delete_message(message)
    if message.content.startswith('%exec') and message.author.id == '333910121992159232':
        ctx = message.content.split(" ")
        ctx = " ".join(ctx[1:])
        old_stdout = sys.stdout
        result = StringIO()
        sys.stdout = result
        try:
            exec(ctx)
        except:
            print('Something went wrong!')
        sys.stdout = old_stdout
        result_string = result.getvalue()
        await client.send_message(message.channel, 'Output: `'+result_string+'`')
        print("Output: "+result_string)
    if message.content.startswith('%msg'):
        ctx = message.content.split(" ")
        ctx = " ".join(ctx[1:])
        ctx = ctx.split(", ")
        user = discord.utils.get(client.get_all_members(), id=ctx[0])
        ctx = ", ".join(ctx[1:])
        await client.send_message(user, ctx)
        await client.send_message(message.channel, 'Meddelande: `{0}` till `{1}`'.format(ctx, user.name))
    if message.content.startswith('%nlp'):
        server = message.server
        ctx = message.content.split(" ")
        ctx = "+".join(ctx[1:])
        r = requests.get(api+ctx, headers={'Authorization' : 'Bearer IOZRZBCAI42JPXIOGNIIYRFBA6YV7CDK'})
        r = r.json()
        print(r)
        rtype = r['entities']['intent'][0]['value']
        rvalue = r['entities']
        rvalue.pop('intent')
        rvalue = rvalue[list(rvalue)[0]]
        rvalue = rvalue[0]['value']
        r = "Type: `"+rtype+"` Value: `"+rvalue+"`"
        await client.send_message(message.channel, r)
        voice_client = client.voice_client_in(server)
        player = await voice_client.create_ytdl_player(ctx, ytdl_options=opts, after=lambda: check_queue(server.id))
        players[server.id] = player
        player.start()
    if message.content.startswith('%listqueue'):
        await client.send_message(message.channel, savedqueue)




    #if message.author != client.user:
    #    msg = message.content
    #
    #    print(msg)
    #    requests.get(url+msg)

client.run('NDYxMDk0ODcwOTk2NjE1MTcw.DjUQAQ.jtmANIGUTBjY7n7Ut8wrpLwEEMM')