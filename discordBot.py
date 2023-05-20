from dotenv import load_dotenv
from discord.ext import commands, tasks
import discord, datetime, random, os
import yt_dlp as youtube_dl
from dataclasses import dataclass


# discord bo
CHANNEL_ID = 1098504441101029406
MAX_STUDY_TIME = 45

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())

@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0

session = Session()

@bot.event
async def on_ready():
    print('success')
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send('success')

# @tasks.loop(minutes=MAX_STUDY_TIME, count=2)
# async def break_reminder():
#     if break_reminder.current_loop == 0:
#         return
    
#     channel = bot.get_channel(CHANNEL_ID)
#     await channel.send(f"**Take a break!** You've been studying for {MAX_STUDY_TIME} minutes.")


@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}")

# @bot.command()
# async def compliment(ctx):
#     compliments = ["You look beautiful right now :)", "Your face makes me soso happy :D ", "YOU LIGHT ME UP ! "]

#     await ctx.send(random.choice(compliments))

@bot.command()
async def mood(ctx, input):
    if ctx.author == bot.user:
        return
    
    moods_dict = {}

    for filename in os.listdir('bot\kittyCats'):
        mood = filename.split('.')[0]
        moods_dict[mood] = os.path.join('bot\kittyCats', filename)

    if input in moods_dict:
        mood = moods_dict[input]
        with open(mood, 'rb') as f:
            picture = discord.File(f)
            await ctx.channel.send(f'You are {input} kitty: ', file=picture)
    elif input == "list":
        output = "Here is the list of moods you can choose from!\n"
        output += '\n'.join(moods_dict.keys())
        await ctx.channel.send(output)
    else:
        output = "I do not have that mood available :( Here is the list of moods you can choose from!\n"
        output += '\n'.join(moods_dict.keys())

        await ctx.channel.send(output)

    # output = "Choose a mood!\nI am:\n"
    # output += '\n'.join(moods_dict.keys())

    # await ctx.channel.send(output)

    # try:
    #     response = await bot.wait_for('message', timeout=30.0)
    # except:
    #     await ctx.channel.send('Please enter your mood!')

    # if response.content in moods_dict:
    #     mood = moods_dict[response.content]
    #     with open(mood, 'rb') as f:
    #         picture = discord.File(f)
    #         await ctx.channel.send(file=picture)
    # else:
    #     await ctx.channel.send('Invalid mood.')


    # produce random kitties
    # cats = ['bot\\angryCat.jpg', 'bot\curiousCat.jpg', 'bot\sickCat.jpg', 'bot\suspiciousCat.jpg']

    # cat = random.choice(cats)

    # with open(cat, 'rb') as f:
    #     picture = discord.File(f)

    #     await ctx.channel.send(file=picture)
    

@bot.command()
async def guessNum(ctx):
    if ctx.author == bot.user:
        return
    
    botNum = random.randint(1, 100)
    await ctx.channel.send("My number is between 1 - 100. \nYou have 5 tries. \nStart guessing!")

    for i in range(5):
        try:
            guess = await bot.wait_for('message', timeout=30.0, check=lambda m: m.author != bot.user)

            if guess.content == 'quit':
                await ctx.channel.send('The guessing game has ended.')
                break
            else:
                guess = int(guess.content)

        except:
            await ctx.channel.send('Invalid input. Please enter a number between 1 - 100.')
            continue
        

        if guess == botNum:
            await ctx.channel.send('You guessed my number :0')
            break
        elif guess > botNum:
            await ctx.channel.send('Guess lower!')
        else:
            await ctx.channel.send('Guess higher!')

    else:
        await ctx.channel.send(f"Loser. You coudldn't guess my number :( My number was {botNum}.")

@bot.command()
async def ttt(ctx):
    board = ['-' for x in range(9)]

    def drawBoard():
        row1 = f'{board[0]}  |  {board[1]}  |  {board[2]}\n'
        row2 = f'{board[3]}  |  {board[4]}  |  {board[5]}\n'
        row3 = f'{board[6]}  |  {board[7]}  |  {board[8]}\n'
        return row1 + row2 + row3

    def win(board, piece):
        winPlays = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]

        for wins in winPlays:
            if board[wins[0]] == board[wins[1]] == board[wins[2]] == piece:
                return True
        else:
            return False
            
    async def playerMove(player, piece):
        await ctx.channel.send(f"{player}'s turn! You are {piece}.")
        await ctx.channel.send('Enter a number (1-9): ')
        move = await bot.wait_for('message', timeout=30.0)

        move = move.content

        if move == 'quit':
            return None

        if board[int(move) - 1] == '-':
            return int(move) - 1
        else:
            await ctx.channel.send('Invalid move. Try again.')
            return await playerMove(player, piece)


    await ctx.channel.send('Tic tac toe game has started!')
    await ctx.channel.send('Player 1 name: ')
    player1 = await bot.wait_for('message',timeout=20.0)
    await ctx.channel.send('Player 2 name: ')
    player2 = await bot.wait_for('message', timeout=20.0)
    player1 = player1.content
    player2 = player2.content
    turn = player1

    if player1 == 'quit' or player2 == 'quit':
        await ctx.channel.send('The tic tac toe game has ended.')
        return

    while True:
        try:
            await ctx.channel.send(drawBoard())
            while '-' in board:
                if turn == player1:
                    move = await playerMove(player1, 'X')
                    if move is None:
                        await ctx.channel.send('The tic tac toe game has ended.')
                        return
                    board[move] = 'X'
                else:
                    move = await playerMove(player2, 'O')
                    if move is None:
                        await ctx.channel.send('The tic tac toe game has ended.')
                        return
                    board[move] = 'O'

                await ctx.channel.send(drawBoard())

                if win(board, 'X'):
                    await ctx.channel.send(f'{player1} wins!')
                    return
                if win(board, 'O'):
                    await ctx.channel.send(f'{player2} wins!')
                    return
                if turn == player1:
                    turn = player2
                else:
                    turn = player1

                if '-' not in board:
                    await ctx.channel.send("It's a tie!")
        except:
            await ctx.channel.send('Not a valid input. Try again.')
            continue


@bot.command()
async def bts(ctx):
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

                if response.content == 'quit':
                    await ctx.send('BTS game has ended.')
                    await ctx.voice_client.disconnect()
                    break

            except IndexError:
                return False

            if response.content.lower() == title.lower():
                await ctx.send('Correct! \nYou made BTS proud! A true ARMY <3')
                return
            else:
                guessCount -= 1
                await ctx.send(f'Wrong answer. You have {guessCount} guesses left.')
                if guessCount == 0:
                    await ctx.send(f':( BTS is sad. \nThe song name was {title}')
                    return 
    
         
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


# @bot.command()
# async def start(ctx):
#     if session.is_active:
#         await ctx.send("A session is already active!")
#         return 
    
#     session.is_active = True
#     session.start_time = ctx.message.created_at.timestamp()
#     readable_time = ctx.message.created_at.strftime("%H:%M:%S")
#     break_reminder.start()
#     await ctx.send(f"New session started at {readable_time}")
    
# @bot.command()
# async def end(ctx):
#     if not session.is_active:
#         await ctx.send("No session is active!")
#         return 

#     session.is_active = False
#     end_time = ctx.message.created_at.timestamp()
#     duration = end_time - session.start_time
#     readable_time = str(datetime.timedelta(seconds=duration))
#     break_reminder.stop()
#     await ctx.send(f"Session ended after {readable_time} seconds")

# with open('C:\\Users\\jiwon\\Desktop\\stuff\\python\\bots\\token.txt') as f:
#     BOT_TOKEN = f.readline()



load_dotenv()

    
bot.run(os.getenv('TOKEN'))