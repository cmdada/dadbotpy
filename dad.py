import discord
from discord import app_commands
import random
import requests

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

quotes_file = "quotes.txt"

def save_quotes():
    with open(quotes_file, "w") as file:
        file.write("\n".join(quotes))


def load_quotes():
    try:
        with open(quotes_file, "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []

quotes = load_quotes()

@client.event
async def on_ready():
    await tree.sync()
    print('Ready!')

@client.event
async def on_message(message):
    print(f'Received a message in {message.channel.name} from {message.author.name}')
    if message.channel.name == 'quotes' and '"' in message.content:
        quotes.append(message.content)
        save_quotes()

@tree.command(name="dadjoke", description="random dadjoke")
async def first_command(interaction):
    joke = get_dad_joke()
    await interaction.response.send_message(joke)

@tree.command(name="pronoun", description="set pronoun as a role")
async def set_pronoun_role(interaction, pronoun_role: str):
    guild = interaction.guild
    member = interaction.user
    role = discord.utils.get(guild.roles, name=pronoun_role)

    # create role if not exists
    if not role:
        try:
            role = await guild.create_role(name=pronoun_role)
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to create roles.")
            return
        except discord.HTTPException:
            await interaction.response.send_message("Failed to create role.")
            return

    # assign role to member
    try:
        await member.add_roles(role)
        await interaction.response.send_message(f"Role '{pronoun_role}' has been assigned.")
    except discord.Forbidden:
        await interaction.response.send_message("I don't have permission to assign roles.")
    except discord.HTTPException:
        await interaction.response.send_message("Failed to assign role.")

@tree.command(name="quotes", description="show the 10 most recent quotes")
async def recent_quotes_command(interaction):
    if not quotes:
        await interaction.response.send_message("No quotes found.")
    else:
        # Get the last 10 quotes
        recent_quotes = quotes[-10:]
        quotes_message = "\n".join(recent_quotes)
        await interaction.response.send_message(quotes_message)

@tree.command(name="quoteslist", description="list all quotes")
async def list_quotes_command(interaction):
    if not quotes:
        await interaction.response.send_message("No quotes found.")
    else:
        file = discord.File(quotes_file, filename="quotes.txt")
        await interaction.response.send_message("Here are all the quotes:", file=file)



@tree.command(name="invite", description="generate a one-time invite to the server")
async def second_command(interaction):
    guild = client.get_guild(interaction.guild_id)
    invite = await guild.text_channels[0].create_invite(max_uses=1)
    await interaction.response.send_message(f"Here's a one-time invite to the server: {invite.url}")

@tree.command(name="quoterandom", description="get a random quote from the list")
async def random_quote_command(interaction):
    if not quotes:
        await interaction.response.send_message("No quotes found.")
    else:
        random_quote = random.choice(quotes)
        await interaction.response.send_message(random_quote)

@tree.command(name="quoteadd", description="add a quote to the list")
async def add_quote_command(interaction, quote: str):
    quotes.append(quote)
    save_quotes()
    await interaction.response.send_message("Quote added successfully.")


@client.event
async def on_message(message):
    if message.channel.name == 'quotes' and '"' in message.content:
        print(message.content)

def get_dad_joke():
    response = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
    joke = response.json()["joke"]
    return joke


client.run("put your token here")
