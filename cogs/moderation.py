import discord, sqlite3
from discord.ext import commands

conn = sqlite3.connect('Bot.db')
c = conn.cursor()

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member:discord.Member, *, reason : str = None):
        await ctx.message.delete()
        await ctx.guild.ban(member, reason=reason)
        if reason != None:
            embed = discord.Embed(title=f'{member} was banned for ``{reason}``!', colour = 0x42ffff)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f'{member} was banned!', colour = 0x42ffff)
            await ctx.send(embed=embed)
            


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason : str = None):
        await ctx.message.delete()
        await ctx.guild.kick(member, reason=reason)
        if reason != None:
            embed = discord.Embed(title=f'{member} was kicked for ``{reason}``!', colour = 0x42ffff)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f'{member} was kicked!', colour = 0x42ffff)
            await ctx.send(embed=embed)

    @commands.command()
    async def unblacklist(self, ctx, member: discord.Member):
        await ctx.message.delete()
        embed = discord.Embed(title='User removed from blacklist', description=f"{member.mention} was removed from the blacklist", colour = 0x42ffff)
        await ctx.message.channel.set_permissions(member, read_messages=True, send_messages=True)
        await ctx.send(embed=embed, delete_after=10)
        
    @commands.command()
    async def blacklist(self, ctx, member: discord.Member):
        await ctx.message.delete()
        embed = discord.Embed(title='User blacklisted', description=f"{member.mention} was added to the blacklist", colour = 0x42ffff)
        await ctx.message.channel.set_permissions(member, read_messages=True, send_messages=False)
        await ctx.send(embed=embed, delete_after=10)

    @commands.command()
    @commands.has_role('Owner')
    async def warn(self, ctx, user: discord.Member, *, reason):
        c.execute("SELECT * FROM warns WHERE user=?", (user.name, ))
        test = c.fetchone()
        if test == None:
            count = 1
            c.execute("INSERT INTO warns VALUES (?, ?)", (user.name, count))
        else:
            c.execute("UPDATE warns SET count = count + 1 WHERE user=?", (user.name, ))
        conn.commit()   
        channel = discord.utils.get(ctx.guild.channels, name="staff-warns")
        auth = ctx.message.author
        em = discord.Embed(title="User warned", description=f"{user} was warned for ``{reason}``", colour=0x42ffff)
        em1 = discord.Embed(title="New warning", description=f"{user} was warned", colour=0x42ffff)
        c.execute("SELECT * FROM warns WHERE user=?", (user.name, ))
        coun = c.fetchone()
        count = coun[1]
        em1.add_field(name="Reason", value=f"{reason}", inline=False)
        em1.add_field(name="Total amount of warnings", value="%s" % (count))
        em1.set_footer(text=f"User warned by {auth}")
        await ctx.message.delete()
        await ctx.send(embed=em, delete_after=10)
        await channel.send(embed=em1)
        c.execute("INSERT INTO warnsinfo VALUES (?, ?, ?)", (auth.name, user.name, reason))
        conn.commit()

    @commands.command()
    @commands.has_role('Owner')
    async def warns(self, ctx, user: discord.Member):
        await ctx.message.delete()
        c.execute("SELECT * FROM warnsinfo WHERE user=?", (user.name, ))
        warns = c.fetchall()
        count = -1
        countt = 0
        await ctx.send(":ok_hand:**Oke**, Retrieving warnings", delete_after=10)
        em = discord.Embed(title="Warnings for %s" % (user.name), colour = 0x42ffff)
        for item in warns:
            count += 1
            countt += 1
            reason = warns[count][2]
            warnedby = warns[count][0]
            em.add_field(name="Warning %s" % (countt), value="reason: **%s**. by **%s**" % (reason, warnedby), inline=False)
        await ctx.send(embed=em)   

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int):
        count = 0
        async for message in ctx.channel.history(limit=limit):
            count += 1
        await ctx.channel.purge(limit=limit)
        await ctx.send(':tada: **%s Messages removed**' % (count), delete_after=10) 

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def nuke(self, ctx): 
        await ctx.channel.delete()
        await ctx.guild.create_text_channel(name=ctx.channel.name, category=ctx.channel.category, overwrites=ctx.channel.overwrites)
        
def setup(bot):
    bot.add_cog(Moderation(bot))