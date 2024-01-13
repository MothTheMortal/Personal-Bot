import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from os import getenv
from datetime import datetime
from discord.app_commands import Choice, choices
from discord.ui import View, Button, Select
from discord import app_commands, SelectOption
from gtts import gTTS
import io
import asyncio
import pytube
import requests
from mcstatus import JavaServer
from config import *
import time
from PIL import Image, ImageDraw
import pymongo

load_dotenv()
tts_lock = asyncio.Lock()

TOKEN = getenv("BOT_TOKEN")
DB_KEY = getenv("MONGODB")
database = pymongo.MongoClient(DB_KEY)["lotm"]


def get_database_collection(cln):
    return database[cln]


def generate_social_doc(user_id):
    collection = get_database_collection("social"
                                         "")

    doc = collection.find_one({"_id": user_id})

    if doc is None:
        doc = {
            "_id": user_id,
            "instagram": "",
            "github": "",
            "mlbb": [],
            "coc": [],
            "minecraft": "",
            "steam": "",
            "valorant": ""
        }

        collection.insert_one(doc)



bot = commands.Bot(intents=discord.Intents.all(), command_prefix=".")

# @bot.command(name="test", description="Used for running temporary one-off commands.")
# async def test(ctx: commands.Context):
#     role = ctx.guild.get_role(1147062497812156427)
#     msg = await ctx.guild.fetch_channel(1145462429929717824)
#     x = await msg.fetch_message(1146648138598326342)
#     async for user in x.reactions[0].users():
#         try:
#             if not user.bot:
#                 await user.add_roles(role)
#         except:
#             pass


class SocialGroup(app_commands.Group):
    @app_commands.command()
    async def instagram(self, ctx: discord.Interaction, username: str):
        generate_social_doc(ctx.user.id)

        collection = get_database_collection("social")

        data = "@" + username

        collection.update_one({"_id": ctx.user.id}, {"$set": {"instagram": data}})

        await ctx.response.send_message(f"Instagram: {'@' + username}", ephemeral=True)

    @app_commands.command()
    async def coc(self, ctx: discord.Interaction, username: str, clashid: str):
        generate_social_doc(ctx.user.id)

        collection = get_database_collection("social")

        data = [username, clashid if "#" in clashid else "#" + clashid]

        collection.update_one({"_id": ctx.user.id}, {"$set": {"coc": data}})

        await ctx.response.send_message(f"Clash of Clans: {' '.join(data)}", ephemeral=True)


    @app_commands.command()
    async def mlbb(self, ctx: discord.Interaction, username: str, userid: str):
        generate_social_doc(ctx.user.id)

        collection = get_database_collection("social")

        data = [username, userid]

        collection.update_one({"_id": ctx.user.id}, {"$set": {"mlbb": data}})

        await ctx.response.send_message(f"MLBB: {' '.join(data)}", ephemeral=True)



    @app_commands.command()
    async def valorant(self, ctx: discord.Interaction, username: str):
        generate_social_doc(ctx.user.id)

        collection = get_database_collection("social")

        data = username

        collection.update_one({"_id": ctx.user.id}, {"$set": {"valorant": data}})

        await ctx.response.send_message(f"Valorant: {data}", ephemeral=True)

    @app_commands.command()
    async def github(self, ctx: discord.Interaction, username: str):
        generate_social_doc(ctx.user.id)

        collection = get_database_collection("social")

        data = username

        collection.update_one({"_id": ctx.user.id}, {"$set": {"github": data}})

        await ctx.response.send_message(f"Github: {data}", ephemeral=True)

    @app_commands.command()
    async def minecraft(self, ctx: discord.Interaction, username: str):
        generate_social_doc(ctx.user.id)

        collection = get_database_collection("social")

        data = username

        collection.update_one({"_id": ctx.user.id}, {"$set": {"minecraft": data}})

        await ctx.response.send_message(f"Minecraft IGN: {data}", ephemeral=True)

    @app_commands.command()
    async def steam(self, ctx: discord.Interaction, username: str, friendcode: str):
        generate_social_doc(ctx.user.id)

        collection = get_database_collection("social")

        data = [username, friendcode]

        collection.update_one({"_id": ctx.user.id}, {"$set": {"steam": data}})

        await ctx.response.send_message(f"Steam: {' '.join(data)}", ephemeral=True)

    


@bot.event
async def on_ready():
    serverStatus.start()
    print(f"{bot.user.name} is online.")
    print(f"{len(await bot.tree.sync())} commands loaded.")

    socialGroup = SocialGroup(name="social", description="test ")
    bot.tree.add_command(socialGroup)

    await bot.tree.sync()



@bot.event
async def on_member_join(member: discord.Member):
    if member.guild.id not in [1145420194341204080]:
        return

    member_role = member.guild.get_role(1154077513824354355)
    await member.add_roles(member_role, reason="New Prisoner!")
    # if member.bot:
    #     bot_role = member.guild.get_role(1145465466203152515)
    #     await member.add_roles(bot_role, reason="New Bot role!")
    # else:
    #     member_role = member.guild.get_role(1145461173718896731)
    #     await member.add_roles(member_role, reason="New Member Role!")


@bot.event
async def on_message_delete(message: discord.Message):
    snipe_channel = [channel for channel in message.guild.channels if channel.name == snipeName]
    if snipe_channel:
        snipe_channel = snipe_channel[0]

        if message.channel.id == snipe_channel.id:
            return
        if message.attachments:
            await snipe_channel.send(files=[await f.to_file() for f in message.attachments])
        else:
            await snipe_channel.send(f"{message.author.name}: {message.content}")


@tasks.loop(seconds=30)
async def serverStatus():
    status_channel = bot.get_channel(1147073523416825896)
    msg: discord.Message = await status_channel.fetch_message(1147761585251696640)

    try:
        server = JavaServer.lookup(address="147.185.221.16:47369")
        users = [i.name for i in server.status().players.sample]
        max_user = server.status().players.max
        online_users = server.status().players.online
        motd = server.status().motd.raw['text']
        vers = server.status().version.name
        description = f"**Server:** :green_circle:\n**Players Online:** {online_users}/{max_user}\n**Players:** {', '.join(users)}\n**MOTD**: {motd}\n**Version:** Forge {vers}"
        embed = discord.Embed(title="Moth's Server Status", description=description, colour=0x00FF00)
    except:
        embed = discord.Embed(title="Moth's Server Status", description="**Server:** :red_circle:", colour=0xFF0000)

    embed.set_footer(text="Refreshes every 30 seconds.")
    await msg.edit(content="", embed=embed)


@bot.tree.command(name="play")
@app_commands.describe(link="the URL to the song.")
async def play(ctx: discord.Interaction, link: str):
    await ctx.response.defer()
    if tts_lock.locked():
        await ctx.send("The bot is being used. Please wait.")
        return

    async with tts_lock:

        yt = pytube.YouTube(link)
        description = f"Title: {yt.title}\nLength: {yt.length // 60} minutes {yt.length % 60} seconds"

        embed = discord.Embed(title=f"Playing Song", description=description)
        embed.set_image(url=yt.thumbnail_url)
        embed.set_footer(text="Playing...")

        try:
            channel = ctx.user.voice.channel
        except AttributeError:
            return await ctx.followup.send("You are not in a voice channel.", ephemereal=True)

        view = View(timeout=None)

        options = [SelectOption(label=f"Volume: {num}%", value=f"{num}", emoji=":loud_sound:") for i in range(10, 91, 10)]
        options.append(SelectOption(label=f"Volume: 100%", value=f"100", emoji=":loud_sound:", default=True))

        async def dropdown_callback(ctx: discord.Interaction):
            volume = int(dropdown.values[0])




        dropdown = Select(placeholder="Song Volume", min_values=1, max_values=1, options=options)
        dropdown.callback = dropdown_callback
        await ctx.followup.send(embed=embed)


        voice_client = await channel.connect()
        stream = yt.streams.get_audio_only()
        stream.download(filename="temp_music.mp3")
        await asyncio.sleep(2)
        source = discord.FFmpegPCMAudio("temp_music.mp3")
        voice_client.play(source)


        while voice_client.is_playing():

            await asyncio.sleep(1)
        await voice_client.disconnect()




        os.remove("temp_music.mp3")




@bot.tree.command(name="hatch", description="Hatch 3 spheals!")
async def hatch(ctx: discord.Interaction):
    await ctx.response.defer()
    sphealIMG1, sphealID1 = await spheal()
    sphealIMG2, sphealID2 = await spheal()
    sphealIMG3, sphealID3 = await spheal()

    totalIMG = concatenateIMG(sphealIMG1, sphealIMG2)
    totalIMGFile = IMGtoFile(concatenateIMG(totalIMG, sphealIMG3))
    await ctx.followup.send(file=totalIMGFile)


@bot.tree.command(name="adopt", description="Adopt a spheal!")
async def adopt(ctx: discord.Interaction):
    ...


@bot.tree.command(name="disown", description="Disown your spheal!")
async def disown(ctx: discord.Interaction):
    ...


async def spheal():
    image = Image.open("spheal2.png")

    randomColor = getRandomColor()
    ShadeColor = getShadeFromRGB(randomColor[0], randomColor[1], randomColor[2])
    eyeIMG, eyeColor = getRandomEye((RGBtoHSV(ShadeColor[0], ShadeColor[1], ShadeColor[2])[0]))

    image = image.convert("RGB")


    ImageDraw.floodfill(image, EarShade, ShadeColor, thresh=50)
    ImageDraw.floodfill(image, Shade, ShadeColor, thresh=50)
    ImageDraw.floodfill(image, SkinColor, randomColor, thresh=50)

    spotIMG = getRandomSpot((RGBtoHSV(ShadeColor[0], ShadeColor[1], ShadeColor[2])[0], 19, 100))

    image.paste(spotIMG, (0, 0), spotIMG)
    image.paste(eyeIMG, (0, 0), eyeIMG)
    sphealID = RGBtoHex(randomColor) + RGBtoHex(ShadeColor) + RGBtoHex(eyeColor) + RGBtoHex(HSVtoRGB(RGBtoHSV(ShadeColor[0], ShadeColor[1], ShadeColor[2])[0], 19, 100))

    # if sphealID in generatedSpheals:
    #     return await spheal()

    return image, sphealID


@bot.command(name="math")
async def math(ctx: commands.Context):
    question, solution = getAlgebra()
    timeout = 60
    embed = discord.Embed(title="Algebra Question",
                          description=f"Solve for x:\n{question}\nYou have {timeout} seconds to solve!")
    embed.set_footer(text="Answer has to be simplified, in whole number (12) or fraction form (12/5).")
    await ctx.channel.send(embed=embed)

    def check(m):
        return m.channel == ctx.channel and m.content == str(solution)

    startTime = time.time()
    try:
        msg = await bot.wait_for("message", check=check, timeout=timeout)
    except asyncio.TimeoutError:
        await ctx.channel.send(f"No one answered the question; The answer was {solution}!")
    else:
        await ctx.channel.send(
            f"{msg.author.mention} got the answer correctly in {int(time.time() - startTime)} seconds!")


@bot.command(name="linearmath")
async def linearmath(ctx: commands.Context):
    buffer, solution = getLinear()
    timeout = 600
    embed = discord.Embed(title="Linear Equation Question",
                          description=f"Find equation y=mx+c for this graph.\nYou have {timeout} seconds to solve!")
    embed.set_footer(text="Answer has to be in 'y=mc+x' form.")
    file = discord.File(fp=buffer, filename="linear_equation.png")
    await ctx.channel.send(embed=embed, file=file)

    def check(m):
        answer = m.content.lower()
        answer = answer.replace(" ", "")
        return m.channel == ctx.channel and answer == str(solution)

    startTime = time.time()
    try:
        msg = await bot.wait_for("message", check=check, timeout=timeout)
    except asyncio.TimeoutError:
        await ctx.channel.send(f"No one answered the question; The answer was {solution}!")
    else:
        await ctx.channel.send(
            f"{msg.author.mention} got the answer correctly in {int(time.time() - startTime)} seconds!")


@bot.command(name="quadraticmath")
async def quadraticmath(ctx: commands.Context):
    buffer, solution = getQuadratic()
    timeout = 600
    embed = discord.Embed(title="Quadratic Equation Question",
                          description=f"Find equation y=ax^2+bx+c for this graph.\nYou have {timeout} seconds to solve!")
    embed.set_footer(text="Answer has to be in 'y=ax^2+bx+c' form.")
    file = discord.File(fp=buffer, filename="quadratic_equation.png")
    await ctx.channel.send(embed=embed, file=file)

    def check(m):
        answer = m.content.lower()
        answer = answer.replace(" ", "")
        return m.channel == ctx.channel and answer == str(solution)

    startTime = time.time()
    try:
        msg = await bot.wait_for("message", check=check, timeout=timeout)
    except asyncio.TimeoutError:
        await ctx.channel.send(f"No one answered the question; The answer was {solution}!")
    else:
        await ctx.channel.send(
            f"{msg.author.mention} got the answer correctly in {int(time.time() - startTime)} seconds!")


@bot.command(name="unscramble")
async def unscramble(ctx: commands.Context):
    word, scrambledWord = getRandomWord()
    print(word)
    timeout = 120
    embed = discord.Embed(title="Unscramble!",
                          description=f"Unscramble the scrambled word within {timeout} seconds:\n**{scrambledWord}**")
    await ctx.channel.send(embed=embed)

    def check(m):
        return m.channel == ctx.channel and m.content.lower() == word

    startTime = time.time()

    try:
        msg = await bot.wait_for("message", check=check, timeout=timeout)
    except asyncio.TimeoutError:
        await ctx.channel.send(f"No one answered the question; The word was {word}!")
    else:
        await ctx.channel.send(
            f"{msg.author.mention} got the word correctly in {int(time.time() - startTime)} seconds!")


@bot.command(name="cat")
async def cat(ctx: commands.Context):
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    cat_img_url = response.json()[0]["url"]

    embed = discord.Embed(title="", description="", color=color_theme)
    embed.set_image(url=cat_img_url)
    await ctx.channel.send(embed=embed)


@bot.command(name="snipe")
async def snipe(ctx: commands.Context, count=0):
    snipe_channel = [channel for channel in ctx.guild.channels if channel.name == snipeName]
    if snipe_channel:
        snipe_channel = snipe_channel[0]
    else:
        return await ctx.send(f"channel `{snipeName}` not found!")

    msg = [msg async for msg in snipe_channel.history()][count]
    if msg.attachments:
        await ctx.reply(files=[await f.to_file() for f in msg.attachments])
    else:
        await ctx.reply(msg.content)


@bot.command(name="info")
async def info(ctx: commands.Context):
    Owner = ctx.guild.owner
    BoostsNo = ctx.guild.premium_subscription_count
    Boosters = ctx.guild.premium_subscribers
    TotalMemberCount = ctx.guild.member_count
    BotCount = len([mem for mem in ctx.guild.members if mem.bot])
    MemberCount = TotalMemberCount - BotCount

    description = f"**Members:** {MemberCount}\n**Bots:** {BotCount}\n**Boosts:** {BoostsNo}\n**Boosters:** {', '.join([member.name for member in Boosters])}\n**Created at:** {ctx.guild.created_at.date()}"
    embed = discord.Embed(title=f"{ctx.guild.name}'s Information", description=description, color=color_theme)
    embed.set_image(url=ctx.guild.icon.url)
    embed.set_author(name=Owner.name, icon_url=Owner.avatar.url)
    embed.set_footer(text=f"Owned by {Owner.name}")

    await ctx.channel.send(embed=embed)


@bot.command(name="socials", aliases=["social"])
async def socials(ctx: commands.Context):

    generate_social_doc(ctx.author.id)

    collection = get_database_collection("social")
    doc = collection.find_one({"_id": ctx.author.id})

    description = ""

    for key, value in doc.items():
        if key == "_id":
            continue

        if value:
            description += f"{emojis[key]}: **{value if type(value) == str else ' '.join(value)}**\n"

    if description == "":
        description = "No socials here :("

    embed = discord.Embed(title=f"{ctx.author.name}'s Socials", description=description, color=color_theme)
    await ctx.channel.send(embed=embed)


@bot.tree.command(name="download-yt", description="Download a Youtube Audio/Video")
@choices(filetype=[Choice(name="Audio Only - MP3", value="MP3"), Choice(name="Video & Audio - MP4", value="MP4")])
async def download_yt(ctx: discord.Interaction, link: str, filetype: Choice[str]):
    yt = pytube.YouTube(link)

    description = f"Title: {yt.title}\nLength: {yt.length // 60} minutes {yt.length % 60} seconds"

    embed = discord.Embed(title=f"Youtube Downloader - {filetype.value}", description=description)
    embed.set_image(url=yt.thumbnail_url)
    embed.set_footer(text="Downloading...")

    await ctx.response.send_message(embed=embed)

    if filetype.value == "MP3":
        stream = yt.streams.get_audio_only()
    else:
        stream = yt.streams.get_highest_resolution()

    video_data = io.BytesIO()
    stream.stream_to_buffer(video_data)
    video_data.seek(0)

    file = discord.File(video_data, filename=f"{yt.title[:32]}.{filetype.value.lower()}")

    embed.set_footer(text="Downloaded.")

    await ctx.edit_original_response(embed=embed)
    msg = await ctx.original_response()
    await msg.reply(file=file)


@bot.command(name="ttsa")
async def ttsa(ctx: commands.Context, language, *, text=None):
    if tts_lock.locked():
        await ctx.send("The bot is being used. Please wait.")
        return

    async with tts_lock:
        try:
            channel = ctx.author.voice.channel
        except AttributeError:
            return await ctx.send("You are not in a voice channel.")

        voice_client = await channel.connect()

        try:
            audio = gTTS(text, lang=language)
            audio.save("ttsaudio.mp3")
        except:
            await ctx.send("Unsupported language.")
            await voice_client.disconnect()

        source = discord.FFmpegPCMAudio("ttsaudio.mp3")
        voice_client.play(source)
        while voice_client.is_playing():
            await asyncio.sleep(1)
        await voice_client.disconnect()
        os.remove("ttsaudio.mp3")


@bot.command(name="tts")
async def tts(ctx: commands.Context, *, text=None):
    if tts_lock.locked():
        await ctx.send("The bot is being used. Please wait.")
        return

    async with tts_lock:
        try:
            channel = ctx.author.voice.channel
        except AttributeError:
            return await ctx.send("You are not in a voice channel.")

        voice_client = await channel.connect()

        audio = gTTS(text, lang="en")
        audio.save("ttsaudio.mp3")

        source = discord.FFmpegPCMAudio("ttsaudio.mp3")
        voice_client.play(source)
        while voice_client.is_playing():
            await asyncio.sleep(1)
        await voice_client.disconnect()
        os.remove("ttsaudio.mp3")


@bot.command(name="no-intro")
async def no_intro(ctx: commands.Context):
    intro_channel = ctx.guild.get_channel(1145593789130473573)
    names = [msg.embeds[0].author.name async for msg in intro_channel.history(limit=1000)]
    members = ctx.guild.members
    no_intro_member = []
    ignore_names = ["starbuckbarista", "unknownunfortunately", "meowchan101", "alternatived"]
    for member in members:
        if member.name not in names and not member.bot and member.name not in ignore_names:
            no_intro_member.append(member.name)
    await ctx.reply(", ".join(no_intro_member))


@bot.tree.command(name="edit-introduction", description="Command to edit your introduction")
@choices(question=[
    Choice(name="Name", value="Name"),
    Choice(name="Gender", value="Gender"),
    Choice(name="Age", value="Age"),
    Choice(name="Birthday", value="Birthday"),
    Choice(name="Nationality", value="Nationality"),
    Choice(name="Games", value="Games"),
    Choice(name="Languages", value="Languages"),
    Choice(name="Hobbies", value="Hobbies")
])
async def edit_introduction(ctx: discord.Interaction, question: Choice[str], answer: str):
    await ctx.response.defer()

    intro_channel = [channel for channel in ctx.guild.channels if channel.name == introName]
    if intro_channel:
        intro_channel = intro_channel[0]
    else:
        return await ctx.followup.send(f"Channel `{introName}` not found!")

    message = [msg async for msg in intro_channel.history(limit=1000) if msg.embeds[0].author.name == ctx.user.name]
    if not message:
        return await ctx.followup.send("Are you fucking braindead? Make a fucking introduction first before trynna edit it jeez, wasting my time!")

    message = message[0]
    Embed = message.embeds[0]
    embedDescriptionListed = message.embeds[0].description.split("\n")
    for index, text in enumerate(embedDescriptionListed):
        if f"**{question.name}:**" in text:
            embedDescriptionListed[index] = f"**{question.name}:** {answer}"
            break
    editedEmbedDescription = "\n".join(embedDescriptionListed)
    Embed.description = editedEmbedDescription

    await message.edit(embed=Embed)
    await ctx.followup.send(f"Introduction updated! {message.jump_url}")






@bot.tree.command(name="introduce-yourself", description="Command to introduce yourself.")
@choices(gender=[Choice(name="Male", value="male"), Choice(name="Female", value="female")])
@discord.app_commands.describe(birthday="DD/MM/YYYY Format.")
async def introduce_yourself(ctx: discord.Interaction, name: str, gender: Choice[str], age: int, birthday: str,
                             nationality: str, games: str, hobbies: str, languages: str, anything_note: str):
    await ctx.response.defer()
    intro_channel = [channel for channel in ctx.guild.channels if channel.name == introName]
    if intro_channel:
        intro_channel = intro_channel[0]
    else:
        return await ctx.followup.send(f"Channel `{introName}` not found!")

    names = [msg.embeds[0].author.name async for msg in intro_channel.history(limit=1000)]

    if ctx.user.name in names:
        return await ctx.followup.send("You have already introduced yourself!", ephemeral=True)

    description = f"**Name:** {name}\n**Gender:** {gender.name}\n**Age:** {age}\n**Birthday:** {birthday}\n**Nationality:** {nationality}\n**Games:** {games}\n**Languages:** {languages}\n**Hobbies:** {hobbies}"
    embed = discord.Embed(title=f"{ctx.user.name}'s Introduction", description=description, color=color_theme)
    embed.add_field(name="Note:", value=anything_note[:1024])
    embed.set_author(name=ctx.user.name, icon_url=ctx.user.avatar.url)
    embed.timestamp = datetime.now()

    await intro_channel.send(embed=embed)

    await ctx.followup.send("Introduction sent!", ephemeral=True)


@bot.tree.command(name="make-suggestion", description="Give a suggestion for a feature to add to the bot.")
@discord.app_commands.describe(anonymous="Whether you want your name to be shown with the suggestion or not.",
                               feature_summary="The title of the feature (Make sure it's not too long)",
                               feature="The actual feature (Make sure it's well explained)")
async def make_suggestion(ctx: discord.Interaction, feature_summary: str, feature: str, anonymous: bool):
    suggestion_channel = ctx.guild.get_channel(1145462208969588817)

    past_message = [message async for message in suggestion_channel.history(limit=1)][0]
    title = past_message.embeds[0].title
    counter = int(title[1:title.find(" ") + 1]) + 1

    embed = discord.Embed(title=f"#{counter} " + feature_summary[:254], description=feature[:4096], color=color_theme)
    embed.timestamp = datetime.now()
    if not anonymous:
        try:
            embed.set_author(name=ctx.user.name, icon_url=ctx.user.avatar.url)
        except:
            pass

    await suggestion_channel.send(embed=embed)

    await ctx.response.send_message("Suggestion created!", ephemeral=True)


bot.run(TOKEN)
