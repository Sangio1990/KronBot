import nextcord
from commands.slash_commands import slash_command_list
from command_manager.command_manager import CommandManager
from nextcord.ext import commands
from tokenfile import tokenID

intents = nextcord.Intents.all()
client = commands.Bot(intents=intents)
command_manager = CommandManager(client)


@client.event
async def on_ready():
    print("Logged in as:", client.user)


slash_command_list(client)


@client.event
async def on_message(message):
    if message.author == client.user:
        pass
    else:
        # this must be deleted and an observer done, is just for testing purpose:
        if message.content.lower().startswith("!kr "):
            await command_manager.manage_command(message)


client.run(tokenID)
