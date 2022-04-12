import hikari
import lightbulb
from lightbulb import commands

plugin=lightbulb.Plugin("Groups",include_datastore=True)
plugin.d.words=[]


@plugin.command()
@lightbulb.command("word","Words group")
@lightbulb.implements(commands.PrefixCommandGroup,commands.SlashCommandGroup)
async def cmd_word(ctx) -> None:
    await ctx.respond("This is a group")


@cmd_word.child()
@lightbulb.option("word","The word to add",str)
@lightbulb.command("add","Add a word to the list")
@lightbulb.implements(commands.PrefixSubCommand,commands.SlashSubCommand)
async def cmd_word_add(ctx) -> None:
    plugin.d.words.append(ctx.options.word)
    await ctx.respond("Word added")


@cmd_word.child()
@lightbulb.option("word","The word to delete",str)
@lightbulb.command("delete","Delete a word from the list")
@lightbulb.implements(commands.PrefixSubCommand,commands.SlashSubCommand)
async def cmd_word_add(ctx) -> None:
    plugin.d.words.remove(ctx.options.word)
    await ctx.respond("Word deleted")

@cmd_word.child()
@lightbulb.command("print","Display the word list")
@lightbulb.implements(commands.PrefixSubCommand,commands.SlashSubCommand)
async def cmd_word_add(ctx) -> None:
    await ctx.respond(f"Words:"+", ".join(plugin.d.words))


def load(bot) -> None:
    bot.add_plugin(plugin)

def unload(bot) -> None:
    bot.remove_plugin(plugin)