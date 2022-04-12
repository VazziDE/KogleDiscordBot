import json
import datetime

import discord
from discord import Embed
from discord.ext import commands

TOKEN = ""
BANNER = b"\x20\x5F\x20\x20\x5F\x5F\x20\x5F\x5F\x5F\x5F\x20\x20\x5F\x5F\x5F\x5F\x5F\x20\x5F\x20\x20\x20\x20\x20\x5F" \
         b"\x5F\x5F\x5F\x5F\x0A\x2F\x20\x7C\x2F\x20\x2F\x2F\x20\x20\x5F\x20\x5C\x2F\x20\x20\x5F\x5F\x2F\x2F\x20\x5C" \
         b"\x20\x20\x20\x2F\x20\x20\x5F\x5F\x2F\x0A\x7C\x20\x20\x20\x2F\x20\x7C\x20\x2F\x20\x5C\x7C\x7C\x20\x7C\x20" \
         b"\x20\x5F\x7C\x20\x7C\x20\x20\x20\x7C\x20\x20\x5C\x20\x20\x0A\x7C\x20\x20\x20\x5C\x20\x7C\x20\x5C\x5F\x2F" \
         b"\x7C\x7C\x20\x7C\x5F\x2F\x2F\x7C\x20\x7C\x5F\x2F\x5C\x7C\x20\x20\x2F\x5F\x20\x0A\x5C\x5F\x7C\x5C\x5F\x5C" \
         b"\x5C\x5F\x5F\x5F\x5F\x2F\x5C\x5F\x5F\x5F\x5F\x5C\x5C\x5F\x5F\x5F\x5F\x2F\x5C\x5F\x5F\x5F\x5F\x5C "
PREFIX = "&="
bot = commands.Bot(command_prefix="&=")

botcommands = ["level", "leveluser", "daily", "coins"]


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
        y = {str(userID): True, 'level': 0, 'coins': 0, 'cooldown': 0}
        tempdata.append(y)

    with open("level.json", "w") as f:
        json.dump(data, f, indent=4)


def giveUserLevel(userID):
    if existUser(userID) is False:
        createUserLevel(userID)
    oldLevel = getUserLevel(userID)
    oldCoins = getUserCoins(userID)
    cooldown = getUserCooldown(userID)

    with open("level.json") as json_file:
        data = json.load(json_file)
        tempdata = data["levels"]
        oldData = {str(userID): True, 'level': oldLevel, 'coins': oldCoins, 'cooldown': cooldown}
        tempdata.remove(oldData)

        with open("level.json") as json_file:
            newLevel = {str(userID): True, 'level': (oldLevel + 1), 'coins': oldCoins, 'cooldown': cooldown}
            tempdata.append(newLevel)

        with open("level.json", "w") as f:
            json.dump(data, f, indent=4)


def giveUserCoins(userID):
    if existUser(userID) is False:
        createUserLevel(userID)
    if int(getUserCooldown(userID)) < int(datetime.datetime.now().strftime("%Y%m%d%H%M%S")):
        oldLevel = getUserLevel(userID)
        oldCoins = getUserCoins(userID)
        cooldown = getUserCooldown(userID)

        with open("level.json") as json_file:
            data = json.load(json_file)
            tempdata = data["levels"]
            oldData = {str(userID): True, 'level': oldLevel, 'coins': oldCoins, 'cooldown': cooldown}
            tempdata.remove(oldData)

            with open("level.json") as json_file:
                newLevel = {str(userID): True, 'level': oldLevel, 'coins': (oldCoins + 10), 'cooldown': cooldown}
                tempdata.append(newLevel)

            with open("level.json", "w") as f:
                json.dump(data, f, indent=4)
        updateCooldown(userID)
        return True
    return False


def updateCooldown(userID):
    if existUser(userID) is False:
        createUserLevel(userID)
    oldLevel = getUserLevel(userID)
    oldCoins = getUserCoins(userID)
    cooldown = getUserCooldown(userID)
    with open("level.json") as json_file:
        data = json.load(json_file)
        tempdata = data["levels"]
        oldData = {str(userID): True, 'level': oldLevel, 'coins': oldCoins, 'cooldown': cooldown}
        tempdata.remove(oldData)

        nowtime = int(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        enddate = nowtime + int(datetime.timedelta(days=1).total_seconds())
        with open("level.json") as json_file:
            newLevel = {str(userID): True, 'level': oldLevel, 'coins': oldCoins,
                        'cooldown': enddate}
            tempdata.append(newLevel)

        with open("level.json", "w") as f:
            json.dump(data, f, indent=4)


def getUserCooldown(userID):
    oldCooldown = 0
    with open("level.json") as json_file:
        data = json.load(json_file)
        tempdata = data["levels"]
        for checking in tempdata:
            if str(userID) in checking:
                if "cooldown" in checking:
                    oldCooldown = checking["cooldown"]
                    tempdata.remove(checking)
                    break

    return oldCooldown


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


def getUserCoins(userID):
    oldCoins = 0
    with open("level.json") as json_file:
        data = json.load(json_file)
        tempdata = data["levels"]
        for checking in tempdata:
            if str(userID) in checking:
                oldCoins = checking["coins"]
                tempdata.remove(checking)
                break

    return oldCoins


@bot.event
async def on_message(message):
    channel = message.channel
    if isinstance(channel, discord.TextChannel):
        author = message.author
        if author.id != bot.user.id:
            useCommand = False
            for checkcmd in botcommands:
                if message.content.startswith(PREFIX + checkcmd) is True:
                    useCommand = True
                    break
            if useCommand is False:
                giveUserLevel(author.id)
    await bot.process_commands(message)


@bot.command()
async def level(ctx):
    author = ctx.author
    await ctx.send("Your level is " + str(getUserLevel(author.id)))


@bot.command()
async def leveluser(ctx, *, member: discord.Member):
    await ctx.send(member.display_name + "'s level is " + str(getUserLevel(member.id)))


@bot.command()
async def daily(ctx):
    channel = ctx.channel
    if isinstance(channel, discord.TextChannel):
        author = ctx.author
        if giveUserCoins(author.id) is True:
            claimembed = Embed(
                title="Dailyreward Claimed",
                url="",
                description="You have claimed your dailyreward of 10 coins.",
                color=0x06a135
            )
            await ctx.send(embed=claimembed)
        else:
            claimembed = Embed(
                title="Dailyreward Cooldown",
                url="",
                description="You are still in a cooldown.",
                color=discord.Colour.from_rgb(211, 84, 0)
            )
            await ctx.send(embed=claimembed)


@bot.command()
async def coins(ctx):
    channel = ctx.channel
    if isinstance(channel, discord.TextChannel):
        author = ctx.author
        coinsembed = Embed(
            title="Your Coins",
            url="",
            description="You have " + str(getUserCoins(author.id)) + " coins.",
            color=10417
        )
        await ctx.send(embed=coinsembed)


@leveluser.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing Argument [1]: &=leveluser @User")


bot.run(TOKEN)
