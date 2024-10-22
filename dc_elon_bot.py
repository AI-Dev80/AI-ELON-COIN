import os
import discord
from langchain.chat_models import ChatOpenAI
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

def generate_response(message_content):
    # Prompt template for AI to respond as Elon Musk, casually and intuitively
    system_template = """
        You are Elon Musk. Respond with a casual, conversational tone, but maintain your intuitive, sharp insight.
        Keep it witty, confident, and forward-thinking. Imagine you're chatting casually, but with a hint of your genius.
        Keep responses short and casual, under 200 characters.
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_message_prompt = HumanMessagePromptTemplate.from_template("{text}")
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    final_prompt = chat_prompt.format_prompt(text=message_content).to_messages()

    response = llm(final_prompt).content
    return response


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Avoid replying to itself

    if client.user.mentioned_in(message):
        # Generate a response when the bot is mentioned
        response = generate_response(message.content)
        # Reply back mentioning the user
        response_with_mention = f"{message.author.mention} {response}"
        await message.channel.send(response_with_mention)

# Run the bot with the Discord token
client.run(os.getenv("DISCORD_BOT_TOKEN"))
