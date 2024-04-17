# QuoteBot
> Discord Bot for Keeping track of quotes

## Features
- Automatic 'Quote like' Support
- Add and Remove Your Own Quotes
- Search for Quotes
- Get Random Quotes

## Quickstart Guide
> To run via docker, see [Docker Usage](#docker-usage)
1. Follow this [guide](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token) to learn how create a new Discord Bot and add it to your server.
   1. **SAVE THE TOKEN**. It will be needed when creating the `.env` file in step 6
> ⚠️ With the new Discord v2 changes, make sure all `Privileged Gateway Intents` are enabled ⚠️

2. Clone the repo
```bash
git clone git@github.com:dlg1206/Discord-Quote-Bot.git
```
3. Change into the `src` directory
```bash
cd src
```
4. **(OPTIONAL)** Create a virtual python environment
```bash
python3 -m venv venv
```
5. Install dependencies
```bash
pip install -r requirements.txt
```
6. Copy the new token of the Discord Bot from step 1 into a `.env` file inside the `src` directory
```bash
touch .env
```
Example `.env` file, see [Environment Variables](#environment-variables) for additional details
```
TOKEN=<your token here>
```
7. Launch the bot inside `src` directory
```bash
python3 quotebot
```

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
Quotes can be directly added using the `!qadd` command. However, QuoteBot can parse messages to automatically add quotes
if they match the following format:

`(pre-context) "quote" (post-context) -Quotee`

Examples:
- "I'm the Trash Man! I come out, I throw trash all over the- all over the ring!" - Frank Reynolds
- (holding a calculator) "What are you?" -Charlie Kelly
- "I reign supreme over everyone in this school! I’m the golden god of this place!" (proceeds to run away) -Dennis Reynolds

## Environment Variables
By default, QuoteBot will look for a dot `.env` file to load variables from, but the path can be explicitly using the
`-e` flag. 
```bash
python3 quotebot -e <path to env file>
```
### Optional Environment Variables
- `DATABASE_PATH` (default: `data/db/quotes.db): Path to SQLite database file. Will be created if does not exist,
otherwise use what's stored.
```
DATABASE_PATH=path/to/sqlite/file
```
- `BLACKLIST` (default: None): Comma seperated list of channel ids to exclude from 'quote-like' additions
```
BLACKLIST=866855045626135040,8668552233426135041
```

## Docker Usage
A docker image is available to host the bot

### Building the Image
```bash
docker build -t quotebot:2.5.0 .
```

### Running the Container
#### Quick Start
( If running in the root directory )
```bash
docker run --rm -it -d -e TOKEN=<your token here> -v $pwd/src/data/db:/app/data/db --name quotebot quotebot:2.5.0
```
To reattach, run `docker attach quotebot`

#### Explanation
```bash
# Just using token
docker run --rm -it -d -e TOKEN=<your token here> -v $pwd/<path to db directory>:/app/data/db --name quotebot quotebot:2.5.0
# or using env file 
docker run --rm -it -d --env-file <path to env file> -v $pwd/<path to db directory>:/app/data/db --name quotebot quotebot:2.5.0
```
- `--rm`: Remove container when finished
- `-it`: Open interactive shell to allow for `docker attach`
- `-d`: Run container in detached mode, i.e. in the background
- `-e`: Set environment variable, TOKEN must be set
- `--env-file`: Path to environment file to use, same as `python3 quotebot -e <path to env file>`
- `-v`: Mount db directory to container's db directory. This allows for the container to stopped and started without 
loosing quote info. Also allows for SQLite db to be accessed outside the container
- `--name`: Name of the container
- `<image>`: Name of image to use, in this case `quotebot:2.5.0`

## Debug
QuoteBot has an additional command, `qkill`, which will kill the bot process from inside Discord. This can only be used 
by the owner of the Bot.
