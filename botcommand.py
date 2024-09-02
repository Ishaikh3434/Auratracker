import asyncio
import discord
import os
from discord import Embed, app_commands
from discord.ext import commands
import sqlite3
import random as rd

class Command(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot

    
    global swagup,swagdown
    global swagalias
    swagup="🔥"
    swagdown="🤓"
    swagalias="Swag"

    @commands.hybrid_command(name="ping", description="pong")
    async def ping(self, ctx):
        '''PONG'''
        latency = self.bot.latency * 1000
        await ctx.send(f"Pong! Latency: {latency:.2f} ms")
    
    @commands.hybrid_command(name="pointsname", description="Change the name of the points tracked by the bot! Purely cosmetic.")
    async def pointsname(self,ctx,name):
        global swagalias
        swagalias=name
        await ctx.send(f"Now tracking {swagalias} points!")
    
    @commands.hybrid_command(name="mypoints", description=f"Check your points!")
    async def mypoints(self,ctx,member:discord.Member = None):
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
        
        await ctx.send(f"{member} has {swag} {swagalias} points.")
        cursor.close()
        db.close()
    
    @commands.hybrid_command(name="changereaction",description="Change the reactions the bot will grant/remove points for. Inputs must be emoji.")
    async def changereaction(self,ctx,emoteup:discord.Emoji=None,emotedown:discord.Emoji=None):
        global swagup,swagdown
        swagup,swagdown=emoteup,emotedown
        
        await ctx.send(f'You now gain {swagalias} when you get "{swagup}"-reacted, and lose {swagalias} when you get "{swagdown}"-reacted!')


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        channel = await self.bot.fetch_channel(reaction.channel_id)
        message = await channel.fetch_message(reaction.message_id)
    
    
        db= sqlite3.connect(f"/auratracker/main.sqlite")
        cursor = db.cursor()
        author=message.author
        if reaction.emoji.name==swagup and reaction.member.id != author.id:
            cursor.execute(f"SELECT swag FROM main WHERE user_id={author.id}")
            wallet=cursor.fetchone()
            sql = (f"UPDATE main SET swag = ? WHERE user_id = ?")
            val = (wallet[0] + int(100), author.id)
            cursor.execute(sql, val)
            db.commit()
            sql = (f"UPDATE main SET swag = ? WHERE user_id = ?")
            val = (wallet[0] + int(10), reaction.member.id)
            cursor.execute(sql, val)            
            db.commit()
            cursor.close()
            db.close()
            
        if reaction.emoji.name==swagdown and reaction.member.id != author.id:
            cursor.execute(f"SELECT swag FROM main WHERE user_id={author.id}")
            wallet=cursor.fetchone()
            sql = (f"UPDATE main SET swag = ? WHERE user_id = ?")
            val = (wallet[0] + int(-100), author.id)
            cursor.execute(sql, val)
            db.commit()
            sql = (f"UPDATE main SET swag = ? WHERE user_id = ?")
            val = (wallet[0] + int(-20), reaction.member.id)
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
        if reaction.emoji.name==swagup:
            
            cursor.execute(f"SELECT swag FROM main WHERE user_id={author.id}")
            wallet=cursor.fetchone()
            sql = (f"UPDATE main SET swag = ? WHERE user_id = ?")
            val = (wallet[0] + int(-100), author.id)
            cursor.execute(sql, val)
            db.commit()
            sql = (f"UPDATE main SET swag = ? WHERE user_id = ?")
            val = (wallet[0] + int(-10), reaction.member.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
            
        if reaction.emoji.name==swagdown:
            cursor.execute(f"SELECT swag FROM main WHERE user_id={author.id}")
            wallet=cursor.fetchone()
            sql = (f"UPDATE main SET swag = ? WHERE user_id = ?")
            val = (wallet[0] + int(100), author.id)
            cursor.execute(sql, val)
            db.commit()
            sql = (f"UPDATE main SET swag = ? WHERE user_id = ?")
            val = (wallet[0] + int(+20), reaction.member.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

    @commands.hybrid_command(name="leaderboard",description=f"Check the rankings!")
    async def Leaderboard(self,ctx):
        db=sqlite3.connect("/auratracker/main.sqlite")
        cursor=db.cursor()
        query = f'SELECT user_id,swag FROM main WHERE guild_id = {ctx.message.guild.id} ORDER BY swag DESC'  
        cursor.execute(query)

        user_ids = cursor.fetchall()

        cursor.close()
        db.close()
        
        embed=discord.Embed(title=f'{swagalias} Leaderboard', description="Who's winning?")
        i=0
        for user in user_ids:
            try:
                username=ctx.bot.get_user(int(user[0])).display_name
            except:
                username="Removed User"
            if i==0:
                pastestring=f"👑 {username} 👑: {str(user[1])}"
            else:
                pastestring=f"{i+1} - {username}: {str(user[1])}"
            embed.add_field(name=pastestring, value='', inline=False)
            i+=1
        await ctx.send(content="Leaderboard", embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        author=message.author
        bot=self.bot
        if message.author.bot:
            return
        if rd.randint(0,100) == 50:
            reaction_emoji='🔮'
            await message.add_reaction(reaction_emoji)
            def check(reaction, recipient):
                return recipient == message.author and str(reaction.emoji) == reaction_emoji and reaction.message == message 
            try:
                db= sqlite3.connect(f"/auratracker/main.sqlite")
                cursor = db.cursor()
                reaction, _ = await self.bot.wait_for('reaction_add', timeout=3.0, check=check)
                await message.remove_reaction(reaction_emoji,author)
                await message.remove_reaction(reaction_emoji,bot.user) 
                cursor.execute(f"SELECT swag FROM main WHERE user_id={author.id}")
                wallet=cursor.fetchone()
                sql = (f"UPDATE main SET swag = ? WHERE user_id = ?")
                val = (wallet[0] + int(100), author.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

            except asyncio.TimeoutError:
                await message.remove_reaction(reaction_emoji,author)
                await message.remove_reaction(reaction_emoji,bot.user)        

