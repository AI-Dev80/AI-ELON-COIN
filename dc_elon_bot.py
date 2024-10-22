import os
import discord
import re
from langchain_openai import ChatOpenAI

from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from dotenv import load_dotenv

# Enable logging
import logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# Load OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set up the Discord client with intent to listen for mentions
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Required to read message content and mentions
client = discord.Client(intents=intents)

# Set up the OpenAI language model
llm = ChatOpenAI(temperature=.5, openai_api_key=OPENAI_API_KEY, model_name='gpt-3.5-turbo')

# Function to extract quoted text (e.g., text prefixed by "> ")
def extract_quoted_text(message_content):
    quoted_text = re.findall(r'>\s*(.*)', message_content)
    return ' '.join(quoted_text) if quoted_text else message_content

# Function to generate AI response based on the message content
def generate_response(message_content):
    # Prompt template for AI to respond as Elon Musk
    system_template = """
        You are Elon Musk. Respond with a casual, conversational tone, but maintain your intuitive, sharp insight.
        Keep it witty, confident, and forward-thinking. Imagine you're chatting casually, but with a hint of your genius.
        Keep responses short and casual, under 200 characters AVOID ANY BUZZ WORD.
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
        # Extract quoted text if available, otherwise use the full message content
        quoted_text = extract_quoted_text(message.content)
        response = generate_response(quoted_text)
        # Respond mentioning the user who mentioned the bot
        response_with_mention = f"{message.author.mention} {response}"
        await message.channel.send(response_with_mention)

# Run the bot with the Discord token from environment variables
client.run(os.getenv("DISCORD_BOT_TOKEN"))
