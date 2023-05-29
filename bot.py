from datetime import datetime
import discord
from discord.ext import commands, tasks
import json
import configparser
from urllib.request import urlopen, Request
import os
import sys
from colorama import Fore
import asyncio
import ping3
intents = discord.Intents.default()
intents.typing = False  
intents.presences = False  
intents.message_content = True  

bot = commands.Bot(command_prefix='!', intents=intents)
config = configparser.ConfigParser()
config.read('config.cfg')
TOKEN = config.get('Discord', 'token')
GUILD_ID = config.getint('Discord', 'guild_id')
CHANNEL_ID_LEAVE_JOIN = config.getint('Discord', 'channel_id_leave_join')
CHANNEL_FOR_EMBED_PLAYER_INFO = config.getint('Discord', 'channel_for_embed_player_info')
server_address = config.get('Server', 'address')
server_port = config.get('Server', 'port')
EMBED_ID  = config.getint('Other', 'embed_id')

print(Fore.LIGHTGREEN_EX +"Starting Up")
print(Fore.MAGENTA +"Developed by iiferedon")

#Globals
NUM_LINES_OF_CARS = 0
           
@tasks.loop(seconds=2)
async def main_loop():
    buffer = "buffer.json"
    try:  
        url = "http://"+server_address+":"+server_port+"/JSON%7C"
        request = Request(url)
        response = urlopen(request, timeout=5)
        jso = response.read()
        response.close()
        global parsed
        parsed = json.loads(jso)
    except:
        print(Fore.RED +"Error, server unavailable.")
        sys.exit()
         
    if os.path.isfile(buffer):
        pass
    else:
        print(Fore.LIGHTRED_EX +"buffer.json does not exist. Creating a new one...")
      
        with open(buffer, "w") as file:
            pass
        print(Fore.GREEN + "buffer.json has been created...")  
    await asyncio.sleep(2) 
    filesize = os.path.getsize(buffer)
    while filesize == 0:
        with open(buffer, 'w') as json_file:
            json.dump(parsed, json_file)
            print(Fore.GREEN +"First Time Buffer Startup Success!")
            break
    cars = parsed["Cars"]
    num_lines = sum(1 for line in cars)
    x = range(1, num_lines)
    global NUM_LINES_OF_CARS  
    NUM_LINES_OF_CARS = num_lines
    
    async def send_embed_message(title, player, colour, model, skin, type):
        guild = bot.get_guild(GUILD_ID)
        if guild is None:
            print(f'Failed to find guild with ID: {GUILD_ID}')
            return

        channel = discord.utils.find(lambda c: c.id == CHANNEL_ID_LEAVE_JOIN and isinstance(c, discord.TextChannel), guild.channels)
        if channel is None:
            print(f'Failed to find channel with ID: {CHANNEL_ID_LEAVE_JOIN}')
            return
        
        if type == 1:
            embed = discord.Embed(
            title=title,
            color=colour
        )
            embed.add_field(name='Player', value=player, inline=True)
            embed.add_field(name='Car', value=model, inline=True)
            embed.add_field(name='Skin', value=skin, inline=True)
            await channel.send(embed=embed)
        else:
            embed = discord.Embed(
            title=title,
            description = player + " left",
            color=colour
        )
            await channel.send(embed=embed)
            
    #Logic
    f = open(buffer, "r")
    read_buffer = f.read()
    global read_json
    read_json = json.loads(read_buffer)
    if True:
        for i in range(num_lines):
            if parsed["Cars"][i]["IsConnected"] and read_json["Cars"][i]["IsConnected"]: #Value stays same, no join or leave
                pass
            elif read_json["Cars"][i]["IsConnected"] != True and parsed["Cars"][i]["IsConnected"]: #Joined Game
                print(Fore.GREEN +"JOINED GAME: Player: " + parsed["Cars"][i]["DriverName"] + ", is driving: " + parsed["Cars"][i]["Model"] + ", with skin: " + parsed["Cars"][i]["Skin"])
                title = "Player Connected"
                player = parsed["Cars"][i]["DriverName"]
                colour = 5763719
                model = parsed["Cars"][i]["Model"]
                skin = parsed["Cars"][i]["Skin"]
                type = 1
                await send_embed_message(title, player, colour, model, skin, type)
            elif parsed["Cars"][i]["IsConnected"] != True and read_json["Cars"][i]["IsConnected"]: #Left Game
                print(Fore.RED +"LEFT GAME: Player: " + parsed["Cars"][i]["DriverName"])
                title = "Player Disconnected"
                player = parsed["Cars"][i]["DriverName"]
                model = parsed["Cars"][i]["Model"]
                skin = parsed["Cars"][i]["Skin"]
                colour = 15548997
                type = 0
                await send_embed_message(title, player, colour, model, skin, type)
                f.close()
    if True:
        global num_lines_parsed
        num_lines_parsed = min(len(parsed["Cars"]), len(read_json["Cars"]))
        global users_in_session 
        users_in_session = 0
    for i in range(num_lines_parsed):
        if parsed["Cars"][i]["IsConnected"] and read_json["Cars"][i]["IsConnected"]:
            users_in_session += 1
    await bot.change_presence(activity=discord.Game(name=f"{users_in_session}/{num_lines} users in session"))
    print(Fore.LIGHTGREEN_EX +"Number of users in session:", users_in_session)
      
    #overwrite previous buffer with current server JSON
    with open(buffer, 'w') as json_file:
        json.dump(parsed, json_file)
        print(Fore.BLUE +"wrote to buffer")
        print("..")
        
    
    await asyncio.sleep(0)

@bot.command()
async def embedmessage(ctx):
    if not update_embed.is_running():
        await send_embed()
        update_embed.start() 
    else:
         await ctx.send(f'Error: Embedded message already exists, use [!deleteembed] to start a new one')
             
             
@bot.command()
async def deleteembed(ctx):
    if not update_embed.is_running():
        await ctx.send(f'Error: No Embedded message found!')
    else:
        update_embed.stop()
        try:
            message = await ctx.channel.fetch_message(EMBED_ID)
            await message.delete()
            await ctx.send("Embed deleted successfully.")
            modifyconfig('Other', 'embed_id', f'{0}')
        except discord.NotFound:
            await ctx.send("Embed not found.")
        except discord.Forbidden:
            await ctx.send("Bot does not have permission to delete messages.") 
        
                   
                   
def modifyconfig(section, item, new_value):
    config.set(section, item, new_value)
    with open('config.cfg', 'w') as configfile:
        config.write(configfile)
                             
async def send_embed():
    guild = bot.get_guild(GUILD_ID)
    channel = guild.get_channel(CHANNEL_FOR_EMBED_PLAYER_INFO)

    embed = discord.Embed(title="Server Status", description=f"Users Connected: {users_in_session}/{NUM_LINES_OF_CARS}")
    embed.add_field(name='Player', value='', inline=True)
    embed.add_field(name='Car', value='', inline=True)
    embed.add_field(name='Skin', value='', inline=True)
    message = await channel.send(embed=embed)
   
    global EMBED_ID
    EMBED_ID = message.id
    modifyconfig('Other', 'embed_id', f'{EMBED_ID}')
    print(Fore.MAGENTA +f"Started embed with: {EMBED_ID} as the message ID")

@tasks.loop(seconds=2)
async def update_embed():
    await bot.wait_until_ready()
    
    guild = bot.get_guild(GUILD_ID)
    channel = guild.get_channel(CHANNEL_FOR_EMBED_PLAYER_INFO)
    message = await channel.fetch_message(EMBED_ID)
    # Create a new embed for each update
    embed = discord.Embed(title=f"Live Server Status", description=f"Users Connected: {users_in_session}/{NUM_LINES_OF_CARS}",colour=5763719)
    for i in range(num_lines_parsed):
        if parsed["Cars"][i]["IsConnected"] and read_json["Cars"][i]["IsConnected"]:
            player_name = parsed['Cars'][i]['DriverName']
            car_model = parsed['Cars'][i]['Model']
            skin = parsed['Cars'][i]['Skin']
            
            embed.add_field(name=f"Client #{i}", value=f"**{player_name}** is driving **{car_model}** with skin **{skin}**", inline=False)
    await message.edit(embed=embed)


@main_loop.before_loop
async def before_my_loop():
    await bot.wait_until_ready()
    print(Fore.GREEN +"Bot Initialized")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    main_loop.start()

@bot.command()
async def ping(ctx):
    print(Fore.GREEN +"Ping Command Used")
    latency = bot.latency
    ping_ms = round(latency * 1000) 
    await ctx.send(f'Bot latency: {ping_ms}ms')

@bot.command()
async def pingserver(ctx):
    try:
        response_time = ping3.ping(server_address)
        if response_time is not None:
            response_time *= 1000  
            await ctx.send(f'[BOT to GAME SERVER]: {response_time:.2f} ms')
        else:
            await ctx.send(f'Error: Failed to ping {server_address}')
    except Exception as e:
        await ctx.send(f'Error: {str(e)}')

@bot.event
async def on_message(message):
    await bot.process_commands(message)  
    

bot.run(TOKEN)
