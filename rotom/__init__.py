from .cog1.cog1 import Cog1
from .cog2.cog2 import Cog2


def setup(bot):
    bot.add_cog(Cog1(bot))
    bot.add_cog(Cog2(bot))
