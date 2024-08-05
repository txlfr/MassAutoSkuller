import discord
import asyncio
import json
from discord.ext import commands

# Load the configuration from the JSON file
with open("config.json") as f:
    config = json.load(f)

tokens = config.get("Tokens", []) 
target_user_ids = config.get("TargetUserIDs", [])

class SkullBot(commands.Bot):
    def __init__(self, token):
        super().__init__(command_prefix=';', self_bot=True)
        self.token = token

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        if message.author.id in target_user_ids:
            try:
                await message.add_reaction('😭')
                await message.add_reaction('☠')
                await message.add_reaction('💀')
            except discord.errors.Forbidden:
                print(f"Can't react to message in {message.channel}")
        await self.process_commands(message)

async def run_bot(token):
    bot = SkullBot(token)
    try:
        await bot.start(token)
    except discord.errors.LoginFailure:
        print(f"Failed to log in with token: {token[:10]}...")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

async def main():
    tasks = [run_bot(token) for token in tokens]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
