import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
from datetime import datetime
from discord.app_commands import Choice, choices
load_dotenv()

TOKEN = getenv("BOT_TOKEN")

bot = commands.Bot(intents=discord.Intents.all(), command_prefix="?!")

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


@bot.tree.command(name="introduce-yourself", description="Command to introduce yourself.")
@choices(gender=[Choice(name="Male", value="male"), Choice(name="Female", value="female")])
async def introduce_yourself(ctx: discord.Interaction, name: str, gender: Choice[str], age: int, birthday: str, games: str, hobbies: str, anything_note: str):
    intro_channel = ctx.guild.get_channel(1145593789130473573)
    names = [msg.embeds[0].author.name async for msg in intro_channel.history(limit=1000)]

    if ctx.user.name in names:
        return await ctx.response.send_message("You have already introduced yourself!", ephemeral=True)

    description = f"Name: {name}\nGender: {gender.name}\nAge: {age}\nBirthday: {birthday}\nGames: {games}\nHobbies: {hobbies}"
    embed = discord.Embed(title=f"{ctx.user.name}'s Introduction", description=description, color=color_theme)
    embed.add_field(name="Note:", value=anything_note[:1024])
    embed.set_author(name=ctx.user.name, icon_url=ctx.user.avatar.url)
    embed.timestamp = datetime.now()

    await intro_channel.send(embed)

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
