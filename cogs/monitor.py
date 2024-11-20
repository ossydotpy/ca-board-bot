import discord
from discord.ext import commands
from db_handler import DatabaseHandler
from utils.funcs import is_valid_solana_address



class MonitorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DatabaseHandler()

    def extract_contract_info(self, message):
        """Extract Solana contract addresses from message"""
        words = message.content.split()
        return [word for word in words if is_valid_solana_address(word)]

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        contracts = self.extract_contract_info(message)
        for contract in contracts:
            if self.db.add_contract(
                contract,
                message.guild.id, 
                message.author.id
            ):
                await message.add_reaction('📋')

    @commands.command(name='clipboard')
    async def show_clipboard(self, ctx):
        """Show recent contracts for the current server"""
        recent_contracts = self.db.get_recent_contracts(ctx.guild.id)
        
        if not recent_contracts:
            await ctx.send("No contracts in clipboard for this server.")
            return

        embed = discord.Embed(
            title="📋 Server Contract Clipboard",
            description="Here are the recent contracts submitted by users.",
            color=discord.Color.blue()
        )

        for idx, (address, discord_user_id, timestamp) in enumerate(recent_contracts, start=1):
            
            user = self.bot.get_user(discord_user_id) or await self.bot.fetch_user(discord_user_id)
            username = user.name if user else "Unknown User"

            embed.add_field(
                name="",
                value=(
                    f"```{address}```"
                    f"** By:** {username} **@:** {timestamp}\n"
                ),
                inline=False
            )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(MonitorCog(bot))
