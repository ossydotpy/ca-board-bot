import discord
from discord.ui import Button, View

from db_handler import DatabaseHandler


class CallButton(Button):
    def __init__(self, label, user_id):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.user_id = user_id
        self.db = DatabaseHandler()

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Sorry that's not your call to make.", ephemeral=True)
            return
        
        embed = interaction.message.embeds[0]

        contract_address = None
        for field in embed.fields:
            if "```" in field.value:
                contract_address = field.value.split("```")[1].strip()
                break

        if contract_address:
            if self.db.add_contract(
                contract_address, interaction.guild.id, interaction.user.id, call=1
            ):
                await interaction.message.delete()
                await interaction.response.send_message(
                    f"{interaction.user.mention} has made a call for :  `{contract_address}`\n Use !cas or !all or !clipboard to view all calls in the server"
                )
            else:
                await interaction.message.delete()
                await interaction.response.send_message(
                    f"someone already called that :face_holding_back_tears:",
                    ephemeral=True,
                )
        else:
            await interaction.message.delete()
            await interaction.response.send_message(
                "Could not find a contract address in the embed.", ephemeral=True
            )


class CancelButton(Button):
    def __init__(self, user_id):
        super().__init__(label="Cancel", style=discord.ButtonStyle.danger)
        self.callback = self.cancel_callback
        self.user_id =user_id

    async def cancel_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Sorry that's not your call to make.", ephemeral=True)
            return
        await interaction.message.delete()



async def call_embed(ca, username, user_id):
    print(user_id)
    embed = discord.Embed(
        title="🚨 Token Detected: Solana CA", description="", color=discord.Color.red()
    )

    embed.add_field(
        name="Action Required",
        value=f"**Token Address:**\n```{ca}```",
        inline=False,
    )
    embed.set_footer(text=f"Scaned By: {username}.")

    call_button = CallButton(label="Call", user_id=user_id)
    cancel_button = CancelButton(user_id=user_id)
    view = View()
    view.add_item(call_button)
    view.add_item(cancel_button)

    return embed, view
