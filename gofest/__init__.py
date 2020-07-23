from .gofest import GoFest


def setup(bot):
    bot.add_cog(GoFest(bot))