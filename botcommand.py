import asyncio
import discord
import os
from discord import Embed, app_commands
from discord.ext import commands
import sqlite3

class Command(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot

    


    @commands.hybrid_command(name="ping", description="pong")
    async def ping(self, ctx):
        '''PONG'''
        latency = self.bot.latency * 1000
        await ctx.send(f"Pong! Latency: {latency:.2f} ms")
    
    @commands.hybrid_command(name="myswag", description="Check your swag")
    async def myswag(self,ctx,member:discord.Member = None):
        if member is None:
            member = ctx.author
        db= sqlite3.connect(f"/auratracker/main.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT swag FROM main WHERE user_id = {member.id}")
        bal = cursor.fetchone()
        try:
            swag=bal[0]
        except:
            swag=0
        
        await ctx.send(f"{member} has {swag} Swag points.")
        cursor.close()
        db.close()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        channel = await self.bot.fetch_channel(reaction.channel_id)
        message = await channel.fetch_message(reaction.message_id)
    
    
        db= sqlite3.connect(f"/auratracker/main.sqlite")
        cursor = db.cursor()
        author=message.author
        if reaction.emoji.name=="🔥": #and reaction.member.id != author.id:
            
            cursor.execute(f"SELECT swag FROM main WHERE user_id={author.id}")
            wallet=cursor.fetchone()
            sql = (f"UPDATE main SET swag = ? WHERE user_id = ?")
            val = (wallet[0] + int(100), author.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
            
        if reaction.emoji.name=="🤓" and reaction.member.id != author.id:
            cursor.execute(f"SELECT swag FROM main WHERE user_id={author.id}")
            wallet=cursor.fetchone()
            sql = (f"UPDATE main SET swag = ? WHERE user_id = ?")
            val = (wallet[0] + int(-100), author.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
            
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, reaction):
        channel = await self.bot.fetch_channel(reaction.channel_id)
        message = await channel.fetch_message(reaction.message_id)
    
    
        db= sqlite3.connect(f"/auratracker/main.sqlite")
        cursor = db.cursor()
        author=message.author
        if reaction.emoji.name=="🔥":
            
            cursor.execute(f"SELECT swag FROM main WHERE user_id={author.id}")
            wallet=cursor.fetchone()
            sql = (f"UPDATE main SET swag = ? WHERE user_id = ?")
            val = (wallet[0] + int(-100), author.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
            
        if reaction.emoji.name=="🤓":
            cursor.execute(f"SELECT swag FROM main WHERE user_id={author.id}")
            wallet=cursor.fetchone()
            sql = (f"UPDATE main SET swag = ? WHERE user_id = ?")
            val = (wallet[0] + int(100), author.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

    @commands.hybrid_command(name="leaderboard",description="Check the swag rankings!")
    async def Leaderboard(self,ctx):
        db=sqlite3.connect("/auratracker/main.sqlite")
        cursor=db.cursor()
        query = 'SELECT user_id,swag FROM main ORDER BY swag DESC'  
        cursor.execute(query)

        user_ids = cursor.fetchall()

        cursor.close()
        db.close()
        
        embed=discord.Embed(title='Swag Leaderboard', description="Who's the swaggiest?")
        i=0
        for user in user_ids:
            username=ctx.bot.get_user(int(user[0])).display_name
            if i==0:
                pastestring=f"👑 {username} 👑: {str(user[1])}"
            else:
                pastestring=f"{i+1} - {username}: {str(user[1])}"
            embed.add_field(name=pastestring, value='', inline=False)
            i+=1
        await ctx.send(content="Leaderboard", embed=embed)
        
        

