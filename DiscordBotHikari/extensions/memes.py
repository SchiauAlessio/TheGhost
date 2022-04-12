import os
from tempfile import TemporaryDirectory

import aiohttp
import requests
import lightbulb
import random
from lightbulb import commands
from lightbulb import context
import hikari
import http.client
import pytube
from pytube import YouTube,exceptions
plugin=lightbulb.Plugin("Memes")

@plugin.command()
@lightbulb.command("programmingmeme","bot sends meme")
@lightbulb.implements(commands.PrefixCommand,commands.SlashCommand)
async def cmd_sendmeme(ctx: context.PrefixContext | context.SlashContext) -> None:
    import requests

    url = "https://programming-memes-images.p.rapidapi.com/v1/memes"

    headers = {
        'x-rapidapi-host': os.getenv("PROGRAMMINGMEME_API_HOST"),
        'x-rapidapi-key': os.getenv("PROGRAMMINGMEME_API_KEY")
    }

    response = requests.request("GET", url, headers=headers)
    memejson=response.json()
    await ctx.respond(memejson[0]["image"])


@plugin.command()
@lightbulb.option("url","The url of the video you wish to download",type=str)
@lightbulb.command("downloadyt","bot sends youtube video")
@lightbulb.implements(commands.PrefixCommand,commands.SlashCommand)
async def cmd_sendmeme(ctx: context.PrefixContext | context.SlashContext) -> None:

    videourl = str(ctx.options.url)
    try:
        video = YouTube(videourl)
        stream = video.streams.get_by_resolution("720p")
        with TemporaryDirectory() as td:
            vd=stream.download(output_path=td)
            with open(vd,'rb') as f:
                await ctx.respond(hikari.File(str(f).split("'")[1]))
    except hikari.errors.ClientHTTPResponseError:
        await ctx.respond("File is too large, sorry. Keep in mind discord's file size limit.\n")
    except pytube.exceptions.RegexMatchError:
        await ctx.respond("Invalid url")
    except pytube.exceptions.VideoUnavailable:
        await ctx.respond("Video unavailable")


#todo train an image recognition algorithm to recognize chonky cats
@plugin.command()
@lightbulb.command("cat", "Searches the web for a random cat picture.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand,lightbulb.PrefixCommand)
async def randomcat(ctx: context.SlashContext|context.PrefixContext) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.thecatapi.com/v1/images/search") as response:
            if response.status == 200:
                catjson = await response.json()

                embed = hikari.Embed(title="🐱 Random kitten", color=0x0000FF)
                embed.set_image(catjson[0]["url"])
            else:
                embed = hikari.Embed(
                    title="🐱 Random kitten",
                    description="Oops! Looks like the cat delivery service is unavailable! Check back later.",
                    color=0xFF0000,
                )

            await ctx.respond(embed=embed)


@plugin.command()
@lightbulb.command("dog", "Searches the web for a random dog picture.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand,lightbulb.PrefixCommand)
async def randomdog(ctx: context.SlashContext|context.PrefixContext) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.thedogapi.com/v1/images/search") as response:
            if response.status == 200:
                dogjson = await response.json()

                embed = hikari.Embed(title="🐶 Random doggo", color=0x0000FF)
                embed.set_image(dogjson[0]["url"])
            else:
                embed = hikari.Embed(
                    title="🐶 Random doggo",
                    description="Oops! Looks like the dog delivery service is unavailable! Check back later.",
                    color=0xFF0000,
                )
            await ctx.respond(embed=embed)


@plugin.command()
@lightbulb.command("otter", "Searches the web for a random otter picture.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand,lightbulb.PrefixCommand)
async def randomotter(ctx: context.SlashContext|context.PrefixContext) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://otter.bruhmomentlol.repl.co/random") as response:
            if response.status == 200:
                otter_image = await response.content.read()

                embed = hikari.Embed(title="🦦 Random otter", color=0xA78E81)
                embed.set_image(hikari.Bytes(otter_image, "otter.jpeg"))
            else:
                embed = hikari.Embed(
                    title="🦦 Random otter",
                    description="Oops! Looks like the otter delivery service is unavailable! Check back later.",
                    color=0xFF0000,
                )

            await ctx.respond(embed=embed)


@plugin.command()
@lightbulb.command("food", "Searches the web for a random food picture.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand,lightbulb.PrefixCommand)
async def randomfood(ctx: context.SlashContext|context.PrefixContext) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://foodish-api.herokuapp.com/api/") as response:
            if response.status == 200:
                foodjson = await response.json()

                embed = hikari.Embed(title="🍕 Random food", color=0x0000FF)
                embed.set_image(foodjson["image"])
            else:
                embed = hikari.Embed(
                    title="🍕 Random food",
                    description="Oops! Looks like the food service is unavailable! Check back later.",
                    color=0xFF0000,
                )
            await ctx.respond(embed=embed)

def load(bot) -> None:
    bot.add_plugin(plugin)

def unload(bot) -> None:
    bot.remove_plugin(plugin)