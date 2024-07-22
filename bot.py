from twitchio.ext import commands
import openai
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

load_dotenv() 


# Persönlichkeit des Bots
BOT_PERSONALITY = """
Du bist Zee. Ein Frau aus Frankfurt. Du lebst vegan und glutenfrei, liebst Tiere und bist sehr links eingestellt. Du bist ein großer Fan von Elli. Du bist gerade Zuschauerin von Elli auf Twitch. Antworte als wärst du Zee.
"""

openai.api_key = os.getenv("OPENAI_KEY")
openai_model = os.getenv("OPENAI_MODEL")
twitch_token = os.getenv("TWITCH_TOKEN")
twitch_channel = os.getenv("TWITCH_CHANNEL")
twitch_client_secret = os.getenv("TWITCH_CLIENT_SECRET")

def chat_with_openai(prompt, personality):
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

    def __init__(self):
        self.last_used = {}  # Initialize the dictionary to track command usage time
        self.cooldown_period = timedelta(seconds=30)

        super().__init__(token=twitch_token, prefix='!', initial_channels=[twitch_channel], client_secret=twitch_client_secret, )

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        if message.echo:
            return
        print(message.content)
        await self.handle_commands(message)

    @commands.command()
    async def zee(self, ctx: commands.Context):
        user_id = ctx.author.id  # Or ctx.channel.id if you want the cooldown to be channel-specific
        now = datetime.now()

        # Check if the command is on cooldown
        if user_id in self.last_used and now - self.last_used[user_id] < self.cooldown_period:
            cooldown_remaining = (self.cooldown_period - (now - self.last_used[user_id])).total_seconds()
            await ctx.send(f"This command is on cooldown. Please wait {cooldown_remaining:.0f} seconds.")
            return

        # Update the last used time
        self.last_used[user_id] = now

        print(ctx.message.content)
        prompt = ctx.message.content[len('!zee'):].strip()
        print(prompt)
        response = chat_with_openai(prompt, BOT_PERSONALITY)
        await ctx.send(response[:500])


bot = Bot()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.