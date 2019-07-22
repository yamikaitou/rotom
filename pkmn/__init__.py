from .pkmn import Pokemon


def setup(bot):
    bot.add_cog(Pokemon(bot))
