#!/usr/bin/python3

import discord
client = discord.Client()

statusName = 'error'
statusType = 0

@client.event
async def on_ready():
    print('Logged in as @{0.user}!'.format(client))

@client.event
async def on_message(message):
    if message.author.id == '333910121992159232':
        if message.content.startswith("%sts "):
            args = message.content.split(" ")
            args = " ".join(args[1:])
            args = args.split(", ")
            await client.delete_message(message)
            statusName = args[0]
            statusType = args[1]
            statusTypestr = statusType
            statusType = int(statusType)
            print(statusName)
            print(statusType)
            args = "Changed your status to: `"+statusName+"` with the type: `"+statusTypestr+"`"
            print(args)
            await client.send_message(message.channel, args)
            await client.change_presence(game=discord.Game(name=statusName, type=statusType))
    if message.author.id == '333910121992159232':
        if message.content.startswith("%stss"):
            args = message.content.split(" ")
            args = " ".join(args[1:])
            args = args.split(", ")
            await client.delete_message(message)
            statusName = args[0]
            statusType = args[1]
            statusTypestr = statusType
            statusType = int(statusType)
            print(statusName)
            print(statusType)
            args = "Changed your status to: `"+statusName+"` with the type: `"+statusTypestr+"`"
            print(args)
            await client.change_presence(game=discord.Game(name=statusName, type=statusType))

##client.run('NDYxMDk0ODcwOTk2NjE1MTcw.DhOTmw.LQeuY1Wmn8zCtBR5FyGumj3fcqw')
client.run('username', 'password')
