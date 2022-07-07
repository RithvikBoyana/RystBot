from ast import alias
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(command_prefix = '.')
client.remove_command('help')

from help_cog import help_cog
from music_cog import music_cog

client.add_cog(help_cog(client))
client.add_cog(music_cog(client))

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity = discord.Game(f'DISCORD | .help'))
    print('Bot is ready')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Please type in a valid command")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required arguments. Please type in *all* arguments")    
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the necessary permissions")
    elif isinstance(error, commands.CommandOnCooldown):
      msg = "You are on cooldown, please try again in {:.2f}s".format(error.retry_after)
      await ctx.send(msg)

@client.command(name="ping", help="Returns the ping of the bot in ms")
async def ping(ctx):
    await ctx.reply(f'{round(client.latency * 1000)}ms')

@client.command(name="clear", aliases=["c"], help="Clears a specified number of messages in a channel or 10 by default")
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount):
    await ctx.channel.purge(limit=amount+1)

@client.command(name="kick", aliases=["k"], help="Kicks a member from the server")
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : commands.MemberConverter, *, reason=None):
    if(ctx.author == member):
        await ctx.reply('You can\'t kick yourself')
        return
    await member.kick(reason=reason)
    await ctx.reply(f'Kicked {member.mention}.')

@client.command(name="ban", aliases=["b"], help="Bans a member from the server")
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : commands.MemberConverter, *, reason=None):
    if(ctx.author == member):
        await ctx.reply('You can\'t ban yourself')
        return
    await member.ban(reason=reason)
    await ctx.reply(f'Banned {member.mention}.')

@client.command(name="unban", aliases=["ub"], help="Unbans a member from the server")
@commands.has_permissions(ban_members = True)
async def unban(ctx, *, member : commands.MemberConverter):
    bannedUsersList = await ctx.guild.bans()
    memberName, memberTag = member.split('#')
    for banEntry in bannedUsersList:
        user = banEntry.user
        if (user.name, user.discriminator) == (memberName, memberTag):
            await ctx.guild.unban(user)
            await ctx.reply(f'Unbanned user {member.mention}.')
            return
    await ctx.reply('User is either not banned or not found')

client.run(os.getenv('TOKEN'))