import disnake
import voice
import utils
from disnake.ext import commands
from bot import StanBot


class Radio(commands.Cog):
    def __init__(self, bot: StanBot):
        self.bot = bot

    @commands.slash_command(
        description="Command Stan to play audio from a url.",
        dm_permission=False
    )
    async def play(self,
                   inter: disnake.ApplicationCommandInteraction,
                   url: str = commands.Param(description="The url to play.")
                   ) -> None:

        channel = voice.try_get_voice_channel(inter.author)
        if channel is None:
            await inter.send("Where, retard?")
            return

        vc = await voice.ensure_in_channel(self.bot, channel)

        try:
            await vc.enqueue(url, inter)
        except Exception as e:
            await inter.send("I farded.")
            await utils.relay_error(self.bot, e, await inter.original_message())

    @commands.slash_command(
        description="Command Stan to skip the current item in queue.",
        dm_permission=False
    )
    async def skip(self,
                   inter: disnake.ApplicationCommandInteraction
                   ):

        channel = voice.try_get_voice_channel(inter.guild.me)
        if channel is None:
            await inter.send("Retard")
            return

        vc = voice.try_get_voice_client(self.bot, channel)
        if vc:
            await vc.skip(inter)
        else:
            await inter.send("Retard.")

    @commands.slash_command(
        description="Forces Stan to disconnect from the voice channel in this guild.",
        dm_permission=False
    )
    async def disconnect(self,
                         inter: disnake.ApplicationCommandInteraction
                         ) -> None:

        channel = voice.try_get_voice_channel(inter.author)
        if channel is None:
            await inter.send("Retard.")
            return

        vc = voice.try_get_voice_client(self.bot, channel)

        if vc is not None:
            await vc.disconnect()
            await inter.send(f"Banished from {channel.name}.")
        else:
            await inter.send("Retard.")

    @commands.slash_command(
        description="Command Stan to toggle looping queue mode.",
        dm_permission=False
    )
    async def loop(self,
                   inter: disnake.ApplicationCommandInteraction
                   ):

        channel = voice.try_get_voice_channel(inter.guild.me)
        if channel is None:
            await inter.send("Retard")
            return

        vc = voice.try_get_voice_client(self.bot, channel)
        if vc:
            await vc.toggle_looping(inter)
        else:
            await inter.send("Retard.")


def setup(bot: StanBot) -> None:
    bot.add_cog(Radio(bot))
