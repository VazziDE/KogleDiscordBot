import json

import discord

TOKEN = ""
BANNER = b"\x20\x5F\x20\x20\x5F\x5F\x20\x5F\x5F\x5F\x5F\x20\x20\x5F\x5F\x5F\x5F\x5F\x20\x5F\x20\x20\x20\x20\x20\x5F" \
         b"\x5F\x5F\x5F\x5F\x0A\x2F\x20\x7C\x2F\x20\x2F\x2F\x20\x20\x5F\x20\x5C\x2F\x20\x20\x5F\x5F\x2F\x2F\x20\x5C" \
         b"\x20\x20\x20\x2F\x20\x20\x5F\x5F\x2F\x0A\x7C\x20\x20\x20\x2F\x20\x7C\x20\x2F\x20\x5C\x7C\x7C\x20\x7C\x20" \
         b"\x20\x5F\x7C\x20\x7C\x20\x20\x20\x7C\x20\x20\x5C\x20\x20\x0A\x7C\x20\x20\x20\x5C\x20\x7C\x20\x5C\x5F\x2F" \
         b"\x7C\x7C\x20\x7C\x5F\x2F\x2F\x7C\x20\x7C\x5F\x2F\x5C\x7C\x20\x20\x2F\x5F\x20\x0A\x5C\x5F\x7C\x5C\x5F\x5C" \
         b"\x5C\x5F\x5F\x5F\x5F\x2F\x5C\x5F\x5F\x5F\x5F\x5C\x5C\x5F\x5F\x5F\x5F\x2F\x5C\x5F\x5F\x5F\x5F\x5C "
PREFIX = "&="
bot = discord.Client()


@bot.event
async def on_ready():
    print(BANNER.decode("utf8"))
    print("Kogle Bot has started and is searching for friends")
    game = discord.Game("Searching for a bot friend")
    await bot.change_presence(status=discord.Status.idle, activity=game)


def existUser(userID):
    with open("level.json") as json_file:
        data = json.load(json_file)
        tempdata = data["levels"]
        isIn = False
        for checking in tempdata:
            if str(userID) in checking:
                isIn = True
                return isIn
        return isIn


def createUserLevel(userID):
    with open("level.json") as json_file:
        data = json.load(json_file)
        tempdata = data["levels"]
        y = {str(userID): True, 'level': 0}
        tempdata.append(y)

    with open("level.json", "w") as f:
        json.dump(data, f, indent=4)


def giveUserLevel(userID):
    if existUser(userID) is False:
        createUserLevel(userID)
        return
    oldLevel = getUserLevel(userID)

    with open("level.json") as json_file:
        data = json.load(json_file)
        tempdata = data["levels"]
        oldData = {str(userID): True, 'level': oldLevel}
        tempdata.remove(oldData)

    with open("level.json") as json_file:
        newLevel = {str(userID): True, 'level': (oldLevel + 1)}
        tempdata.append(newLevel)

    with open("level.json", "w") as f:
        json.dump(data, f, indent=4)


def getUserLevel(userID):
    oldLevel = 0
    with open("level.json") as json_file:
        data = json.load(json_file)
        tempdata = data["levels"]
        for checking in tempdata:
            if str(userID) in checking:
                oldLevel = checking["level"]
                tempdata.remove(checking)
                break

    return oldLevel


@bot.event
async def on_message(message):
    channel = message.channel
    if isinstance(channel, discord.TextChannel):
        lowed = str.lower(message.content)
        author = message.author
        giveUserLevel(author.id)
        if lowed.startswith(PREFIX):
            if lowed == PREFIX + "level":
                await channel.send("Your level is " + str(getUserLevel(author.id)))


bot.run(TOKEN)
