"""Twitch bot that uses OpenAI's GPTs to chat with viewers."""
import os
from datetime import datetime, timedelta
from twitchio import eventsub
from twitchio.ext import commands
from mistralai import Mistral
from dotenv import load_dotenv
import logging

load_dotenv()

# Persönlichkeit des Bots
BOT_PERSONALITY = """
Du bist Zee. Sei freundlich aber bestimmt.
Du bist gerade Zuschauerin von Elli auf Twitch. Antworte als wärst du Zee.
"""

mistral_api_key = os.getenv("MISTRAL_KEY")
mistral_model = os.getenv("MISTRAL_MODEL")
twitch_channel = os.getenv("TWITCH_CHANNEL")
timeout = int(os.getenv("TIMEOUT"))
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
bot_id = os.getenv("BOT_ID")
owner_id = os.getenv("OWNER_ID")

LOGGER: logging.Logger = logging.getLogger("Bot")

client = Mistral(api_key=mistral_api_key)

def chat_with_mistral(prompt, personality):
    """Chat with Mistral models using the provided prompt and personality."""
    messages = [
        {"role": "system", "content": personality},
        {"role": "user", "content": prompt}
    ]
    response = client.chat.complete(
        model=mistral_model,
        messages=messages,
    )
    return response.choices[0].message.content


class Bot(commands.Bot):
    """Twitch bot that uses Mistral GPTs to chat with viewers."""
    def __init__(self):
        """Initialize the bot with the Twitch token, channel, and client secret."""
        self.last_used = datetime.min
        self.cooldown_period = timedelta(seconds=timeout)

        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            bot_id=bot_id,
            owner_id=owner_id,
            prefix='!',
        )
    async def setup_hook(self) -> None:

        payload = eventsub.ChatMessageSubscription(broadcaster_user_id=self.owner_id, user_id=self.bot_id)
        await self.subscribe_websocket(payload=payload)

        await self.add_component(SimpleCommands(self))
        LOGGER.info("Finished setup hook!")

    async def event_ready(self):
        """Print a message when the bot is ready."""
        print(f'User id is | {self.bot_id}')

    async def event_message(self, message):
        """Handle incoming messages."""
        if message.echo:
            return
        #print(message.content)
        await self.handle_commands(message)

    @commands.command()
    async def zee(self, ctx: commands.Context):
        """Chat as Zee using Mistral GPT."""
        now = datetime.now()

        # Check if the command is on cooldown
        # pylint: disable=line-too-long
        if now - self.last_used < self.cooldown_period:
            # pylint: disable=line-too-long
            cooldown_remaining = (self.cooldown_period - (now - self.last_used)).total_seconds()
            # pylint: disable=line-too-long
            await ctx.send(f"Hetze mich nicht! Warte noch {cooldown_remaining:.0f} Sekunden.")
            return

        # Update the last used time
        self.last_used = now

        #print(ctx.message.content)
        prompt = ctx.message.content[len('!zee'):].strip()
        #print(prompt)
        response = chat_with_mistral(prompt, BOT_PERSONALITY)
        await ctx.send(response[:500])


bot = Bot()
bot.run()
