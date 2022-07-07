import discord
from discord.ext import commands

class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = """
```
Prefix is "." (dot)

General commands:
ping - Returns the ping of the bot in ms
clear - Clears a specified number of messages in a channel or 10 by default
kick - Kicks a member from the server
ban - Bans a member from the server
unban - Unbans a member from the server

Music commands:
play <keywords> - Finds the song on youtube and plays it in your current channel. Will resume playing the current song if it was paused
queue - Displays the current music queue
skip - Skips the current song being played
clear - Stops the music and clears the queue
leave - Disconnects the bot from the voice channel
pause - Pauses the current song being played or resumes if already paused
resume - Resumes playing the current song
```
"""
        self.text_channel_list = []      

    @commands.command(name="help", help="Displays all the available commands")
    async def help(self, ctx):
        await ctx.reply(self.help_message)