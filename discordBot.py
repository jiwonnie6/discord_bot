from dotenv import load_dotenv
from discord.ext import commands, tasks
import discord, datetime, random, os
import yt_dlp as youtube_dl
from dataclasses import dataclass

CHANNEL_ID = 1098504441101029406

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())

# when bot is ready send success
@bot.event
async def on_ready():
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send('success')

# hello
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}")

# compliments
@bot.command()
async def compliment(ctx):
    compliments = ["You look beautiful right now :)", "Your face makes me soso happy :D ", "YOU LIGHT ME UP ! "]

    # sends random compliments from list
    await ctx.send(random.choice(compliments))


# sends a picture of your mood to the channel
@bot.command()
async def mood(ctx, input):
    if ctx.author == bot.user:
        return
    
    # iterate over files in directory and create a mood dictionary
    moods_dict = {}
    for filename in os.listdir('bot\kittyCats'):
        mood = filename.split('.')[0]
        moods_dict[mood] = os.path.join('bot\kittyCats', filename)

    # if input matches a mood send the coressponding image
    if input in moods_dict:
        mood = moods_dict[input]
        with open(mood, 'rb') as f:
            picture = discord.File(f)
            await ctx.channel.send(f'You are {input} kitty: ', file=picture)

    # if input is "list" send a list of the available moods to choose from
    elif input == "list":
        output = "Here is the list of moods you can choose from!\n"
        output += '\n'.join(moods_dict.keys())
        await ctx.channel.send(output)

    # if input is not a valid mood then send an error message and send a list of available moods
    else:
        output = "I do not have that mood available :( Here is the list of moods you can choose from!\n"
        output += '\n'.join(moods_dict.keys())

        await ctx.channel.send(output)


# number guessing game
@bot.command()
async def guessNum(ctx):
    if ctx.author == bot.user:
        return
    
    # generate random number between 1 and 100
    botNum = random.randint(1, 100)
    await ctx.channel.send("My number is between 1 - 100. \nYou have 5 tries. \nStart guessing!")

    # iterate for 5 tries
    for i in range(5):
        try:
            # wait for a message from the user within a 30 second timeout 
            guess = await bot.wait_for('message', timeout=30.0, check=lambda m: m.author != bot.user)

            # check if user wants to end game
            if guess.content == 'quit':
                await ctx.channel.send('The guessing game has ended.')
                break
            # convert the message to integer
            else:
                guess = int(guess.content)

        # handles if user message was non numeric or timeout period has exceeded
        except:
            await ctx.channel.send('Please enter a number between 1 - 100.')
            continue
        
        # if guess matched the number end game
        if guess == botNum:
            await ctx.channel.send('You guessed my number :0')
            break
        # if guess is not correct send hints
        elif guess > botNum:
            await ctx.channel.send('Guess lower!')
        else:
            await ctx.channel.send('Guess higher!')

    # send if all user used all 5 attempts without guessing correctly and end game
    else:
        await ctx.channel.send(f"Loser. You coudldn't guess my number :( My number was {botNum}.")


# tic tac toe game
@bot.command()
async def ttt(ctx):
    # make board thats empty
    board = ['-' for x in range(9)]

    # draw tic tac toe board
    def drawBoard():
        row1 = f'{board[0]}  |  {board[1]}  |  {board[2]}\n'
        row2 = f'{board[3]}  |  {board[4]}  |  {board[5]}\n'
        row3 = f'{board[6]}  |  {board[7]}  |  {board[8]}\n'
        return row1 + row2 + row3

    def win(board, piece):
        # all the winnings plays
        winPlays = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]

        # check if there is a winning play on the board
        for wins in winPlays:
            if board[wins[0]] == board[wins[1]] == board[wins[2]] == piece:
                return True
        else:
            return False
            
    async def playerMove(player, piece):
        # tell users who's turn it is and to enter their move
        await ctx.channel.send(f"{player}'s turn! You are {piece}.")
        await ctx.channel.send('Enter a number (1-9): ')
        move = await bot.wait_for('message', timeout=30.0)

        move = move.content

        # if user wants to quit return none
        if move == 'quit':
            return None

        # return the move the player chose
        if board[int(move) - 1] == '-':
            return int(move) - 1
        else:
            await ctx.channel.send('Invalid move. Try again.')
            return await playerMove(player, piece)

    # start tic tac toe game
    await ctx.channel.send('Tic tac toe game has started!')
    # enter the players' names
    await ctx.channel.send('Player 1 name: ')
    player1 = await bot.wait_for('message',timeout=20.0)
    await ctx.channel.send('Player 2 name: ')
    player2 = await bot.wait_for('message', timeout=20.0)

    player1 = player1.content
    player2 = player2.content
    turn = player1

    # if either player says quit before game started end game
    if player1 == 'quit' or player2 == 'quit':
        await ctx.channel.send('The tic tac toe game has ended.')
        return

    while True:
        try:
            await ctx.channel.send(drawBoard())

            # play game until the board is full or someone wins
            while '-' in board:
                if turn == player1:
                    move = await playerMove(player1, 'X')
                    # if move is none end game
                    if move is None:
                        await ctx.channel.send('The tic tac toe game has ended.')
                        return
                    board[move] = 'X'
                else:
                    move = await playerMove(player2, 'O')
                    # if move is none end game
                    if move is None:
                        await ctx.channel.send('The tic tac toe game has ended.')
                        return
                    board[move] = 'O'

                await ctx.channel.send(drawBoard())

                # check for wins otherwise the turn goes to the next player
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

                # if board fills up, tie
                if '-' not in board:
                    await ctx.channel.send("It's a tie!")
        # if user input not avaiable send error message and continue 
        except:
            await ctx.channel.send('Not a valid input. Try again.')
            continue


@bot.command()
async def bts(ctx):
    # check if user is in a voice channel and if not prompts user to enter one
    if not ctx.author.voice:
         await ctx.send('You are not in a voice channel. Please enter one to play the BTS game!')
    # checks if bot is connected to voice channel and if not connects it
    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()
    else:
        await ctx.channel.send('Already connected to voice channel.')

    # youtube download options
    ydl_opts = {
            'format': 'bestaudio', 
            'noplaylist': 'False',
            'playliststart': True,
            }
        
    # list of BTS song URls
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

    # shuffle the song URLs to be random each time
    random.shuffle(URLS)
    
    async def guessSong(title):
        #  user has three guesses
         guessCount = 3
         for i in range(3):
            try:
                response = await bot.wait_for('message', timeout=90.0)

                # if user quits then end game and disconnect the voice channel
                if response.content == 'quit':
                    await ctx.send('BTS game has ended.')
                    await ctx.voice_client.disconnect()
                    break

            except IndexError:
                return False

            # checks if user guess is correct
            if response.content.lower() == title.lower():
                await ctx.send('Correct! \nYou made BTS proud! A true ARMY <3')
                return
            # otherwise guess content goes down and tells user how many guesses they have left
            else:
                guessCount -= 1
                await ctx.send(f'Wrong answer. You have {guessCount} guesses left.')

                # if the guess content is 0 end the round 
                if guessCount == 0:
                    await ctx.send(f':( BTS is sad. \nThe song name was {title}')
                    return 
    
         
    async def playRandomSong(urls):
        for url in urls:
            # extracting information from youtube
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)

            songURL = info['url']
            songTitle = info['title']

            # play the song in the voice channel
            ctx.voice_client.play(discord.FFmpegPCMAudio(source=songURL,executable="C:\\Users\\jiwon\\Desktop\\stuff\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg"))
            await ctx.send('Guess the song title!')

            # wait for user to guess the song title
            await guessSong(songTitle)

            # stops playing current song
            ctx.voice_client.stop()


    await ctx.send(f'You are playing the BTS song guessing game!')

    # start plaing BTS songs to guess
    await playRandomSong(URLS)

# loads token from enviroment variable
load_dotenv()
bot.run(os.getenv('TOKEN'))