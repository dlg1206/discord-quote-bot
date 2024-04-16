"""
File: QuoteBot.py
Description: Collection of Commands for the Discord Bot

@author Derek Garcia
"""

import discord
from discord.ext import commands

from db.Database import Database
from quote.Quote import format_quotee
from util import Util

VERSION = "2.4"
SOURCE_CODE = "https://github.com/dlg1206/Discord-Quote-Bot"


class QuoteBot(commands.Bot):

    def __init__(self, database: Database):
        """
        Create new Bot

        :param database: Quote Database to use
        """
        super().__init__(command_prefix="!", intents=discord.Intents.all())
        self.database = database
        self.version = VERSION
        self.source_code = SOURCE_CODE

        # ADD CHANNEL ID'S TO EXCLUDE FROM QUOTE DETECTION
        self.blacklist_channels = []

        self.init_commands()

    def init_commands(self):
        """
        Register custom commands to the bot
        """

        @self.command()
        async def qadd(ctx, *, prompt=None):
            """
            Adds quote to quote dictionary and txt file
            :param ctx: command prefix
            :param prompt: Entire quote/author
            """
            # Check if prompt was given
            if prompt is None:
                await ctx.channel.send('Proper Usage: `!qadd "[quote]" -[Quotee]`')
                # log(ctx.message.author, "!qadd", False, "No args")    # TODO
                return

            # Else split
            key = '-'  # Custom Split key
            split_prompt = f"{prompt}".split(key)

            # Error check, should only be 2 parts
            if len(split_prompt) != 2:
                await ctx.channel.send('Sorry, I didn\'t get that :(\nCommand: `!qadd "[quote]" -[Quotee]`')
                return
                # log(ctx.message.author, "!qadd", False, f"invalid args: {prompt}")    # TODO

            # Quote is valid
            # Break quote into quote and quotee
            quote = split_prompt[0].replace("\"", "").strip()
            quotee = split_prompt[1].lower().strip()

            # Upload to db
            code = self.database.add_quote(quote, quotee, str(ctx.message.author))

            # Confirmation
            if code == 0:
                await ctx.channel.send("Quote added! :)")

            await self.change_presence(
                activity=discord.Game(f"{self.database.get_quote_total()} quotes and counting!"))

            # Record Outcome in data file
            # log(ctx.message.author, "!qadd", True, prompt) # TODO

        @self.command()
        async def q(ctx, *, quotee=None):
            """
            Get a random quote from given name

            :param ctx: command
            :param quotee: name to search quotes for
            """

            # check if quotee was given
            if quotee is None:
                await ctx.channel.send("Proper Usage: `!q [Name]`")
                # log(ctx.message.author, "!q", False, "No args")   # TODO
                return

            # If name exist in self.quote_data
            rand_quote = self.database.get_rand_quote(quotee)
            if rand_quote is not None:
                # Print quote and person
                await ctx.channel.send(rand_quote)
                # log(ctx.message.author, "!q", True)   # TODO
                return

            # If name not in QUOTES, print not found
            await ctx.channel.send("I don't have any quotes from " + f"{quotee}" + " :(")

            # list similar if any
            similar = [format_quotee(q) for q in self.database.find_similar_quotee(quotee)]
            if len(similar) != 0:
                await ctx.channel.send(f"Did you mean anyone here?\n{'\n'.join(similar)}")

            # log(ctx.message.author, "!q", False, f"No quotes from {quotee}")  # TODO

        @self.command()
        async def qall(ctx, *, quotee=None):
            """
            Get all the quotes for a specific person

            :param ctx: command
            :param quotee: name to search quotes for
            """

            if quotee is None:
                await ctx.channel.send("Proper Usage: `!qall [Name]`")
                # log(ctx.message.author, "!qall", False, "No args") # TODO
                return

            # Search for quotes
            quotes = self.database.get_all_quotes(quotee)

            # If no quotes, check for similar
            if len(quotes) == 0:
                await ctx.channel.send("I don't have any quotes from " + f"{format_quotee(quotee)}" + " :(")

                # list similar if any
                similar = [format_quotee(q) for q in self.database.find_similar_quotee(quotee)]
                if len(similar) != 0:
                    await ctx.channel.send(f"Did you mean anyone here?\n{'\n'.join(similar)}")

                # log(ctx.message.author, "!qall", False, f"No quotes from {quotee}")   # TODO
                return

            # Format and display all quotes
            only_quotes = [f'> - "{q.quote}"' for q in quotes]
            await ctx.channel.send(f"{'\n'.join(only_quotes)}"
                                   f"**{format_quotee(quotee)} has {len(quotes)} quotes!**")
            # log(ctx.message.author, "!qall", True)    # TODO

        @self.command()
        async def qrand(ctx):
            """
            Get random quote from entire quote dictionary

            :param ctx: Command
            """
            rand_quote = self.database.get_rand_quote()
            # Print Random quote and author
            await ctx.channel.send(rand_quote)

            # Record Outcome in data file
            # log(ctx.message.author, "!qrand", True) # TODO

        @self.command()
        async def qsearch(ctx, *, keywords=None):
            """
            Searches database for people's names. Either lists all or ones that match the keywords

            :param ctx: command
            :param keywords: optional keywords to look for
            """
            if keywords is None:
                # List ALL names in database
                all_quotees = [f"> {format_quotee(q)}" for q in self.database.get_all_quotees()]
                await ctx.channel.send(f"**I have quotes from all these people!**\n{'\n'.join(all_quotees)}")
                # log(ctx.message.author, "!qsearch", True)     # TODO
            else:
                # List names that match the keywords
                similar = [format_quotee(q) for q in self.database.find_similar_quotee(keywords)]
                if len(similar) != 0:
                    await ctx.channel.send(f"Here's what I could find:\n{'\n'.join(similar)}")
                    # log(ctx.message.author, "!qsearch [keywords]", True)  # TODO

        @self.command()
        async def qstat(ctx, *, quotee=None):
            """
            Gets Stats of QuoteBoi

            :param ctx: Command
            :param quotee: optional quotee field
            """
            # No args given print entire system info
            if quotee is None:
                # Print num quotes from num people
                await ctx.channel.send(
                    f"I have {self.database.get_quote_total()} quotes from {self.database.get_quotee_total()} people!")
                # log(ctx.message.author, "!qstat", True)   # TODO
                return

            # Check if in data
            num_quotes = self.database.get_quote_total(quotee)
            if num_quotes != 0:
                # Print quote and person
                await ctx.channel.send(f"{format_quotee(quotee)} has {num_quotes} quotes!")
                # log(ctx.message.author, "!qstat [quotee]", True, quotee)  TODO
            # No quotes from quotee
            else:
                # Print not found
                await ctx.channel.send("I don't have any quotes from " + f"{format_quotee(quotee)}" + " :(")

                # print similar if any
                similar = [format_quotee(q) for q in self.database.find_similar_quotee(quotee)]
                if len(similar) != 0:
                    await ctx.channel.send(f"Did you mean anyone here?\n{'\n'.join(similar)}")

                # log(ctx.message.author, "!qstat", False, f"No quotes from {quotee}")  # TODO

        @self.command()
        async def qhelp(ctx):
            """
            Prints command arguments

            :param ctx: Command
            """

            await ctx.channel.send(f"__**QuoteBoi Version: {self.version}**__\n" +
                                   f"Source Code: {self.source_code}\n" +
                                   "> - Add quote: `!qadd \"[quote]\" -[Quotee]`\n" +
                                   "> - Get Quote: `!q [Name]`\n" +
                                   "> - Get All quotes: `!qall [Name]`\n" +
                                   "> - Random Quote: `!qrand`\n" +
                                   "> - All People list: `!qsearch`\n" +
                                   "> - Keyword Search: `!qsearch [Keywords]`\n" +
                                   "> - Total Quote Stats: `!qstat`\n" +
                                   "> - Person Quote Stats: `!qstat [Name]`\n" +
                                   "> - Help: `!qhelp`")
            await ctx.channel.send("**'Quote Like' Support**\n" +
                                   "> QuoteBoi will detect 'Quote Like' messages in *roughly* the following format:\n" +
                                   "> `[pre-context] \"[quote]\" [post-context] -[quotee]`\n" +
                                   "> There's no guarantee, but it's good at detecting them. `!qadd` is the only way\n" +
                                   "> to add quotes for sure")
            # log(ctx.message.author, "!qhelp", True) # TODO

            return

        @self.command()
        @commands.is_owner()
        async def qkill(ctx):
            """
            Master kill switch from inside discord

            :param ctx: command
            """
            quote = self.database.get_rand_quote()
            await ctx.channel.send(f'Goodbye, and in the words of {format_quotee(quote.quotee)}: "{quote}"')
            exit(0)

    async def on_message(self, message) -> None:
        """
        Parses message and determines if it is 'quote like' and attempts to add it

        :param message: message to parse
        """

        await self.process_commands(message)  # exe any commands first

        # ignore any commands or messages from self
        if Util.is_command(message.content) or message.author.bot:
            return

        # ignore any none quote like commands
        if not Util.is_quote(message.content):
            return

        # Don't include quotes from blacklisted channels
        if message.channel.id in self.blacklist_channels:
            return

        # attempt to add quote
        if Util.add_quote(self.database, message):
            # log(message.author, "quote-like add", True, message.content)    # TODO
            await self.change_presence(
                activity=discord.Game(f"{self.database.get_quote_total()} quotes and counting!"))
        else:
            # log(message.author, "quote-like add", False, message.content) # TODO
            return

    async def on_ready(self) -> None:
        """
        Tells console that bot is active and basic info

        :return:
        """

        await self.change_presence(status=discord.Status.online,
                                   activity=discord.Game(f"{self.database.get_quote_total()} quotes and counting!"))
        print('{0.user}'.format(self) + " is online")
        print(f"Quote File: {self.database.db_location}")

        # log("admin", "run bot", True)   # TODO
