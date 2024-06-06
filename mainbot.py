import asyncio
import os
import discord
from botevent import Event # type: ignore
from botcommand import Command # type: ignore
from discord import Embed, app_commands
from discord.ext import commands
import sqlite3
import dotenv 

dotenv.load_dotenv()
 
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/",case_insensitive=True, intents=intents, heartbeat_timeout=60)
asyncio.run(bot.add_cog(Event(bot)))
asyncio.run(bot.add_cog(Command(bot)))

@bot.event
async def on_ready():
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Game(name="bingbomg"))
    print(f"{bot.user} aka {bot.user.name} has connected to Discord!")

    invite_link = discord.utils.oauth_url(
        bot.user.id,
        permissions=discord.Permissions(),
        scopes=("bot", "applications.commands")
    )
    print(f"Invite link: {invite_link}")






# Run the bot with your token
bot.run('')