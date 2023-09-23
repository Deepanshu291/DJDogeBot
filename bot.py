import discord
from discord.ext import commands
import os 
import time
from pytube import YouTube as yt
import shutil
from dotenv import load_dotenv

TOKEN = 'MTEyNDM4NTk1NTk3Mzk2Nzk5Mg.GyG3nb.aicc422lvGflGqaSDOZ1kqZs8LT7pXH0hPcJAg'
PREFIX = '!'
load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX,intents=intents)
bot.remove_command('help')

filename = "./data/songs.mp4"

queue = []


class DJBot:
    song_queue=[]
    url = ""
    looping =False
    current = ""
    title = []
    def __init__(self) -> None:
        print("Dj Bot is Started")

    def cleanup(self):
        shutil.rmtree(path="data")
        self.song_queue.clear()
        self.url = ""
        self.looping = False
        self.current = ""  

    def Downloader(self):
            ytube =  yt(url=self.url)
            self.title.append(ytube.title)
            aud = ytube.streams.get_audio_only().download(filename=f"{ytube.title}.mp4",output_path="data")
            # queue.append(aud)
            # self.song_queue.append(aud)
            print(self.song_queue)
            return aud

    def fileh():
        if os.path.exists("data"):
            shutil.rmtree(path="data")
        else:
            os.makedirs(name="data")


dj = DJBot()


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    
@bot.command(name="h")
async def help(ctx):
    embed = discord.Embed(
        title="🎶 DJ Bot Help 🎶",
        description="Here are the available commands and their descriptions:",
        color=discord.Color.green()
    )

    embed.add_field(name="➡️ #join", value="Join the voice channel.", inline=False)
    embed.add_field(name="⬅️ #leave", value="Leave the voice channel.", inline=False)
    embed.add_field(name="▶️ #play [URL]", value="Play a song from a URL.", inline=False)
    embed.add_field(name="⏸️ #pause", value="Pause the currently playing song.", inline=False)
    embed.add_field(name="⏯️ #resume", value="Resume the paused song.", inline=False)
    embed.add_field(name="⏹️ #stop", value="Stop playback and clear the queue.", inline=False)
    embed.add_field(name="📜 #queue", value="Display the queue of songs.", inline=False)
    embed.add_field(name="⏭️ #skip", value="Skip the currently playing song.", inline=False)
    embed.add_field(name="🔄 #loop", value="Toggle song looping on/off.", inline=False)
    embed.add_field(name="❓ #help", value="Display this help message.", inline=False)

    await ctx.send(embed=embed)


@bot.command(name="v")
async def version(ctx):
    await ctx.message.channel.send("Version 0.9.1")

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    print(channel)
    await channel.connect()

@bot.command()
async def leave(ctx):
    dj.cleanup()
    await ctx.voice_client.disconnect()




# @bot.command()
# async def play(ctx, url):
#     voice_client = ctx.voice_client

#     if voice_client is None:
#         channel = ctx.author.voice.channel
#         await channel.connect()

#     dj.url = url

#     def play_finished(error):
#         if error:
#             print(f"Error: {error}")

#         if dj.looping:
#             play_song()
#         elif dj.song_queue:
#             play_song()

#     def play_song():
#         dj.current = dj.Downloader()
#         voice_client.play(discord.FFmpegPCMAudio(dj.current), after=play_finished)

#     if voice_client and voice_client.is_connected():
#         if voice_client.is_playing():
#             dj.Downloader()
#         else:
#             play_song()



@bot.command()
async def play(ctx,url):
    voice_client = ctx.voice_client
    dj.url = url
   
    if voice_client is None:
        channel = ctx.author.voice.channel
        dj.current =  dj.Downloader()
        # dj.song_queue.append(dj.current)
        await channel.connect()

    print("its connected")
    if voice_client and voice_client.is_connected():
        
        if voice_client.is_playing():
            aud = dj.Downloader()
            dj.song_queue.append(aud)
        else:
            dj.current = dj.Downloader()
            
            def play_song():
                print(dj.song_queue)
                if dj.looping:
                     voice_client.play(discord.FFmpegPCMAudio(dj.current), after=play_finished)
                elif dj.song_queue:         
                    current = dj.song_queue.pop(0)
                    dj.title.pop(0)
                    voice_client.play(discord.FFmpegPCMAudio(current), after=play_finished)
                    
            def play_finished(error):
                if error:
                    print(f"Error: {error}")
                play_song()

            voice_client.play(discord.FFmpegPCMAudio(dj.current), after=play_finished)
            await ctx.send(f"Here is your Song {dj.title[0]}")
    else:
        await ctx.send("Bot is not in a voice channel. Use `!join` to make the bot join a voice channel.")
        await ctx.invoke(bot.get_command("playone"))
        

@bot.command()
async def playone(ctx):
    voice_client = ctx.voice_client
    if voice_client and voice_client.is_connected():
        voice_client.play(discord.FFmpegPCMAudio(dj.current))
        

@bot.command()
async def skip(ctx):
    voice_client = ctx.voice_client

    if voice_client and voice_client.is_connected():
        if dj.song_queue:
            voice_client.stop()
            await ctx.send("Skipped the current song.")
        else:
            await ctx.send("There are no more songs in the queue.")
    else:
        await ctx.send("Bot is not currently playing any song to skip.")


# @bot.command()
# async def skip(ctx):
#     voice_client = ctx.voice_client
    
#     if voice_client and voice_client.is_connected() and voice_client.is_playing():
#             voice_client.stop()
#             await ctx.send("Skipped the current song.")
#     elif not dj.song_queue:
#         voice_client.stop()
#         await ctx.send("Bot is not currently playing any song to skip.")
    
@bot.command()
async def queue(ctx):
    # for title, index in dj.title:
    if not dj.title:
        await ctx.send("The queue is empty.")
    else:
        embed = discord.Embed(title="Queue", color=discord.Color.dark_purple())
        for i, song in enumerate(dj.title):
            embed.add_field(name=f"Song {i + 1}", value=song, inline=False)
        await ctx.send(embed=embed)
    # await ctx.send(f"song : {dj.title} \n")

@bot.command()
async def loop(ctx):
    dj.looping = not dj.looping
    print(dj.current)
    if dj.looping:
        await ctx.send("Looping is enabled. The currently playing song will be looped.")
    else:
        await ctx.send("Looping is disabled.")

@bot.command()
async def pause(ctx):
    ctx.voice_client.pause()
    await ctx.send('Paused')

@bot.command()
async def resume(ctx):
    ctx.voice_client.resume()
    await ctx.send('Resumed')

@bot.command()
async def stop(ctx):
    # shutil.rmtree(path="data")
    ctx.voice_client.stop()
    await ctx.send('Stopped')

bot.run(os.getenv("TOKEN"))




# class DJBot:
#     song_queue=[]
#     url = ""
#     looping =False
#     current = ""
#     title = []
#     def __init__(self) -> None:
#         print("Dj Bot is Started")

#     def cleanup(self):
#         shutil.rmtree(path="data")
#         self.song_queue.clear()
#         self.url = ""
#         self.looping = False
#         self.current = ""  

#     def Downloader(self):
#             ytube =  yt(url=self.url)
#             self.title.append(ytube.title)
#             aud = ytube.streams.get_audio_only().download(filename=f"{ytube.title}.mp4",output_path="data")
#             # queue.append(aud)
#             # self.song_queue.append(aud)
#             print(self.song_queue)
#             return aud

#     def fileh():
#         if os.path.exists("data"):
#             shutil.rmtree(path="data")
#         else:
#             os.makedirs(name="data")


# dj = DJBot()




# @bot.command()
# async def play(ctx,url):
#     voice_client = ctx.voice_client   
#     dj.url = url
#     # await ctx.invoke(bot.get_command("join"))
#     if voice_client is None:
#         channel = ctx.author.voice.channel
#         dj.current =  dj.Downloader()
#         await channel.connect()
#         await ctx.send("Bot joined your voice Channel :)")

#     if voice_client and voice_client.is_connected():
        
#         if voice_client.is_playing():
#             aud = dj.Downloader()
#             dj.song_queue.append(aud)

#         else:
#             dj.current = dj.Downloader()
            
#             def play_song():
#                 print(dj.song_queue)
#                 if dj.looping:
#                      voice_client.play(discord.FFmpegPCMAudio(dj.current), after=play_finished)
#                 elif dj.song_queue:         
#                     current = dj.song_queue.pop(0)
#                     dj.title.pop(0)
#                     voice_client.play(discord.FFmpegPCMAudio(current), after=play_finished)

#             def play_finished(error):
#                 if error:
#                     print(f"Error: {error}")
#                 play_song()
#             voice_client.play(discord.FFmpegPCMAudio(dj.current), after = play_finished)

#     else:
#         await ctx.invoke(bot.get_command("playone"))
        

# @bot.command()
# async def playone(ctx):
#     voice_client = ctx.voice_client
#     if voice_client and voice_client.is_connected():
#         voice_client.play(discord.FFmpegPCMAudio(dj.current))
#         await ctx.send(f"Here is your Song {dj.title[0]}")

 

# bot.run(os.getenv("TOKEN"))
