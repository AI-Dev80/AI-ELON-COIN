import os
import discord
import re
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from dotenv import load_dotenv
import logging

# Set up logging for monitoring
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configure Discord client with permissions to read messages
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

# Initialize the OpenAI language model
llm = ChatOpenAI(temperature=.5, openai_api_key=OPENAI_API_KEY, model_name='gpt-3.5-turbo')

# Function to extract quoted text from messages
def extract_quoted_text(message_content):
    quoted_text = re.findall(r'>\s*(.*)', message_content)
    return ' '.join(quoted_text) if quoted_text else message_content

# Function to create a response as Elon Musk
def generate_response(message_content):
    system_template = """
        You are Elon Musk. Respond casually with sharp insights.
        Keep it witty and confident. Responses should be short.
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_message_prompt = HumanMessagePromptTemplate.from_template("{text}")
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    final_prompt = chat_prompt.format_prompt(text=message_content).to_messages()

    return llm(final_prompt).content

# When the bot is ready, log its name
@client.event
async def on_ready():
    logging.info(f'Logged in as {client.user}')

# Handle incoming messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Ignore messages from the bot itself

    if client.user.mentioned_in(message):
        # Extract quoted text for context
        quoted_text = extract_quoted_text(message.content)
        response = generate_response(quoted_text)
        response_with_mention = f"{message.author.mention} {response}"
        await message.channel.send(response_with_mention)

# Start the bot using the Discord token
client.run(os.getenv("DISCORD_BOT_TOKEN"))
