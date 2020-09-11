import discord
from discord.ext import commands
import asyncio


class Members(commands.Cog):

    def __init__(self, client):
        self.client = client

    # LISTENERS
    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, name='Member')
        await member.add_roles(role)

        for guild in self.client.guilds:
            for channel in guild.text_channels:
                if channel.name == 'welcome':
                    await channel.send(f'{member.name} Joined the server!')

    # COMMANDS
    @commands.command()
    async def invite(self, ctx, *, member: discord.Member):
        """ Sends a dm with server invite to specified member """
        channel = await member.create_dm()
        await channel.send(await ctx.channel.create_invite())

    @commands.command()
    async def roleadd(self, ctx, member: discord.Member, *, role):
        """ adds role to mentioned member """
        role = discord.utils.get(member.guild.roles, name=role)
        await member.add_roles(role)

    @commands.command()
    async def rolerem(self, ctx, member: discord.Member, *, role):
        """ removes role to mentioned member """
        role = discord.utils.get(member.guild.roles, name=role)
        await member.remove_roles(role)

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """ kicks memeber from server """
        await member.kick(reason=reason)

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """ bans member args: usr object """
        await member.ban(reason=reason, delete_message_days=2)

    @commands.command()
    async def unban(self, ctx, *, member):
        """ unbans member args: name#tag """
        banned_users = await ctx.guild.bans()
        member_name, member_id = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_id):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.name}')

    @commands.command()
    async def mute(self, ctx, time=0, *, member: discord.Member):

        if not member:
            ctx.send('Give me someone to mute pls.')
            return

        if self.client.user == member:
            embed = discord.Embed(title='You can\'t mute me i am too comfy!')
            await ctx.send(embed)
            pass

        role = discord.utils.get(member.guild.roles, name='Muted')
        await member.add_roles(role)
        await ctx.send('{0.mention} has been muted by {1.mention}.'.format(member, ctx.author))

        if time > 0:
            await asyncio.sleep(time * 60)
            await member.remove_roles(role, reason='Time\'s up')

    # LOOPS


def setup(client):
    client.add_cog(Members(client))
