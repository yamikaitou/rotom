from .pokemon import Pokemon
from .rotom import Rotom
from .raidtrain import RaidTrain
from .raids import Raids
from .contest import Contests


def setup(bot):
    cmds = ["info"]
    for cmd_name in cmds:
        old_cmd = bot.get_command(cmd_name)
        if old_cmd:
            bot.remove_command(old_cmd.name)

    bot.add_cog(Pokemon(bot))
    bot.add_cog(Rotom(bot))
    bot.add_cog(Raids(bot))
    bot.add_cog(Contests(bot))
