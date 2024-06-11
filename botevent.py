import asyncio
import discord
import os
from discord import Embed, app_commands
from discord.ext import commands
import sqlite3

class Event(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        
        db = sqlite3.connect(f"/auratracker/main.sqlite")
        cursor=db.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS main (
                       user_id INTEGER, swag INTEGER, guild_id INTEGER
        )''')
        
       
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
      
        author = message.author
        print(message.guild.id)
        db = sqlite3.connect(f"/auratracker/main.sqlite")
        cursor=db.cursor()
        cursor.execute(f"SELECT user_id FROM main WHERE user_id = {author.id} AND guild_id = {message.guild.id}")
        result=cursor.fetchone()
        if result is  None:
            sql = (f"INSERT INTO main(user_id,swag,guild_id) VALUES (?,?,?)")
            val = (author.id, 0, message.guild.id)
            cursor.execute(sql,val)

        db.commit()
        cursor.close()
        db.close()

