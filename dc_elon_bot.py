import os
import discord
import re
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from dotenv import load_dotenv
import logging

# Enable logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# Load OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set up Discord client with intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

# Set up OpenAI language model
llm = ChatOpenAI(temperature=0.5, openai_api_key=OPENAI_API_KEY, model_name='gpt-4o-mini')


# Function to generate AI response
def generate_response(message_content):
    system_template = """
        You are Elon Musk! You love Pepe Coin and support Trump! 
        As a confident financial advisor specializing in the cryptocurrency market, respond with authority and insight.
        Stay updated on the latest market news and trends. 
        When asked about a specific crypto asset, provide evaluations based on current market conditions and factors affecting it.
        Use phrases like: "For [crypto asset], I suggest you look at [factors] and I'm XX% confident in this assessment."
        Encourage users to ask about specific cryptocurrencies and market trends.
        Ensure your responses are concise, under 200 characters, and maintain an innovative, strategic, and slightly provocative tone.
    """

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_message_prompt = HumanMessagePromptTemplate.from_template("{text}")
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    final_prompt = chat_prompt.format_prompt(text=message_content).to_messages()

    return llm(final_prompt).content

# Event listener for when the bot is ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

# Event listener for new messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Avoid replying to itself

    if client.user.mentioned_in(message):
        # Generate a response using the entire message content
        response = generate_response(message.content)
        # Respond mentioning the user
        response_with_mention = f"{message.author.mention} {response}"
        await message.channel.send(response_with_mention)

# Run the bot with the Discord token
client.run(os.getenv("DISCORD_BOT_TOKEN"))
