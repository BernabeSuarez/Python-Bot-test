import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from urllib import parse, request
import re

load_dotenv()

token = os.getenv("TOKEN")
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


@bot.command()
async def hola(ctx):
    """Saludo con nombre segun el autor del mensaje"""
    await ctx.send(f"Welcome {ctx.message.author}")


@bot.command()
async def ayuda(ctx):
    await ctx.send("Que quieres hacer:")
    await ctx.send(
        "Si queres ver un video de youtube: \n !youtube (Y el nombre del video que quieres ver)"
    )


@bot.command()
async def youtube(ctx, *, search):
    """Busca en youTube y devuelve el primer resultado que aparezca."""
    query_str = parse.urlencode({"search_query": search})
    html_content = request.urlopen("https://www.youtube.com/results?" + query_str)
    search_content = html_content.read().decode()
    search_result = re.findall(r"\/watch\?v=\w+", search_content)
    # print(search_result)

    await ctx.send("https://www.youtube.com/" + search_result[0])


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f"{member.name} joined {discord.utils.format_dt(member.joined_at)}")


@bot.command()
async def repeat(ctx, times: int, content="repeating..."):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)


bot.run(token)
