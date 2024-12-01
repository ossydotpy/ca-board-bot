import discord
from discord.ext import commands
from db_handler import DatabaseHandler
from utils.funcs import is_valid_contract_address, time_ago
from utils.views import call_embed



class MonitorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DatabaseHandler()

    def extract_contract_info(self, message):
        """Extract Solana contract addresses from message"""
        words = message.content.split()
        return [word for word in words if is_valid_contract_address(word)]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        contracts = self.extract_contract_info(message)
        for ca in contracts:
            username = message.author.name

            embed, view = await call_embed(ca, username, user_id=message.author.id)
            await message.channel.send(embed=embed, view=view, reference=message)


async def setup(bot):
    await bot.add_cog(MonitorCog(bot))
