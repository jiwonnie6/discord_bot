from discord.ext import commands
import discord, asyncio, os, queue, random
import yt_dlp as youtube_dl
from dataclasses import dataclass

BOT_TOKEN = 'MTEwNTA0NTk4MzY3NjYwNDQyNg.GrdNw-.4gqVf5P3_8gdNs0AKlBuqoTo3xwHhjUvvTU5us'
CHANNEL_ID = 1098504441101029406

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('success')
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send('success')

@bot.command()
async def play(ctx):
    if not ctx.author.voice:
         await ctx.send('You are not in a voice channel. Please enter one to play the BTS game!')
    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()
    else:
        await ctx.channel.send('Already connected to voice channel.')

    ydl_opts = {
            'format': 'bestaudio', 
            'noplaylist': 'False',
            'playliststart': True,
            }
        
    URLS = [
            'https://www.youtube.com/watch?v=e95-Gaj2iXM&list=PLP-tftygSBgr9wnES7vRGP88PqnUWe6KK&index=1',
            'https://www.youtube.com/watch?v=VEZ_Ui6d9AM&list=PLP-tftygSBgr9wnES7vRGP88PqnUWe6KK&index=2',
            'https://www.youtube.com/watch?v=1o0CtxZ_Cbo&list=PLP-tftygSBgr9wnES7vRGP88PqnUWe6KK&index=3',
            'https://www.youtube.com/watch?v=VMqDSntAbC0&list=PLP-tftygSBgr9wnES7vRGP88PqnUWe6KK&index=4',
            'https://www.youtube.com/watch?v=3J9G-PWo2oE&list=PLP-tftygSBgr9wnES7vRGP88PqnUWe6KK&index=5',
            'https://www.youtube.com/watch?v=zdLvqiOmWq4&list=PLP-tftygSBgr9wnES7vRGP88PqnUWe6KK&index=6',
            'https://www.youtube.com/watch?v=wIq2gPdj_68&list=PLP-tftygSBgr9wnES7vRGP88PqnUWe6KK&index=8',
            'https://www.youtube.com/watch?v=AEm5O3VnKi8&list=PLP-tftygSBgr9wnES7vRGP88PqnUWe6KK&index=13',
            'https://www.youtube.com/watch?v=SxAvr92fRg4&list=PLP-tftygSBgr9wnES7vRGP88PqnUWe6KK&index=14',
            'https://www.youtube.com/watch?v=9IVhjh15ofo&list=PLP-tftygSBgr9wnES7vRGP88PqnUWe6KK&index=16',
            'https://www.youtube.com/watch?v=F5H3g0UR7CI&list=PLP-tftygSBgr9wnES7vRGP88PqnUWe6KK&index=29',
            'https://www.youtube.com/watch?v=1yxEmmYQdl8&list=PLP-tftygSBgr9wnES7vRGP88PqnUWe6KK&index=33',
            'https://www.youtube.com/watch?v=LYUCYSszl7w&list=PLP-tftygSBgr9wnES7vRGP88PqnUWe6KK&index=37',
            'https://www.youtube.com/watch?v=e8loM2YykmE&list=PLP-tftygSBgr9wnES7vRGP88PqnUWe6KK&index=41',
            'https://www.youtube.com/watch?v=3J7rt7bkDCY',
            'https://www.youtube.com/watch?v=Fw7C6IsDYgI',
            'https://www.youtube.com/watch?v=NvK9APEhcdk&list=RD3J7rt7bkDCY&index=2'
        ]

    random.shuffle(URLS)
    
    async def guessSong(title):
         guessCount = 3
         for i in range(3):
            try:
                response = await bot.wait_for('message', timeout=90.0)
            except IndexError:
                return False

            if response.content.lower() == title.lower():
                await ctx.send('Correct! \nYou made BTS proud! A true ARMY <3')
                return
            else:
                guessCount -= 1
                await ctx.send(f'Wrong answer. You have {guessCount} guesses left.')

         await ctx.send(f':( BTS is sad. \nThe song name was {title}')
    
         
    async def playRandomSong(urls):
        for url in urls:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)

            songURL = info['url']
            songTitle = info['title']

            ctx.voice_client.play(discord.FFmpegPCMAudio(source=songURL,executable="C:\\Users\\jiwon\\Desktop\\stuff\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg"))
            await ctx.send('Guess the song title!')

            await guessSong(songTitle)
            ctx.voice_client.stop()


    await ctx.send(f'You are playing the BTS song guessing game!')
    await playRandomSong(URLS)


@bot.command()
async def quit(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send('You have ended the BTS game.')
    else:
        await ctx.send('You are not in a game.')

bot.run(BOT_TOKEN)