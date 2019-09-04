from .pokemon import Pokemon
from .rotom import Rotom
from .raidtrain import RaidTrain
from .raids import Raids


def setup(bot):
    cmds = ["info", "help"]
    for cmd_name in cmds:
        old_cmd = bot.get_command(cmd_name)
        if old_cmd:
            bot.remove_command(old_cmd.name)
    
    bot.add_cog(Pokemon(bot))
    bot.add_cog(Rotom(bot))
    bot.add_cog(RaidTrain(bot))
    bot.add_cog(Raids(bot))
