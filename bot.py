import discord
import os
import sys
import json
import random
import time
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

saved_jerry = {}
time_since_last_command = int(time.time())

with open('jerry.txt', 'r') as f:
    saved_jerry = json.loads(f.read())

def spam_check(_time):
    global time_since_last_command
    if int(time.time()) < (_time + 2):
        return True

    time_since_last_command = int(time.time())
    return False

def file_check(id):
    if os.path.isfile(f'{id}.txt') != True:
        with open(f'{id}.txt', "w") as f:
            user_json = {
                "coins": 0,
                "items": [],
                "pats": 0
            }
            f.write(json.dumps(user_json))

def add_coins(id, amount):
    file_check(id)
    with open(f'{id}.txt', 'r') as f:
        user_json = json.loads(f.read())
        
    with open(f'{id}.txt', 'w') as f:
        user_json["coins"] = int(user_json["pats"]) + amount
        f.write(json.dumps(user_json))


def add_pats(id):
    file_check(id)
    with open(f'{id}.txt', 'r') as f:
        user_json = json.loads(f.read())
        
    with open(f'{id}.txt', 'w') as f:
        user_json["pats"] = int(user_json["pats"]) + 1
        f.write(json.dumps(user_json))
    
    saved_jerry["times_pet"] = int(saved_jerry["times_pet"]) + 1

    with open('jerry.txt', 'w') as f:
        f.write(json.dumps(saved_jerry))

def add_items(id, amount):
    pass

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    game_list = [
        "Overwatch",
        "Among Us",
        "VALORANT",
        "Minecraft",
        "The Elder Scrolls V: Skyrim Special Edition"
    ]
    await bot.change_presence(activity=discord.Game(name=random.choice(game_list)))

@bot.event
async def on_message(message):
    if message.content.startswith('<:jerry:765676912374186094>'):
        rand_num = random.randint(1, 100)
        if rand_num == 1:
            await message.channel.send("That's me! hehe")
            add_coins(message.author.id, 250)

    await bot.process_commands(message)            

@bot.command(name="hello", help="Say hi to Jerry")
async def hello(ctx):
    if spam_check(time_since_last_command):
        return

    await ctx.send(f'Hi, {ctx.author.name}!')

@bot.command(name="mood", help="Jerry will tell you his current mood")
async def mood(ctx):
    if spam_check(time_since_last_command):
        return
    pass

@bot.command(name="profile", help="Show's the users profile")
async def profile(ctx):
    if spam_check(time_since_last_command):
        return    
    user_id = ctx.author.id
    file_check(user_id)
    
    with open(f'{user_id}.txt', "r") as f:
        user_json = json.loads(f.read())

    embed=discord.Embed(title=f"{ctx.author.name}'s Profile", description="Shows all the stats Jerry remembers about you.", color=0x80ffff)
    embed.set_thumbnail(url="https://images.emojiterra.com/google/android-nougat/512px/1f422.png")
    embed.add_field(name="Jerry Coins", value=user_json["coins"], inline=True)
    embed.add_field(name="Pats", value=user_json["pats"], inline=True)
    embed.add_field(name="Items", value="None", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="pet", help="Give Jerry a pet")
async def pet(ctx):
    if spam_check(time_since_last_command):
        return    
    pet_messages = [
        f'I love pets! Thanks {ctx.author.name}! :blush:',
        f'Pets pets pets~ :grin:',
        f'Pet\'s always make me happy :blush:',
        f'Aww, thanks for the pets! You can have a pet too, {ctx.author.name}!',
        f'*RUFF RUFF* ...wait, I\'m not a dog...'
    ]
    special_messages = [
        "I hope you don't have feelings for me because it's weird to crush on a pet even after your crush turned you down.",
        "I don't get why you're always talking about her she already clowned you loser.",
        ":sunglasses:",
        "Jerry is a happy boi <:jerry:765676912374186094>"
    ]

    num = random.randrange(1,100)
    if num < 5:
        await ctx.send(random.choice(special_messages))
    else:
        await ctx.send(random.choice(pet_messages))

    add_pats(ctx.author.id)

@bot.command(name="status", help="Jerry's current stats")
async def status(ctx):
    if spam_check(time_since_last_command):
        return    
    embed=discord.Embed(title="Happiness", description="Jerry is a turtle, and just like all turtle's he loves being loved. Give Jerry a !pet!", color=0x80ffff)
    embed.set_author(name="Little Jerry")
    embed.set_thumbnail(url="https://images.emojiterra.com/google/android-nougat/512px/1f422.png")
    embed.add_field(name="Happiness", value=":blush:", inline=True)
    embed.add_field(name="Times Pet", value=saved_jerry["times_pet"], inline=True)
    await ctx.send(embed=embed)

@bot.command(name="coinflip", help="Jerry flips a coin for you")
async def coinflip(ctx):
    if spam_check(time_since_last_command):
        return    
    embed=discord.Embed(title="Jerry takes a coin out of his shell and throws it up into the air. The coin falls onto the ground and lands on...", description=random.choice(["**...HEADS**", "**...TAILS**"]), color=0x80ffff)
    embed.set_author(name="Little Jerry's Coin Flip")
    embed.set_thumbnail(url="https://images.emojiterra.com/google/android-nougat/512px/1f422.png")
    await ctx.send(embed=embed)

@bot.command(name="goodmorning", help="Say goodmorning to Jerry")
async def goodmorning(ctx):
    if spam_check(time_since_last_command):
        return    
    pass

@bot.command(name="goodnight", help="Say goodnight to Jerry(This will disconnect the bot)")
async def goodnight(ctx):
    if spam_check(time_since_last_command):
        return    
    await ctx.send(f'Goodnight, {ctx.author.name}!')

    with open('jerry.txt', 'w') as f:
        f.write(json.dumps(saved_jerry))

    try:
        await bot.close()
    except:
        print("Goodbye~")


bot.run(TOKEN)