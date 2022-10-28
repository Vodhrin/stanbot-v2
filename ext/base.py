import disnake
import lang
import utils
import io
from disnake.ext import commands
from bot import StanBot


class Base(commands.Cog):
    def __init__(self, bot: StanBot):
        self.bot = bot

    @commands.slash_command(
        description="Ask Stan to imbue text with sussiness.",
        dm_permission=True
    )
    async def sussify(self,
                      inter: disnake.ApplicationCommandInteraction,
                      text: str = commands.Param(description="The text to rape.")
                      ):

        await inter.response.defer()

        try:
            result = lang.replace_words_by_tag_random(text).replace("  ", "\n")
            if len(result) < 2001:
                await inter.send(result)
            else:
                await inter.send("Result over 2000 characters, initiating poop dispenser:")
                it = [result[i:min(i+2000, len(result))] for i in range(0, len(result), 2000)]
                for i in it:
                    await inter.channel.send(i)
        except Exception as e:
            await inter.send("I farded.")
            await utils.relay_error(self.bot, e, await inter.original_message())

    @commands.message_command(
        name="Sussify Message",
        description="Ask Stan to imbue text with sussiness.",
        dm_permission=True
    )
    async def sussify_selected(self, inter: disnake.ApplicationCommandInteraction):

        if not inter.target or len(inter.target.content) < 1:
            await inter.send("I can't sussify that, retard.")
            return

        await self.sussify(inter, inter.target.content)

    @commands.slash_command(
        description="Change Stan's activity.",
        dm_permission=True
    )
    async def set_activity(self,
                           inter: disnake.ApplicationCommandInteraction,
                           activity_name: str = commands.Param(description="The name of the activity to display."),
                           activity_type: disnake.ActivityType = commands.param(description="The type of activity.")
                           ):

        try:
            activity = disnake.Activity(name=activity_name, type=activity_type)
            await self.bot.change_presence(activity=activity)
            await inter.send(f"Activity set to '{activity_name}'.")
        except Exception as e:
            await inter.send("I farded")
            await utils.relay_error(self.bot, e, await inter.original_message())


def setup(bot: StanBot) -> None:
    bot.add_cog(Base(bot))
