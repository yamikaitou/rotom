from .pokemon import Pokemon
from .rotom import Rotom
from .raidtrain import RaidTrain
from .raids import Raids
from .contest import Contests


def setup(bot):

    bot.add_cog(Pokemon(bot))
    bot.add_cog(Rotom(bot))
    bot.add_cog(Raids(bot))
