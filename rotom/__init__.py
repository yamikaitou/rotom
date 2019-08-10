from .pokemon import Pokemon
from .rotom import Rotom


def setup(bot):
    bot.add_cog(Pokemon(bot))
    bot.add_cog(Rotom(bot))
