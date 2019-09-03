from .pokemon import Pokemon
from .rotom import Rotom
from .raidtrain import RaidTrain


def setup(bot):
    bot.add_cog(Pokemon(bot))
    bot.add_cog(Rotom(bot))
    bot.add_cog(RaidTrain(bot))
    bot.add_cog(Raids(bot))
