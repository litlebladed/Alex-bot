import discord
from discord.ext import commands

class OnJoinLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.channels, name="joined")
        await channel.send("%s Joined" % (member.mention))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.channels, name="joined")
        await channel.send("%s Left" % (member.mention))

def setup(bot):
    bot.add_cog(OnJoinLeave(bot))