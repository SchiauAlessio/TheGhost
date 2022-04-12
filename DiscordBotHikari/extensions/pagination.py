import lightbulb
import hikari
from lightbulb import commands
from lightbulb.utils import nav,pag
from lightbulb.utils.pag import StringPaginator
plugin=lightbulb.Plugin("Pagination")

@plugin.command()
@lightbulb.command("members","Display a list of the server members")
@lightbulb.implements(lightbulb.PrefixCommand,lightbulb.SlashCommand)
async def cmd_members(ctx:lightbulb.Context)->None:
    members=await ctx.bot.rest.fetch_members(ctx.guild_id)
    paginator=pag.EmbedPaginator(max_lines=10)

    for i,member in enumerate(members,start=1):
        paginator.add_line(f"**{i:,}.** {member.display_name}")

    netscape=nav.ButtonNavigator(paginator.build_pages())
    await netscape.run(ctx)


def load(bot) -> None:
    bot.add_plugin(plugin)

def unload(bot) -> None:
    bot.remove_plugin(plugin)