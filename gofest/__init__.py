from .gofest import gofest


def setup(bot):
    bot.add_cog(GoFest(bot))