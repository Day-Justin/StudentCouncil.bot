import nextcord
from nextcord.ext import commands
import youtube_dl


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.is_playing = False
        self.is_paused = False

        self.music_queue = []
        self.index = 0
        self.YDL_OPTIONS = {'format': "bestaudio"}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn'}
        self.vc = None

    def search_yt(self, query):
        with youtube_dl.YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % query, download=False)['entries'][0]
            except Exception:
                return False
            return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if self.index < len(self.music_queue):
            self.is_playing = True
            m_url = self.music_queue[self.index][0]['source']
            self.index += 1
            self.vc.play(nextcord.FFmpegOpusAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())

        else:
            self.is_playing = False

    async def play_music(self, ctx):
        if self.index < len(self.music_queue):
            self.is_playing = True
            m_url = self.music_queue[self.index][0]['source']

            if self.vc is None:  # or not self.vc.is_connected():
                self.vc = await self.music_queue[self.index][1].connect()

                if self.vc is None:
                    await ctx.send("Could not connect to voice channel.")

            else:
                await self.vc.move(self.music_queue[self.index][1])

            self.index += 1
            self.vc.play(nextcord.FFmpegOpusAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())

    @commands.command()
    async def join(self,ctx):
        if ctx.author.voice is None:
            await ctx.send("Your not even in the voice channel!")

        if self.vc is None:
            self.vc = ctx.author.voice.channel

        if ctx.voice_client is None:
            await self.vc.connect()
        else:
            await ctx.voice_client.move(self.vc)

    @commands.command(name='disconnect', aliases=['l'])
    async def disconnect(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()

    @commands.command(name='play', aliases=['P', 'p', 'Play'], help="Play some beats (yt only)")
    async def play(self, ctx, *args):
        query = " ".join(args)

        voice_channel = ctx.author.voice.channel
        await self.join(ctx)

        if self.is_paused:
            await self.resume( ctx)

        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not get song.")

            else:
                await ctx.send("Song added to queue")
                self.music_queue.append([song, voice_channel])

                if self.is_playing is False:
                    await self.play_music(ctx)

    @commands.command(name= 'pause', aliases=['Pause'])
    async def pause(self,ctx):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        await ctx.send("Paused ⏸")

    @commands.command(name='resume', aliases=["Resume"])
    async def resume(self,ctx):
        if self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()
        await ctx.send("Resuming ▶️")

    @commands.command(name='skip', aliases=['pn', 'Playnext', 'playnext', 's', 'Skip'])
    async def skip(self, ctx):
        if self.vc is not None and self.vc:
            self.vc.stop()
            await self.play_music(ctx)

    @commands.command(name='queue', aliases=['q', 'Queue'], help='Shows the current queue')
    async def queue(self, ctx):
        retval = ""

        for i in range(len(self.music_queue)):
            if i > 4: break
            retval += self.music_queue[i][0]['title'] + '\n'

        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue.")

    @commands.command(name='clear', aliases=['c', 'bin', 'Clear'])
    async def clear(self, ctx):
        if self.vc is not None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        self.index = 0
        await ctx.send("Music queue cleared.")


def setup(client):
    client.add_cog(Music(client))
