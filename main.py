import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv

load_dotenv()

TOKEN = getenv("BOT_TOKEN")

bot = commands.Bot(intents=discord.Intents.all(), command_prefix="?!")


@bot.event
async def on_ready():
    print(f"{bot.user.name} is online.")
    print(f"{len(await bot.tree.sync())} commands loaded.")


@bot.event
async def on_member_join(member: discord.Member):
    member_role = member.guild.get_role(1145461173718896731)
    await member.add_roles(member_role, reason="New Member Role!")


bot.run(TOKEN)


