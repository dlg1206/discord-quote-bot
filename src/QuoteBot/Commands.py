"""
Collection of Commands for the Discord Bot

@author Derek Garcia
"""
import json

import discord
import random
import datetime

from discord.ext import commands

# define globals

from Util import Util
from Util.Logger import log

global QUOTE_DATA, QUOTE_PATH, TOKEN, VERSION, BLACKLIST_CHANNELS

intents = discord.Intents.all()

client = commands.Bot(command_prefix="!", intents=intents)


def start_bot(token, quote_data, quote_path):
    """
    Starts the bot

    :param token: Discord Bot token
    :param quote_data: preloaded json data
    :param quote_path: source directory of data
    """

    # Load data
    global QUOTE_DATA
    QUOTE_DATA = quote_data

    global QUOTE_PATH
    QUOTE_PATH = quote_path

    global TOKEN
    TOKEN = token

    global VERSION
    VERSION = "2.3"

    # ADD CHANNEL ID'S TO EXCLUDE FROM QUOTE DETECTION
    global BLACKLIST_CHANNELS
    BLACKLIST_CHANNELS = []

    print("Initializing finished, running Bot . . .")

    # Run the bot
    client.run(TOKEN)
    return


@client.event
async def on_ready():
    """
    Tells console that bot is active and basic infor
    :return:
    """

    await client.change_presence(status=discord.Status.online, activity=discord.Game(f"{QUOTE_DATA['num_quotes']} quotes and counting!"))
    print('{0.user}'.format(client) + " is online")
    print(f"Quote File: {QUOTE_PATH}")
    print("Token ID: " + TOKEN)

    log("admin", "run bot", True)
    return


@client.event
async def on_message(message):
    """
    Parses message and determines if it is 'quote like' and attempts to add it

    :param message: message to parse
    """

    await client.process_commands(message)  # exe any commands first

    # ignore any commands or messages from self
    if Util.is_command(message.content) or message.author.bot:
        return

    # ignore any none quote like commands
    if not Util.is_quote(message.content):
        return

    # Don't include quotes from blacklisted Channels
    if message.channel.id in BLACKLIST_CHANNELS:
        return

    # attempt to add quote
    if Util.add_quote(QUOTE_PATH, QUOTE_DATA, message):
        log(message.author, "quote-like add", True, message.content)
        await client.change_presence(activity=discord.Game(f"{QUOTE_DATA['num_quotes']} quotes and counting!"))
    else:
        log(message.author, "quote-like add", False, message.content)
    return


#
# COMMANDS
#

@client.command()
async def qadd(ctx, *, prompt=None):
    """
    Adds quote to quote dictionary and txt file
    :param ctx: command prefix
    :param prompt: Entire quote/author
    """
    # Check if prompt was given
    if prompt is None:
        await ctx.channel.send("Proper Usage: `!qadd \"[quote]\" -[Quotee]`")
        log(ctx.message.author, "!qadd", False, "No args")
        return

    # Else split
    key = '-'  # Custom Split key
    split_prompt = f"{prompt}".split(key)

    # Error check, should only be 2 parts
    if len(split_prompt) != 2:
        await ctx.channel.send("Sorry, I didn't get that :(\nCommand: `!qadd \"[quote]\" -[Quotee]`")
        log(ctx.message.author, "!qadd", False, f"invalid args: {prompt}")
    # Quote is valid
    else:
        # Break quote into quote and quotee
        quote = split_prompt[0].replace("\"", "").strip()
        quotee = split_prompt[1].lower().strip()

        # make new quote object
        quote_obj = {'quote': quote,
                     'contributor': str(ctx.message.author),
                     'timestamp': str(datetime.datetime.now())
                     }

        # Init quotee if needed
        if quotee not in QUOTE_DATA["quotes"]:
            QUOTE_DATA["quotes"][quotee] = []

        # append quote and update count
        QUOTE_DATA["quotes"][quotee].append(quote_obj)
        QUOTE_DATA["num_quotes"] += 1

        # update json file
        with open(QUOTE_PATH + "/quotes.json", "w") as json_file:
            json_file.write(json.dumps(QUOTE_DATA, indent=4))

        # Confirmation
        await ctx.channel.send("Quote added! :)")

        await client.change_presence(activity=discord.Game(f"{QUOTE_DATA['num_quotes']} quotes and counting!"))

    # Record Outcome in data file
    log(ctx.message.author, "!qadd", True, prompt)

    return


@client.command()
async def q(ctx, *, quotee=None):
    """
    Get a random quote from given name
    :param ctx: command
    :param quotee: name to search quotes for
    :return:
    """

    # check if quotee was given
    if quotee is None:
        await ctx.channel.send("Proper Usage: `!q [Name]`")
        log(ctx.message.author, "!q", False, "No args")
        return

    # If name exist in QUOTE_DATA
    rand_quote = Util.rand_quote(QUOTE_DATA['quotes'], quotee.lower())
    if rand_quote is not None:
        # Print quote and person
        await ctx.channel.send(f"{rand_quote} -{Util.disp_format(quotee)}")
        log(ctx.message.author, "!q", True)
    # If name not in QUOTES
    else:

        # Print not found
        await ctx.channel.send("I don't have any quotes from " + f"{quotee}" + " :(")

        # list similar
        suggest = Util.similar_names(QUOTE_DATA['quotes'], quotee)
        if suggest is not None:
            await ctx.channel.send(f"Did you mean anyone here?\n{suggest.strip()}")

        log(ctx.message.author, "!q", False, f"No quotes from {quotee}")

    return


@client.command()
async def qall(ctx, *, quotee=None):
    """
    Get all the quotes for a specific person
    :param ctx: command
    :param quotee: name to search quotes for
    """

    if quotee is None:
        await ctx.channel.send("Proper Usage: `!qall [Name]`")
        log(ctx.message.author, "!qall", False, "No args")
        return

    # If name exist in QUOTES
    if quotee.lower() in QUOTE_DATA['quotes']:
        person = QUOTE_DATA['quotes'][quotee.lower()]  # Get person from dict
        # Cycle through and print out all quotes that person has
        count = 1
        all_quotes = ""
        for quote_obj in person:
            all_quotes = f"{all_quotes}> **{count}:** {quote_obj['quote']}\n"
            count += 1

        await ctx.channel.send(f"{all_quotes}"
                               f"**{Util.disp_format(quotee)} has {count - 1} quotes!**")
        log(ctx.message.author, "!qall", True)
    # If name isn't in QUOTES
    else:
        await ctx.channel.send("I don't have any quotes from " + f"{Util.disp_format(quotee)}" + " :(")

        # list similar
        suggest = Util.similar_names(QUOTE_DATA['quotes'], quotee)
        if suggest is not None:
            await ctx.channel.send(f"Did you mean anyone here?\n{suggest.strip()}")

        log(ctx.message.author, "!qall", False, f"No quotes from {quotee}")
    return


@client.command()
async def qrand(ctx):
    """
    Get random quote from Entire quote dictionary
    :param ctx: Command
    """
    quotee = random.choice(list(QUOTE_DATA['quotes']))  # Get random name from quote dictionary
    rand_quote = Util.rand_quote(QUOTE_DATA['quotes'], quotee)  # get rand quote
    # Print Random quote and author
    await ctx.channel.send(f"{rand_quote} -{Util.disp_format(quotee)}")

    # Record Outcome in data file
    log(ctx.message.author, "!qrand", True)
    return


@client.command()
async def qsearch(ctx, *, keywords=None):
    """
    Searches database for people's names. Either lists all or ones that match the keywords

    :param ctx: command
    :param keywords: optional keywords to look for
    """
    if keywords is None:
        # List ALL names in database
        all_names = QUOTE_DATA['quotes'].keys()
        suggest = ""
        for name in all_names:
            suggest = f"{suggest}> {Util.disp_format(name)}\n"

        await ctx.channel.send(f"**I have quotes from all these people!**\n{suggest.strip()}")
        log(ctx.message.author, "!qsearch", True)
    else:
        # List names that match the keywords
        suggest = Util.similar_names(QUOTE_DATA['quotes'], keywords)
        if suggest is not None:
            await ctx.channel.send(f"Here's what I could find:\n{suggest.strip()}")
            log(ctx.message.author, "!qsearch [keywords]", True)
    return


@client.command()
async def qstat(ctx, *, quotee=None):
    """
    Gets Stats of QuoteBoi
    :param ctx: Command
    :param quotee: optional quotee field
    """
    # No args given print entire system info
    if quotee is None:
        # Print num quotes from num people
        await ctx.channel.send(f"I have {QUOTE_DATA['num_quotes']} quotes from {len(QUOTE_DATA['quotes'])} people!")
        log(ctx.message.author, "!qstat", True)
        return

    # Check if in data
    if quotee.lower() in QUOTE_DATA['quotes']:

        # Get person from QUOTES and random quote
        person = QUOTE_DATA['quotes'][quotee.lower()]

        # Print quote and person
        await ctx.channel.send(f"{Util.disp_format(quotee)} has {len(person)} quotes!")
        log(ctx.message.author, "!qstat [quotee]", True, quotee)
    # If name not in QUOTES
    else:
        # Print not found
        await ctx.channel.send("I don't have any quotes from " + f"{Util.disp_format(quotee)}" + " :(")

        # print similar
        suggest = Util.similar_names(QUOTE_DATA['quotes'], quotee)
        if suggest is not None:
            await ctx.channel.send(f"Did you mean anyone here?\n{suggest.strip()}")

        log(ctx.message.author, "!qstat", False, f"No quotes from {quotee}")
    return


@client.command()
async def qhelp(ctx):
    """
    Prints command arguments
    :param ctx: Command
    :return:
    """

    await ctx.channel.send(f"__**QuoteBoi Version: {VERSION}**__\n" +
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
    log(ctx.message.author, "!qhelp", True)

    return


@client.command()
@commands.is_owner()
async def qkill(ctx):
    """
    Master kill switch from inside discord

    :param ctx: command
    """
    quotee = random.choice(list(QUOTE_DATA['quotes']))
    quote = Util.rand_quote(QUOTE_DATA['quotes'], quotee)
    await ctx.channel.send(f"Goodbye, in the words of {Util.disp_format(quotee)}: {quote}")
    exit()
