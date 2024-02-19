import discord
from discord.ext import commands

class help_cog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        
        self.help_message = """
        Kommandok:
        .play/.p
        .queue/.q
        .skip/.s
        .clear/.c
        .leave/.l
        .pause/.p
        .resume/.r 
        
        """
        self.text_ch_text = []
        
    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                self.text_ch_text.append(channel)
                
        await self.seld_to_all(self.help_message)
        
    async def send_to_all(self, msg):
        for text_channel in self.text_ch_text:
            await text_channel.send(msg)
            
    @commands.command(name="help", help="Segíts Mish!")
    async def help(self,ctx):
        await ctx.send(self.help_message)