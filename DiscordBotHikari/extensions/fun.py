import lightbulb
import random
from lightbulb import commands
from lightbulb import context
import hikari
import miru
from enum import IntEnum
import typing as t
import aiohttp
plugin= lightbulb.Plugin("Fun")

@plugin.command()
@lightbulb.command("hello","bot says hello")
@lightbulb.implements(commands.PrefixCommand,commands.SlashCommand)
async def cmd_hello(ctx: context.PrefixContext | context.SlashContext) -> None:
    greetings = random.choice(("Hello","Hi","Hey","How about you fuck off","Yo","What's up","Greetings"))
    await ctx.respond(f"{greetings} {ctx.member.mention}!",user_mentions=True)

@plugin.command()
@lightbulb.option("bonus","A fixed number to add to the total roll number", int, default=0)
@lightbulb.option("sides","Number of sides of the die", int, default=6)
@lightbulb.option("number","Number of dice to roll", int)
@lightbulb.command("dice","Roll one or more dice")
@lightbulb.implements(commands.PrefixCommand,commands.SlashCommand)
async def dice(ctx) -> None:
    bonus=ctx.options.bonus
    sides=ctx.options.sides
    number=ctx.options.number
    if number > 100:
        await ctx.respond("No more than 100 dice")
        return
    if sides > 100:
        await ctx.respond("No more than 100 sides")

    rolls=[random.randint(1,sides) for _ in range(number)]

    await ctx.respond(
        " + ".join(f"{roll}" for roll in rolls)
        + (f" + {bonus} (bonus) " if bonus else "")
        + f"=**{sum(rolls)+bonus:,}**"
    )


@plugin.command()
@lightbulb.add_cooldown(10.0,1,lightbulb.UserBucket)
@lightbulb.option("text","The text to print",modifier=commands.OptionModifier.CONSUME_REST)
@lightbulb.command("echo","I say something")
@lightbulb.implements(commands.PrefixCommand,commands.SlashCommand)
async def cmd_echo(ctx) -> None:
    await ctx.respond(ctx.options.text)


@plugin.command()
@lightbulb.add_cooldown(10.0,1,lightbulb.UserBucket)
@lightbulb.option("text","The text to print",modifier=commands.OptionModifier.CONSUME_REST)
@lightbulb.option("count","How many times the text will be printed",int)
@lightbulb.command("repeat","I repeat something a number of given times")
@lightbulb.implements(commands.PrefixCommand,commands.SlashCommand)
async def cmd_repeat(ctx) -> None:
    for _ in range(ctx.options.count):
        await ctx.respond(ctx.options.text)


@plugin.command
@lightbulb.option("query", "The thing to search.")
@lightbulb.command("google", "Let me Google that for you...")
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_google(ctx: lightbulb.SlashContext) -> None:
    q = ctx.options.query

    if len(q) > 500:
        await ctx.respond("Your query should be no longer than 500 characters.")
        return

    await ctx.respond(f"<https://letmegooglethat.com/?q={q.replace(' ', '+')}>")


@plugin.command()
@lightbulb.command("barbut","Play barbut with the bot")
@lightbulb.implements(commands.PrefixCommand,commands.SlashCommand)
async def cmd_barbut(ctx)->None:
    you_rolled = random.randint(1, 12)
    bot_rolled = random.randint(1, 12)
    embed = hikari.Embed(title="Barbot", description="The Game of Dice. You win or you die.", color=0xff0000)
    embed.add_field(name="You Rolled ", value=format(you_rolled))
    embed.add_field(name="Ghost Rolled ", value=format(bot_rolled))
    await ctx.respond(embed=embed)
    if you_rolled == bot_rolled:
        await ctx.respond("`Looks like you rolled the same!`")
    elif you_rolled < bot_rolled:
        await ctx.respond("`Looks like Ghost rolled more than you. Better luck next time!`")
    else:
        await ctx.respond("`Looks like YOU rolled more than Ghost!`")


@plugin.command()
@lightbulb.option("player","The player you want to play against",type=hikari.Member,modifier=commands.OptionModifier.CONSUME_REST)
@lightbulb.command("barbutpvp","Play barbut against someone else")
@lightbulb.implements(commands.PrefixCommand,commands.SlashCommand)
async def barbut_pvp(ctx):
    you_rolled = random.randint(1, 12)
    second_player_rolled = random.randint(1, 12)
    embed = hikari.Embed(title="Barbot", description="The Game of Dice. You win or you die.", color=0xff0000)
    embed.add_field(name="You Rolled ", value=format(you_rolled))
    embed.add_field(name="{}".format(ctx.options.player), value=format(second_player_rolled))
    await ctx.respond(embed=embed,user_mentions=True)
    if you_rolled == second_player_rolled:
        await ctx.respond("`Looks like you rolled the same!`")
    elif you_rolled < second_player_rolled:
        await ctx.respond("`Looks like {} rolled more than you. Better luck next time!`".format(ctx.options.player))
    else:
        await ctx.respond("`Looks like YOU rolled more than {}!`".format(ctx.options.player))



class WinState(IntEnum):
    PLAYER_X = 0
    PLAYER_O = 1
    TIE = 2


class TicTacToeButton(miru.Button):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(style=hikari.ButtonStyle.SECONDARY, label="\u200b", row=y)
        self.x: int = x
        self.y: int = y

    async def callback(self, ctx: miru.Context) -> None:
        if isinstance(self.view, TicTacToeView) and self.view.current_player.id == ctx.user.id:
            view: TicTacToeView = self.view
            value: int = view.board[self.y][self.x]

            if value in (view.size, -view.size):
                return

            if view.current_player.id == view.playerx.id:
                self.style = hikari.ButtonStyle.DANGER
                self.label = "X"
                self.disabled = True
                view.board[self.y][self.x] = -1
                view.current_player = view.playero
                embed = hikari.Embed(
                    title="Tic Tac Toe!",
                    description=f"It is **{view.playero.display_name}**'s turn!",
                    color=0x009DFF,
                )
                embed.set_thumbnail(view.playero.display_avatar_url)

            else:
                self.style = hikari.ButtonStyle.SUCCESS
                self.label = "O"
                self.disabled = True
                view.board[self.y][self.x] = 1
                view.current_player = view.playerx
                embed = hikari.Embed(
                    title="Tic Tac Toe!",
                    description=f"It is **{view.playerx.display_name}**'s turn!",
                    color=0xFF0000,
                )
                embed.set_thumbnail(view.playerx.display_avatar_url)

            winner = view.check_winner()

            if winner is not None:

                if winner == WinState.PLAYER_X:
                    embed = hikari.Embed(
                        title="Tic Tac Toe!",
                        description=f"**{view.playerx.display_name}** won!",
                        color=0x77B255,
                    )
                    embed.set_thumbnail(view.playerx.display_avatar_url)

                elif winner == WinState.PLAYER_O:
                    embed = hikari.Embed(
                        title="Tic Tac Toe!",
                        description=f"**{view.playero.display_name}** won!",
                        color=0x77B255,
                    )
                    embed.set_thumbnail(view.playero.display_avatar_url)

                else:
                    embed = hikari.Embed(title="Tic Tac Toe!", description=f"It's a tie!", color=0x77B255)
                    embed.set_thumbnail(None)

                for button in view.children:
                    assert isinstance(button, miru.Button)
                    button.disabled = True

                view.stop()

            await ctx.edit_response(embed=embed, components=view.build())


class TicTacToeView(miru.View):
    def __init__(self, size: int, playerx: hikari.Member, playero: hikari.Member, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.current_player: hikari.Member = playerx
        self.size: int = size
        self.playerx: hikari.Member = playerx
        self.playero: hikari.Member = playero

        if size in [3, 4, 5]:
            self.board = [[0 for _ in range(size)] for _ in range(size)]

        else:
            raise TypeError("Invalid size specified. Must be either 3, 4, 5.")

        for x in range(size):
            for y in range(size):
                self.add_item(TicTacToeButton(x, y))

    async def on_timeout(self) -> None:
        for item in self.children:
            assert isinstance(item, miru.Button)
            item.disabled = True

        embed = hikari.Embed(
            title="Tic Tac Toe!",
            description="This game timed out! Try starting a new one!",
            color=0xFF0000,
        )
        assert self.message is not None
        await self.message.edit(embed=embed, components=self.build())

    def check_blocked(self) -> bool:
        """
        Check if the board is blocked
        """
        blocked_list = [False, False, False, False]

        # Check rows
        blocked = []
        for row in self.board:
            if not (-1 in row and 1 in row):
                blocked.append(False)
            else:
                blocked.append(True)

        if blocked.count(True) == len(blocked):
            blocked_list[0] = True

        # Check columns
        values = []
        for col in range(self.size):
            values.append([])
            for row in self.board:
                values[col].append(row[col])

        blocked = []
        for col in values:
            if not (-1 in col and 1 in col):
                blocked.append(False)
            else:
                blocked.append(True)
        if blocked.count(True) == len(blocked):
            blocked_list[1] = True

        # Check diagonals
        values = []
        diag_offset = self.size - 1
        for i in range(0, self.size):
            values.append(self.board[i][diag_offset])
            diag_offset -= 1
        if -1 in values and 1 in values:
            blocked_list[2] = True

        values = []
        diag_offset = 0
        for i in range(0, self.size):
            values.append(self.board[i][diag_offset])
            diag_offset += 1
        if -1 in values and 1 in values:
            blocked_list[3] = True

        if blocked_list.count(True) == len(blocked_list):
            return True

        return False

    def check_winner(self) -> t.Optional[WinState]:
        """
        Check if there is a winner
        """

        # Check rows
        for row in self.board:
            value = sum(row)
            if value == self.size:
                return WinState.PLAYER_O
            elif value == -self.size:
                return WinState.PLAYER_X

        # Check columns
        for col in range(self.size):
            value = 0
            for row in self.board:
                value += row[col]
            if value == self.size:
                return WinState.PLAYER_O
            elif value == -self.size:
                return WinState.PLAYER_X

        # Check diagonals
        diag_offset_1 = self.size - 1
        diag_offset_2 = 0
        value_1 = 0
        value_2 = 0
        for i in range(0, self.size):
            value_1 += self.board[i][diag_offset_1]
            value_2 += self.board[i][diag_offset_2]
            diag_offset_1 -= 1
            diag_offset_2 += 1
        if value_1 == self.size or value_2 == self.size:
            return WinState.PLAYER_O
        elif value_1 == -self.size or value_2 == -self.size:
            return WinState.PLAYER_X

        if self.check_blocked():
            return WinState.TIE


@plugin.command()
@lightbulb.option("size", "The size of the board. Default is 3.",int,default=3, required=False)
@lightbulb.option("user", "The user to play tic tac toe with!", type=hikari.Member)
@lightbulb.command("tictactoe", "Play tic tac toe with someone!")
@lightbulb.implements(lightbulb.SlashCommand,lightbulb.PrefixCommand)
async def tictactoe(ctx: context.SlashContext) -> None:
    assert ctx.member is not None

    if ctx.options.user.id == ctx.author.id:
        embed = hikari.Embed(
            title="❌ Invoking self",
            description=f"I'm sorry, but how would that even work?",
            color=0xFF0000,
        )
        await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        return

    if not ctx.options.user.is_bot:
        embed = hikari.Embed(
            title="Tic Tac Toe!",
            description=f"**{ctx.options.user.display_name}** was challenged for a round of tic tac toe by **{ctx.member.display_name}**!\nFirst to a row of **{ctx.options.size} wins!**\nIt is **{ctx.member.display_name}**'s turn!",
            color=0x009DFF,
        )
        embed.set_thumbnail(ctx.member.display_avatar_url)

        view = TicTacToeView(ctx.options.size, ctx.member, ctx.options.user)
        proxy = await ctx.respond(embed=embed, components=view.build())
        view.start(await proxy.message())

    else:
        embed = hikari.Embed(
            title="❌ Invalid user",
            description=f"Sorry, but you cannot play with a bot! Check again in the future!",
            color=0xFF0000,
        )
        await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
        return





def load(bot) -> None:
    bot.add_plugin(plugin)
    miru.load(bot)

def unload(bot) -> None:
    bot.remove_plugin(plugin)