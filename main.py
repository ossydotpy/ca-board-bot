from typing import Optional, Literal

import discord
import os, asyncio

import discord
import os, asyncio

from discord import app_commands, Activity, ActivityType
from discord.ext import commands
from discord.ext.commands import Context, Greedy

from dotenv import load_dotenv
from datetime import datetime
import db_handler

load_dotenv()


TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    print(f"{datetime.now()} | Bot {client.application_id} is online.")
    await client.change_presence(
        activity=Activity(type=ActivityType.watching, name="dee's mom")
    )
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await client.load_extension(f"cogs.{filename[:-3]}")
                print(f"{datetime.now()} | {filename[:-3]} loaded successfully.")
            except Exception as e:
                print(f"{datetime.now()} | Error loading {filename}: {e}")


@client.command(hidden=True)
@commands.guild_only()
@commands.is_owner()
async def sync(
    ctx: Context,
    guilds: Greedy[discord.Object],
    spec: Optional[Literal["~", "*", "^"]] = None,
) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.client.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.client.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.client.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.client.tree.clear_commands(guild=ctx.guild)
            await ctx.client.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.client.tree.sync()

        await ctx.send(
            f"{datetime.now()} | Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        print(
            f"{datetime.now()} | Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return


async def main():
    await client.start(TOKEN)


if __name__=='__main__':
    asyncio.run(main())