import logging
from discord.ext import commands
from sqlalchemy.ext.asyncio import AsyncEngine


class Boggart(commands.Bot):
    def __init__(
        self,
        *args,
        initial_extensions: list[str],
        pg_engine: AsyncEngine,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.initial_extensions = initial_extensions
        self.pg_engine = pg_engine
        self.command_prefix = "!"
        self.logger = logging.getLogger("discord")

    async def setup_hook(self) -> None:
        """Load anything that should be in memory prior to handling events"""
        for extension in self.initial_extensions:
            await self.load_extension(extension)
            self.logger.info(f"{extension} loaded")
