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

@tree.command(name="invite", description="generate a one-time invite to the server")
async def second_command(interaction):
    guild = client.get_guild(interaction.guild_id)
    invite = await guild.text_channels[0].create_invite(max_uses=1)
    await interaction.response.send_message(f"Here's a one-time invite to the server: {invite.url}")

def get_dad_joke():
    response = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
    joke = response.json()["joke"]
    return joke

@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")

client.run("your token (crazy)")
