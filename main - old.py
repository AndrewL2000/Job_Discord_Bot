from operator import mod
import discord
import os
import asyncio
import datetime

from discord.ext import commands
from discord.ext.commands import check

from dotenv import load_dotenv
from time import *
from random import randint
from datetime import datetime

import gspread

from PIL import Image, ImageDraw, ImageFont, ImageSequence
import io

from webscrape import *
from webscrape import mapping

load_dotenv()

client = commands.Bot(command_prefix="?", help_command=None)
client.activity = discord.Game(name=f"{client.command_prefix}with my balls")

@client.event   # Decorator to register an event (ASYNC library -> Uses Callbacks)
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_ready():
    print(f"{client.user} is ready to help {len(client.guilds)} server(s).")
    
@client.event
async def on_disconnect():
    print(f"{client.user} has disconnected at {datetime.now()}.")

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     if message.content.startswith("o/"):
#         await message.channel.send("o/")

@client.command()
async def wakeup(ctx, member : discord.Member):
    try:
        if member.voice:
            channel_start = member.voice.channel
            for channel in ctx.guild.voice_channels:
                await member.move_to(channel)
                await asyncio.sleep(0.2)
            await member.move_to(channel_start)
            channel = client.get_channel(382867403777769473)    # job-search
            await channel.send(f"Wake up {member.mention}")
    except:
        print(f"{member.mention} left voice channel whilst getting moved")
        channel = client.get_channel(382867403777769473)    # job-search
        await channel.send(f"{member.mention}, You would run you little bitch")

@client.command()
async def mute(ctx, member: discord.Member):
    try:
        if member.voice:
            for i in range(1,10):
                await member.edit(mute=True)
                await asyncio.sleep(0.2)
                await member.edit(mute=False)
                await asyncio.sleep(0.2)
            await ctx.channel.send(f"Shut the fk up {member.mention}")
    except:
        print(f"{member.mention} left voice channel whilst getting moved")
        await ctx.channel.send(f"{member.mention}, You would run you little bitch")

@client.command()
async def name(ctx, member: discord.Member):
    try:    
        nicknames = ["Bart", "Homer", "Marge", "Lisa", "Milhouse", "Moe", "Ned", "Lenny", "Carl", "Maggie", "Mr Burns", "Comic Book Guy", "Smithers", "Ralph", "Apu", "Barney", "Krusty"]
        i = randint(0,len(nicknames)-1)
        await member.edit(nick=nicknames[i])
        await asyncio.sleep(0.5)
    except:
        print(f"{member.mention} cannot be remained")
        await ctx.channel.send(f"{member.mention}, You would run you little bitch")


@client.command()
async def ban(ctx, member: discord.Member):
    print(ctx.author)    
    try:
        if ctx.author:
            ctx.author.disconnect(force=True)
    except:
        print(f"{ctx.author.mention} left voice channel whilst getting moved")
        await ctx.channel.send(f"{ctx.author.mention}, You would run you little bitch")
        

# This always sends the same message to the same person.  Is that what you want?
@client.command(pass_context=True)
@commands.is_owner()  # The account that owns the bot
async def dm(ctx):
    await ctx.channel.send("?dm")
    members = []
    for channel in ctx.guild.voice_channels:
        for member in channel.members:
            members.append(member)
            print(member)
    print(members)



def member_list(ctx):
    members = []
    for channel in ctx.guild.voice_channels:
        for member in channel.members:
            members.append(member)
    print(members)


@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@client.command()
async def dc(ctx):
    await ctx.voice_client.disconnect()



@client.command()
async def job(ctx, jobField=None):
    channel = client.get_channel(382867403777769473)    # job-search
    #944463840068927572 job-search
    #382867403777769473 Astolbo spam

    sa = gspread.service_account()
    sh = sa.open('Job Listings')

    worksheet = sh.worksheet("job")
    data = worksheet.get_all_records()

    if data:
        embed = make_embed("Job Listings")
        embed.set_footer(text=f"Jobs listed here were last updated on {sh.lastUpdateTime[:10]}")
        msg = await channel.send(embed=embed)
        i = 0
        for job in data:
            url = job['URL']
            field = job['Fields']
            company = job['Company']
            deadline = job['Deadline']
            qualification = job['Qualification']
            posted = job['Date Added']
            if deadline=='N/A':
                notPassedDeadline = True
            else:
                deadline_dt = datetime.strptime(deadline, '%d %b %Y')
                notPassedDeadline =  deadline_dt > datetime.now()
            if (str(jobField).lower() in field.lower() or jobField == None or "any" in field.lower()) and notPassedDeadline:
                await client.wait_until_ready()
                hyperlink = f"[{company}]({url})"
                embed.add_field(name=f"Job [{i+1}]", value=hyperlink, inline=True)
                embed.add_field(name="Field", value=f"{field} ({qualification})", inline=True)
                embed.add_field(name="Deadline", value=f"{deadline} | Posted {posted}", inline=True)
                i = i + 1
                await msg.edit(embed=embed)
                if mod(i,5)==0 and i!=len(url):
                    embed = make_embed("Job Listings")
                    embed.set_footer(text=f"Jobs listed here were last updated on {sh.lastUpdateTime[:10]}")
                    msg = await channel.send(embed=embed)   
        await client.wait_until_ready()
        await channel.send("Add new jobs here on [Google Sheets] (https://docs.google.com/spreadsheets/d/10mbAQtgDh4VMxxaOn9-QVSY5UUi5WnFpSNlxmPAoM0M/edit?usp=sharing)")   


@client.command()
async def modcheck(ctx, text: discord.Member):
    my_text = str(text)[:-5] 
    my_font = ImageFont.truetype(font=f'./fonts/OpenSans-Bold.ttf', size=50)

    im = Image.open('./mod-check.gif')

    # Image width and height
    W, H = (im.width, im.height)

    # Text width and height
    w, h = ImageDraw.Draw(im).textsize(text=my_text, font=my_font)

    frames = []
    for frame in ImageSequence.Iterator(im):
        # Add text
        d = ImageDraw.Draw(frame)
        d.text(xy=((W-w)/2, 20), text=my_text, fill=0, font=my_font)
        del d
        
        b = io.BytesIO()
        frame.save(b, format="GIF")
        frame = Image.open(b)

        frames.append(frame)
    # Save as GIF
    frames[0].save('./mod-check-out.gif', save_all=True, append_images=frames[1:])

    await ctx.channel.send(file=discord.File('./mod-check-out.gif'))

@client.command()
async def furry(ctx):
    embed = make_embed("Owo")
    embed.set_image(url="https://c.tenor.com/ap980s7uK14AAAAC/come-sit-bathroom.gif")
    await ctx.channel.send(embed=embed)

@client.command()
async def newjob(ctx=None):
    sa = gspread.service_account()
    sh = sa.open('Job Listings')

    worksheet = sh.worksheet("job")
    data = worksheet.get_all_records()

    channel = client.get_channel(382867403777769473)
    
    if data:
        embed = make_embed("**NEW** Job Listings")
        embed.set_footer(text=f"Jobs listed here were last updated on {sh.lastUpdateTime[:10]}")
        msg = await channel.send(embed=embed)
        i = 0
        for job in data:
            date_added = job['Date Added']
            date_added = datetime.strptime(date_added, '%d %b %Y') 
            duration = datetime.now() - date_added
            if duration.total_seconds() <= 86400:
                url = job['URL']
                field = job['Fields']
                company = job['Company']
                deadline = job['Deadline']
                qualification = job['Qualification']
                await client.wait_until_ready()
                hyperlink = f"[{company}]({url})"
                embed.add_field(name=f"Job [{i+1}]", value=hyperlink, inline=True)
                embed.add_field(name="Field", value=f"{field} ({qualification})", inline=True)
                embed.add_field(name="Deadline", value=deadline, inline=True)
                i = i + 1
                await msg.edit(embed=embed)
                if mod(i,5)==0 and i!=len(url):
                    embed = make_embed("Job Listings")
                    embed.set_footer(text=f"Jobs listed here were last updated on {sh.lastUpdateTime[:10]}")
                    msg = await channel.send(embed=embed)  


@client.command()
async def JOB(ctx, field=None, job_type=None, ordering=None):
    url = mapping['gradconnection']['domain']
    args_raw = ["?job", field, job_type, ordering]
    args = []
    for arg in args_raw:
        if(type(arg)==str):
            args.append(arg.lower())

    # # Build url
    # args = sys.argv
    if len(args) == 1:
        url += mapping['gradconnection']['job_type']['grad']  + '/'
        url += 'sydney/'
        url += '?ordering=' + mapping['gradconnection']['ordering']['closing']

    elif len(args) == 3 or len(args) == 4: 
        field = args[1]
        job_type = args[2]
        for field_map in mapping['gradconnection']['field']:
            if field in field_map:
                field = field_map
        if job_type=="graduate":
            job_type = "grad"
        else:
            for job_type_map in mapping['gradconnection']['job_type']:
                if job_type in job_type_map:
                    job_type = job_type_map            
            

        url += mapping['gradconnection']['job_type'][job_type] + '/'
        url += mapping['gradconnection']['field'][field] + '/'
        url += 'sydney/'

        url += '?ordering='
        if len(args) == 4:
            ordering = args[3]
            for ordering_map in mapping['gradconnection']['ordering']:
                if ordering in ordering_map:
                    ordering = ordering_map  
            url += mapping['gradconnection']['ordering'][ordering]
        else:
            url += mapping['gradconnection']['ordering']['closing']

    # Webscrape
    (app_name_list,company_list,app_link_list,deadline_list) = mapping['gradconnection']['func'](url)
    channel = client.get_channel(382867403777769473)    # job-search
    
    if app_name_list:
        embed = make_embed("Job Listings")
        embed.set_footer(text=f"Jobs listed here were last updated on")
        msg = await channel.send(embed=embed)
        i = 0
        for j in range(len(app_name_list)):
            url = app_link_list[j]
            field = app_name_list[j]
            company = company_list[j]
            deadline = deadline_list[j]

            await client.wait_until_ready()
            hyperlink = f"[{company}]({url})"
            embed.add_field(name=f"Job [{i+1}]", value=hyperlink, inline=True)
            embed.add_field(name="Description", value=f"{field}", inline=True)
            embed.add_field(name="Deadline", value=f"{deadline}", inline=True)
            i = i + 1
            await msg.edit(embed=embed)
            if mod(i,5)==0 and i!=len(url):
                embed = make_embed("Job Listings")
                embed.set_footer(text=f"Jobs listed here were last updated on")
                msg = await channel.send(embed=embed)   
    



@client.command()
async def help(ctx):
    embed = make_embed("Commands")
    embed.add_field(name="?wakeup <@User>", value="Helps get the user's attention",inline=False)
    embed.add_field(name="?job <field>(Optional)", value="Job Listings",inline=False)
    embed.add_field(name="?modcheck <field>(Optional)", value="fish",inline=False)
    await ctx.channel.send(embed=embed)

        

def make_embed(desc=""):
    embed = discord.Embed(color=39679, description=desc) if desc else discord.Embed(color=39679)
    embed.set_author(name="Bnet", icon_url=client.user.avatar_url)
    return embed

async def on_loop():
    await client.wait_until_ready()

    channel = client.get_channel(382867403777769473)

    # Intro message
    embed = make_embed("Commands")
    embed.add_field(name="?wakeup <@User>", value="Helps get the user's attention",inline=False)
    embed.add_field(name="?job <field>(Optional)", value="Job Listings",inline=False)
    embed.add_field(name="?modcheck <field>(Optional)", value="fish",inline=False)

    await channel.send(embed=embed) 

    while True:
        await newjob()
        await asyncio.sleep(60*60*24)

client.loop.create_task(on_loop())
    
client.run(os.getenv("DISCORD_API"))    # Turns on the bot 
