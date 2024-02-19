
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import Bot
from cogs.music_cog import music_cog
from cogs.help_cog import help_cog



#bot = discord.Client()
intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='>',intents=intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    await bot.wait_until_ready()
    await bot.add_cog(music_cog(bot))
    await bot.add_cog(help_cog(bot))
    
    print('Logged in as: {0.user.name} Bots user id: {0.user.id}'.format(bot))

    
TOKEN = load_dotenv(TOKEN)
bot.run(TOKEN)