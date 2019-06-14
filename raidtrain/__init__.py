from .raidtrain import RaidTrain


def setup(bot):
    bot.add_cog(RaidTrain(bot))
