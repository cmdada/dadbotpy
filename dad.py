import discord
from discord import app_commands
import requests

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name="dadjoke", description="random dadjoke") 
async def first_command(interaction):
    joke = get_dad_joke()
    await interaction.response.send_message(joke)

def get_dad_joke():
    response = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
    joke = response.json()["joke"]
    return joke

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1175224722598936656))
    print("Ready!")

client.run("wow you really think im going to put the token in a PUBLIC git repo")
