import os
import random
from datetime import timedelta
from typing import Type, Union

from typing_extensions import override

import discord
from discord.ext import commands
from discord.ext.track_edits import EditTrackableContext, EditTrackerCog


class Bot(commands.Bot):
    async def setup_hook(self) -> None:
        await self.add_cog(
            EditTrackerCog(
                self,
                max_duration=timedelta(minutes=5),
                execute_untracked_edits=True,
                ignore_edits_if_not_yet_responded=False,
            ),
        )

    @override
    async def get_context(
        self,
        origin: Union[discord.Message, discord.Interaction],
        *,
        cls: Type[EditTrackableContext] = EditTrackableContext,
    ) -> EditTrackableContext:
        return await super().get_context(origin, cls=cls)


intents = discord.Intents.default()
intents.message_content = True

bot = Bot(command_prefix="!", intents=intents)


@bot.command()
async def add(ctx: commands.Context[Bot], left: int, right: int):
    """Adds two numbers together."""

    if random.random() < 0.5:
        _ = await ctx.reply(str(left + right), mention_author=False)
    else:
        _ = await ctx.reply(
            embed=discord.Embed(description=f"{left} + {right} = {left + right}"),
            mention_author=False,
        )


if __name__ == "__main__":
    bot.run(os.environ["DISCORD_TOKEN"])
