from .exraid import EXRaid


def setup(bot):
    n = EXRaid(bot)
    bot.add_cog(n)
