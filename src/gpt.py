import openai
import discord
import os
from dotenv import load_dotenv

# Load the values from the .env file
load_dotenv()

# Set the Discord token and OpenAI API key]
DISCORD_TOKEN = os.environ["TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Initialize the Discord and OpenAI clients
client = discord.Client()
openai.api_key = OPENAI_API_KEY

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return
    print(message.content)
    # Generate a response using GPT-3
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=message.content,
        max_tokens=1024,
        n=1,
        temperature=0.5
    )
    # Check if the response contains a valid text value
    text = response["choices"][0]["text"]
    if text:
        # Send the response to the user in the Discord channel
        await message.channel.send(text)
    else:
        # Send a default message if the response is empty
        await message.channel.send("I'm sorry, I cannot generate a response for this prompt.")


client.run(DISCORD_TOKEN)

# things to add
# maybe add a specific command for code blocks
# (Need to fix) THe bot is replying to every message with some random stuff