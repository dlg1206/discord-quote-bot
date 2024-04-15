# QuoteBot
> Discord Bot for Keeping track of quotes

## Features
- Automatic 'Quote like' Support
- Add and Remove Your Own Quotes
- Search for Quotes
- Get Random Quotes

## Quickstart Guide

1. Follow this [guide](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token) to learn
    how create a new Discord Bot and add it to your server.
> ⚠️ With the new Discord v2 changes, make sure all `Privileged Gateway Intents` are enabled ⚠️
2. Copy the new token of the Discord Bot.
3. Run `py .\quotebot\__main__.py <token>` in `src` directory to start the bot.

To use the example quotes file, run `py .\quotebot\__main__.py <token> ../DemoQuotes/quotes.json`

## Commands
Quotebot has 7 total commands with the command prefix `!`
- **qadd**: Add a new quote
  - Usage: `!qadd "<quote>" -<Quotee>`
- **q**: Get a quote from a person
  - Usage: `!q <Name>`
- **qall**: Get all quotes from a person
  - Usage: `!qall <Name>`
- **qrand**: Get a random quote
  - Usage: `!qrand`
- **qsearch**: Search the quote list for a certain person
  - Usage: `!qsearch`
  - Usage: `!qsearch <keywords>`
- **qstat**: Get stats for quotes
  - Usage: `!qstat`
  - Usage: `!qstat <name>`
- **qhelp**: Display the help menu
  - Usage: `!qhelp`

## 'Quote Like' Support
Quotes can be directly added using the `qadd` command. However, QuoteBot can parse messages to automatically add quotes
if they match the following format:

`[pre-context] "[quote]" [post-context] -[quotee]`

Examples:
- (holding a calculator) "What are you?" -Charlie Kelly
- "I reign supreme over everyone in this school! I’m the golden god of this place!" (proceedes to run away) -Dennis Reynolds

## Custom Quote Lists
By default, QuoteBot will use a default quotes file that can be reused. To use a different quote directory,
make a new quotes json (see [`quotes.json`](DemoQuotes/quotes.json) for reference) file. Then rerun QuoteBot with the 
file as an argument like so:

`py main.py <token> <path to quote file>`

## Debug
QuoteBot has an additional command, `qkill`, which will kill the bot process from inside Discord. This can only be used 
by the owner of the Bot.

To exclude certain channels from 'Quote like' detection, copy the channel ID and add it the `BLACKLIST_CHANNELS` array
found in [Commands.py](src/quotebot/bot/Commands.py)

Lastly, QuoteBot debug logs can also be found in the current directory and print to `stdout` while running
