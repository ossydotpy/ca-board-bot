# clipboard_cog.py
import discord
from discord.ext import commands
from db_handler import DatabaseHandler
from utils.funcs import is_valid_solana_address



class ClipboardCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DatabaseHandler()


    @commands.command(name='ca')
    async def add_contract_manually(self, ctx, contract_address: str):
        """Manually add a contract to the server's clipboard"""
        
        if not is_valid_solana_address(contract_address):
            await ctx.send("❌ Invalid Solana contract address.")
            return

        if self.db.add_contract(
            contract_address, 
            ctx.guild.id, 
            ctx.author.id
        ):
            await ctx.send(f"✅ Contract `{contract_address}` added to clipboard.")
        else:
            await ctx.send("❌ Contract already exists in this server's clipboard.")

    @commands.command(name='by')
    async def contracts_by_user(self, ctx, member: discord.Member = None):
        """Show contracts added by a specific user or yourself"""
        target_user = member or ctx.author

        if target_user.guild.id != ctx.guild.id:
            await ctx.send("❌ You can only check contracts for members in this server.")
            return

        cursor = self.db.conn.cursor()
        cursor.execute('''
            SELECT contract_address, timestamp 
            FROM contracts 
            WHERE server_id = ? AND discord_user_id = ?
            ORDER BY timestamp DESC 
            LIMIT 10
        ''', (ctx.guild.id, target_user.id))
        
        contracts = cursor.fetchall()

        if not contracts:
            await ctx.send(f"No contracts found for {target_user.display_name}.")
            return

        embed = discord.Embed(
            title=f"📋 Contracts by {target_user.display_name}", 
            color=discord.Color.green()
        )

        for address, timestamp in contracts:
            embed.add_field(
                name="",
                value=(
                    f"```{address}```"
                    f"**@:** {timestamp}\n"
                ),
                inline=False
            )

        await ctx.send(embed=embed)

    @commands.command(name='clear')
    @commands.has_permissions(manage_messages=True)
    async def clear_clipboard(self, ctx):
        """Clear all contracts for this server (Moderator only)"""
        cursor = self.db.conn.cursor()
        cursor.execute('DELETE FROM contracts WHERE server_id = ?', (ctx.guild.id,))
        self.db.conn.commit()
        
        await ctx.send("🧹 Server clipboard has been cleared.")

    @commands.command(name='contractcount')
    async def contract_count(self, ctx):
        """Show the total number of contracts in the server's clipboard"""
        cursor = self.db.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM contracts WHERE server_id = ?', (ctx.guild.id,))
        count = cursor.fetchone()[0]

        await ctx.send(f"📊 Total contracts in this server's clipboard: {count}")

    def cog_unload(self):
        """Ensure database connection is closed when cog is unloaded"""
        self.db.close()

async def setup(bot):
    await bot.add_cog(ClipboardCog(bot))