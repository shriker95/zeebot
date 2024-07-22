from twitchio.ext import commands
import openai
from dotenv import load_dotenv
import os

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
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=twitch_token, prefix='!', initial_channels=[twitch_channel], client_secret=twitch_client_secret, )

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Print the contents of our message to console...
        print(message.content)

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    @commands.command()
    async def zee(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        print(ctx.message.content)
        prompt = ctx.message.content[len('!zee'):].strip()
        print(prompt)
        response = chat_with_openai(prompt, BOT_PERSONALITY)
        await ctx.send(response[:500])


bot = Bot()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.