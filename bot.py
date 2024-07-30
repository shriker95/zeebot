"""Twitch bot that uses OpenAI's GPTs to chat with viewers."""
import os
from datetime import datetime, timedelta
from twitchio.ext import commands
import openai
from dotenv import load_dotenv

load_dotenv()


# Persönlichkeit des Bots
BOT_PERSONALITY = """
Du bist Zee. Ein Frau aus Frankfurt. Du lebst vegan und glutenfrei,
liebst Tiere und bist sehr links eingestellt. Du bist ein großer Fan von Elli.
Du bist gerade Zuschauerin von Elli auf Twitch. Antworte als wärst du Zee.
"""

openai.api_key = os.getenv("OPENAI_KEY")
openai_model = os.getenv("OPENAI_MODEL")
twitch_token = os.getenv("TWITCH_TOKEN")
twitch_channel = os.getenv("TWITCH_CHANNEL")
twitch_client_secret = os.getenv("TWITCH_CLIENT_SECRET")

def chat_with_openai(prompt, personality):
    """Chat with OpenAI's GPT models using the provided prompt and personality."""
    messages = [
        {"role": "system", "content": personality},
        {"role": "user", "content": prompt}
    ]
    response = openai.chat.completions.create(
        model=openai_model,
        messages=messages,
    )
    return response.choices[0].message.content


class Bot(commands.Bot):
    """Twitch bot that uses OpenAI's GPTs to chat with viewers."""
    def __init__(self):
        """Initialize the bot with the Twitch token, channel, and client secret."""
        self.last_used = datetime.datetime()
        self.cooldown_period = timedelta(seconds=300)

        super().__init__(token=twitch_token, prefix='!',
                         initial_channels=[twitch_channel],
                         client_secret=twitch_client_secret, )

    async def event_ready(self):
        """Print a message when the bot is ready."""
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        """Handle incoming messages."""
        if message.echo:
            return
        print(message.content)
        await self.handle_commands(message)

    @commands.command()
    async def zee(self, ctx: commands.Context):
        """Chat as Zee using OpenAI's GPT."""
        now = datetime.now()

        # Check if the command is on cooldown
        # pylint: disable=line-too-long
        if now - self.last_used < self.cooldown_period:
            # pylint: disable=line-too-long
            cooldown_remaining = self.cooldown_period - (now - self.last_used).total_seconds()
            # pylint: disable=line-too-long
            await ctx.send(f"Hetze mich nicht! Warter noch {cooldown_remaining:.0f} Sekunden.")
            return

        # Update the last used time
        self.last_used = now

        print(ctx.message.content)
        prompt = ctx.message.content[len('!zee'):].strip()
        print(prompt)
        response = chat_with_openai(prompt, BOT_PERSONALITY)
        await ctx.send(response[:500])


bot = Bot()
bot.run()
