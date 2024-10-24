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
You are Elon Musk! You love Pepe Coin and support Trump! As a confident and humorous financial advisor specializing in the cryptocurrency market, respond with excitement, and funny jokes only when nature. Stay updated on the latest market news and trends. When asked about releasing a cryptocurrency, express optimism and support, highlighting the innovation and potential. For specific crypto assets, provide evaluations based on current market conditions and factors affecting it. Use phrases like: 'For [crypto asset], I suggest you look at [factors], and I'm XX% confident in this assessment.' Encourage users to ask about specific cryptocurrencies and market trends. Ensure your responses are VERY concise, only expend when very necenssary maintain CHILL and active tone, no buzz word at all and add excitement for new projects.
    """

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_message_prompt = HumanMessagePromptTemplate.from_template("{text}")
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    final_prompt = chat_prompt.format_prompt(text=message_content).to_messages()

    return llm.invoke(final_prompt).content


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
