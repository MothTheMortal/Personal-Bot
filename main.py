import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
from datetime import datetime
from discord.app_commands import Choice, choices
from discord import app_commands
from gtts import gTTS
import io
import asyncio
import pytube
import requests

load_dotenv()

tts_lock = asyncio.Lock()

TOKEN = getenv("BOT_TOKEN")

bot = commands.Bot(intents=discord.Intents.all(), command_prefix=".")

color_theme = 0x2fd034


@bot.event
async def on_ready():
    print(f"{bot.user.name} is online.")
    print(f"{len(await bot.tree.sync())} commands loaded.")


@bot.event
async def on_member_join(member: discord.Member):
    if member.bot:
        bot_role = member.guild.get_role(1145465466203152515)
        await member.add_roles(bot_role, reason="New Bot role!")
    else:
        member_role = member.guild.get_role(1145461173718896731)
        await member.add_roles(member_role, reason="New Member Role!")

@bot.event
async def on_message_delete(message: discord.Message):
    snipe_channel = message.guild.get_channel(1146317717540966430)
    async for msg in snipe_channel.history():
        await msg.delete()
    if message.attachments:
        await snipe_channel.send(files=message.attachments)
    else:
        await snipe_channel.send(f"{message.author.name}: {message.content}")

@bot.command(name="cat")
async def cat(ctx: commands.Context):
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    cat_img_url = response.json()[0]["url"]

    embed = discord.Embed(title="", description="", color=color_theme)
    embed.set_image(url=cat_img_url)
    await ctx.channel.send(embed=embed)


@bot.command(name="snipe")
async def snipe(ctx: commands.Context):
    snipe_channel = ctx.guild.get_channel(1146317717540966430)
    msg = [msg async for msg in snipe_channel.history()][0]
    if msg.attachments:
        await ctx.reply(files=msg.attachments)
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

    description = f"<:MLBB:1146157862901514343>: **MothTheMortal 1048896713**\n<:clashofclan:1146158873862995988>: **#2928URGPP**\n<:github:1146156218524631052>: **MothTheMortal**\n<:instagram:1146155920699686932>: **@xmothpvp**\n<:minecraft:1146157223823802518>: **MothTheMortal**\n<:steam:1146159493873418260>: **MothTheMortal**\n<:valorant:1146156993623625841>: **MothTheMortal#Moth**"
    embed = discord.Embed(title="MothTheMortal's Socials", description=description, color=color_theme)
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
        await ctx.send("The command is already running. Please wait.")
        return

    async with tts_lock:
        channel = ctx.author.voice.channel

        if not channel:
            await ctx.send("You are not in a voice channel.")

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
        await ctx.send("The command is already running. Please wait.")
        return

    async with tts_lock:
        channel = ctx.author.voice.channel

        if not channel:
            await ctx.send("You are not in a voice channel.")

        voice_client = await channel.connect()

        audio = gTTS(text, lang="en")
        audio.save("ttsaudio.mp3")

        source = discord.FFmpegPCMAudio("ttsaudio.mp3")
        voice_client.play(source)
        while voice_client.is_playing():
            await asyncio.sleep(1)
        await voice_client.disconnect()
        os.remove("ttsaudio.mp3")


@bot.tree.command(name="introduce-yourself", description="Command to introduce yourself.")
@choices(gender=[Choice(name="Male", value="male"), Choice(name="Female", value="female")])
@discord.app_commands.describe(birthday="DD/MM/YYYY Format.")
async def introduce_yourself(ctx: discord.Interaction, name: str, gender: Choice[str], age: int, birthday: str,
                             nationality: str, games: str, hobbies: str, languages: str, anything_note: str):
    intro_channel = ctx.guild.get_channel(1145593789130473573)
    names = [msg.embeds[0].author.name async for msg in intro_channel.history(limit=1000)]

    if ctx.user.name in names:
        return await ctx.response.send_message("You have already introduced yourself!", ephemeral=True)

    description = f"**Name:** {name}\n**Gender:** {gender.name}\n**Age:** {age}\n**Birthday:** {birthday}\n**Nationality:** {nationality}\n**Games:** {games}\n**Languages:** {languages}\n**Hobbies:** {hobbies}"
    embed = discord.Embed(title=f"{ctx.user.name}'s Introduction", description=description, color=color_theme)
    embed.add_field(name="Note:", value=anything_note[:1024])
    embed.set_author(name=ctx.user.name, icon_url=ctx.user.avatar.url)
    embed.timestamp = datetime.now()

    await intro_channel.send(embed=embed)

    await ctx.response.send_message("Introduction sent!", ephemeral=True)


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
