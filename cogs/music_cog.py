import asyncio
import discord 
from discord.ext import commands
from youtube_dl import YoutubeDL

class music_cog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        
        self.is_playing = False
        self.is_paused = False
        
        self.music_queue = []
        self.YDL_OPTIONS = {'format':'bestaudio','noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options':'-vn'}
        
        self.vc = None
        print('music cog inicializalva')
        
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download = False)['entries'][0]
            except Exception:
                return False
        return {'source': info['formats'][0]['url'], 'title': info['title']}
    
    async def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            
            m_url = self.music_queue[0][0]['source']
            self.music_queue.pop(0)
            
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS))
            asyncio.sleep(1)
            return self.play_next()
        else: 
            self.is_playing = False
            return
            
    async def play_music(self,ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()
                
                if self.vc == None:
                    await ctx.send('Nem tud Mish csatlakozni a bulihoz')
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])
                    
            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS))
            asyncio.sleep(1)
            await self.play_next()
        
        else:
            self.is_playing = False
            
            
            
            
            
            
            
    @commands.command(name="play",aliases=['p'],help = 'Zenét játszik mit hittél?')
    async def play(self, ctx, *args):
        query = " ".join(args)
        
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send('Csatlakozz előbb he!')
        elif self.is_paused:
            self.vc.resume()
        else: 
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send('Nem tudtam letölteni rossz a formátum vagy valami')
            else:
                await ctx.send('Vettem!')
                self.music_queue.append([song,voice_channel])
                
                if self.is_playing == False:
                    await self.play_music(ctx)
                    
    
    @commands.command(name='pause',aliases=['ps'],help = 'Megállj')
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused  = True
            self.vc.pause()
        elif self.is_paused:
            self.is_playing = True
            self.is_paused  = False
            self.vc.resume()         
            
    
    @commands.command(name='resume',aliases=['r'],help = 'Folyt')   
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.is_playing = True
            self.is_paused  = False
            self.vc.resume()
            
            
    @commands.command(name='skip',aliases=['s'],help = 'Nem tetccik')   
    async def skip(self, ctx, *args):
        if self.vc != None and self.vc:
            self.vc.stop()
            await self.play_music(ctx)
            
        
    @commands.command(name='queue',aliases=['q'],help = 'Mit hallgatunk')   
    async def queue(self, ctx, *args):
        retval = ""
        
        for i in range(0,len(self.music_queue)):
            if i > 4: break
            retval += self.music_queue[i][0]['title'] + '\n'
            
        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send('Üres he')
            
    @commands.command(name='clear',aliases=['c'],help = 'töröl')   
    async def clear(self, ctx, *args):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send('Törölve')
        
    @commands.command(name='leave',aliases=['l'],help = 'hess')   
    async def leave(self, ctx, *args):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()
        
def setup(bot):
    bot.add_cog(music_cog(bot))
             
           
            