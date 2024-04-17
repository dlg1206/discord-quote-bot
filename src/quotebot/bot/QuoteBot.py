"""
File: QuoteBot.py
Description: Collection of Commands for the Discord Bot

@author Derek Garcia
"""
import re

import discord
from discord.ext import commands

from db.Database import Database
from log.Logger import Logger, Status
from quote.Quote import format_quotee, is_quote, parse_quote

VERSION = "2.5"
SOURCE_CODE = "github.com/dlg1206/Discord-Quote-Bot"
COMMANDS_REGEX = re.compile("!qadd|!q|!qall|!qrand|!qsearch|!qstat|!qhelp|!qkill")  # list of commands


class QuoteBot(commands.Bot):

    def __init__(self, database: Database, blacklist_channels: str = None):
        """
        Create new Quote Bot

        :param database: Quote database to use
        :param blacklist_channels: optional string list of black listed channels to ignore for 'quote-like' add
        """
        super().__init__(command_prefix="!", intents=discord.Intents.all())
        self.database = database
        self.logger = Logger(database)
        self.version = VERSION
        self.source_code = SOURCE_CODE
        self.blacklist_channels = {} if blacklist_channels is None else set(blacklist_channels.split(","))

        # Init custom commands
        self.init_commands()

    def init_commands(self) -> None:
        """
        Register custom commands to the bot
        """

        @self.command()
        async def qadd(ctx, *, prompt=None) -> None:
            """
            Adds quote to quote dictionary and txt file

            :param ctx: command prefix
            :param prompt: Entire quote/author
            """
            # Check if prompt was given
            if prompt is None:
                await ctx.channel.send('Proper Usage: `!qadd "[quote]" -[Quotee]`')
                self.logger.log(str(ctx.message.author), "!qadd", Status.ERROR, "No args")
                return

            # Check if quote
            if not is_quote(prompt):
                await ctx.channel.send('Sorry, I didn\'t get that :(\nCommand: `!qadd "[quote]" -[Quotee]`')
                self.logger.log(str(ctx.message.author), "!qadd", Status.ERROR, f"Failed to parse: {prompt}")
                return

            # Upload to db
            code = self.database.add_quote(parse_quote(prompt), str(str(ctx.message.author)))

            # Confirmation
            if code > 0:
                await ctx.channel.send("Quote added! :)")
                self.logger.log(str(ctx.message.author), "!qadd", Status.SUCCESS, code)
            else:
                # error
                self.logger.log(str(ctx.message.author), "!qadd", Status.ERROR, f"Failed to upload: {prompt}")

            await self.change_presence(
                activity=discord.Game(f"{self.database.get_quote_total()} quotes and counting!"))

        @self.command()
        async def q(ctx, *, quotee=None) -> None:
            """
            Get a random quote from given name

            :param ctx: command
            :param quotee: name to search quotes for
            """

            # check if quotee was given
            if quotee is None:
                await ctx.channel.send("Proper Usage: `!q [Name]`")
                self.logger.log(str(ctx.message.author), "!q", Status.ERROR, "No args")
                return

            # Print random quote if one exits
            rand_quote = self.database.get_rand_quote(quotee)
            if rand_quote is not None:
                await ctx.channel.send(rand_quote)
                self.logger.log(str(ctx.message.author), "!q", Status.SUCCESS)
                return

            # If name not in QUOTES, print not found
            self.logger.log(str(ctx.message.author), "!q", Status.WARN, f"No quotes found for {quotee}")
            await self.list_similar(ctx, quotee)

        @self.command()
        async def qall(ctx, *, quotee=None) -> None:
            """
            Get all the quotes for a specific person

            :param ctx: command
            :param quotee: name to search quotes for
            """

            # Invalid usage
            if quotee is None:
                await ctx.channel.send("Proper Usage: `!qall [Name]`")
                self.logger.log(str(ctx.message.author), "!qall", Status.ERROR, "No args")
                return

            # Search for quotes
            quotes = self.database.get_all_quotes(quotee)

            # If no quotes, check for similar
            if len(quotes) == 0:
                self.logger.log(str(ctx.message.author), "!qall", Status.WARN, f"No quotes found for {quotee}")
                await self.list_similar(ctx, quotee)
                return

            # Format and display all quotes
            only_quotes = [f'> - "{q.quote}"' for q in quotes]
            self.logger.log(str(ctx.message.author), "!qall", Status.SUCCESS, f"Found {len(quotes)} for {quotee}")
            await ctx.channel.send(f"{'\n'.join(only_quotes)}\n"
                                   f"**{format_quotee(quotee)} has {len(quotes)} quotes!**")

        @self.command()
        async def qrand(ctx) -> None:
            """
            Get random quote from entire quote dictionary

            :param ctx: Command
            """
            rand_quote = self.database.get_rand_quote()
            await ctx.channel.send(rand_quote)
            self.logger.log(str(ctx.message.author), "!qrand", Status.SUCCESS)

        @self.command()
        async def qsearch(ctx, *, keywords=None) -> None:
            """
            Searches database for people's names. Either lists all or ones that match the keywords

            :param ctx: command
            :param keywords: optional keywords to look for
            """
            # Get all quotees if no keywords
            if keywords is None:
                all_quotees = [f"> {format_quotee(q)}" for q in self.database.get_all_quotees()]
                await ctx.channel.send(f"**I have quotes from all these people!**\n{'\n'.join(all_quotees)}")
                self.logger.log(str(ctx.message.author), "!qsearch", Status.SUCCESS,
                                f"Found {len(all_quotees)} quotees")
            # Search for quotees that match the keywords
            else:
                similar = [format_quotee(q) for q in self.database.find_similar_quotee(keywords)]
                if len(similar) != 0:
                    await ctx.channel.send(f"Here's what I could find:\n{'\n'.join(similar)}")
                    self.logger.log(str(ctx.message.author), "!qsearch [keywords]", Status.SUCCESS,
                                    f"keywords={keywords}")

        @self.command()
        async def qstat(ctx, *, quotee=None) -> None:
            """
            Gets Stats of QuoteBoi or user

            :param ctx: Command
            :param quotee: optional quotee field
            """
            # Get total number of quotes and quotees if no quotee
            if quotee is None:
                await ctx.channel.send(
                    f"I have {self.database.get_quote_total()} quotes from {self.database.get_quotee_total()} people!")
                self.logger.log(str(ctx.message.author), "!qstat", Status.SUCCESS)
                return

            # Check for quotes from given quotee
            num_quotes = self.database.get_quote_total(quotee)
            if num_quotes != 0:
                await ctx.channel.send(f"{format_quotee(quotee)} has {num_quotes} quotes!")
                self.logger.log(str(ctx.message.author), "!qstat [quotee]", Status.SUCCESS, quotee)

            # If none found, list similar
            else:
                # Print not found
                self.logger.log(str(ctx.message.author), "!qstat", Status.WARN, f"No quotes from {quotee}")
                await self.list_similar(ctx, quotee)

        @self.command()
        async def qhelp(ctx) -> None:
            """
            Prints command arguments

            :param ctx: Command
            """
            await ctx.channel.send(f"__**QuoteBoi Version: {self.version}**__\n" +
                                   f"Source Code: {self.source_code}\n" +
                                   "> - Add quote: `!qadd \"quote\" -Quotee`\n" +
                                   "> - Get Quote: `!q Name`\n" +
                                   "> - Get All quotes: `!qall Name`\n" +
                                   "> - Random Quote: `!qrand`\n" +
                                   "> - All People list: `!qsearch`\n" +
                                   "> - Keyword Search: `!qsearch keyword`\n" +
                                   "> - Total Quote Stats: `!qstat`\n" +
                                   "> - Person Quote Stats: `!qstat Name`\n" +
                                   "> - Help: `!qhelp`")
            await ctx.channel.send("**'Quote Like' Support**\n" +
                                   "> QuoteBoi will detect 'Quote Like' messages in *roughly* the following format:\n" +
                                   "> `(pre-context) \"quote\" (post-context) -quotee`\n" +
                                   "> There's no guarantee, but it's good at detecting them. `!qadd` is the only way\n" +
                                   "> to add quotes for sure")
            self.logger.log(str(ctx.message.author), "!qhelp", Status.SUCCESS)

        @self.command()
        @commands.is_owner()
        async def qkill(ctx) -> None:
            """
            Master kill switch from inside discord

            :param ctx: command
            """
            quote = self.database.get_rand_quote()
            await ctx.channel.send(f'Goodbye, and in the words of {format_quotee(quote.quotee)}: "{quote}"')
            self.logger.log(str(ctx.message.author), "!qkill", Status.SUCCESS)
            exit(0)

    async def list_similar(self, ctx: discord.channel, quotee: str, prompt: str = "Did you mean anyone here?") -> None:
        """
        List quotees that are a partial match to the given quotee

        :param ctx: command
        :param quotee: Quotee to attempt to match
        :param prompt: Prompt message to pair list with
        """
        # Print not found
        await ctx.channel.send("I don't have any quotes from " + f"{format_quotee(quotee)}" + " :(")

        # print similar if any, bold matches
        similar = [f"> - {format_quotee(q.lower().replace(quotee.lower(), f"**{quotee}**"))}"
                   for q in self.database.find_similar_quotee(quotee)]
        if len(similar) != 0:
            await ctx.channel.send(f"{prompt}\n{'\n'.join(similar)}\n")
            self.logger.log(str(ctx.message.author), "list_similar", Status.SUCCESS, f"{quotee} matches {len(similar)}")
        # Else just log none found
        else:
            self.logger.log(str(ctx.message.author), "list_similar", Status.WARN, f"Nothing similar to {quotee}")

    async def on_message(self, message) -> None:
        """
        Parses message and determines if it is 'quote like' and attempts to add it

        :param message: message to parse
        """

        # exe any commands first
        await self.process_commands(message)

        # ignore any commands or messages from self
        if bool(re.search(COMMANDS_REGEX, message.content.strip())) or message.author.bot:
            return

        # "quote-like" add, not explicit command and in a valid channel
        if is_quote(message.content) and message.channel.id not in self.blacklist_channels:
            qid = self.database.add_quote(parse_quote(message.content), str(message.author))
            self.logger.log(str(message.author), "quote-like add", Status.SUCCESS, f"{qid} | {message.content}")
            await self.change_presence(activity=discord.Game(f"{self.database.get_quote_total()} quotes and counting!"))

    async def on_ready(self) -> None:
        """
        Tells console that bot is active and basic info

        :return:
        """
        self.logger.log("admin", "start", Status.INFO, "Starting bot. . .")
        await self.change_presence(status=discord.Status.online,
                                   activity=discord.Game(f"{self.database.get_quote_total()} quotes and counting!"))

        self.logger.log("admin", "start", Status.INFO, '{0.user}'.format(self) + " is online")
        self.logger.log("admin", "start", Status.SUCCESS, f"database: {self.database.db_location}")
