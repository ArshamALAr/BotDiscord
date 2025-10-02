import discord
import asyncio
from discord.ext import commands, tasks
from itertools import cycle

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

voice_stats = {}

status_messages = cycle([
    "By Ar Development",
    "ArDev Members: Loading..."
])

@bot.event
async def on_ready():
    print(f'Bot Run Shod Ba User: {bot.user}!')
    update_status.start()

@tasks.loop(seconds=30)
async def update_status():
    current_status = next(status_messages)

    if "ArDev Members" in current_status:
        target_guild_id = 1407535480098001059
        target_guild = discord.utils.get(bot.guilds, id=target_guild_id)
        member_count = len(target_guild.members) if target_guild else "Unknown"
        current_status = f"ArDev Members: {member_count}"

    activity = discord.Activity(type=discord.ActivityType.watching, name=current_status)
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.command()
@commands.has_permissions(administrator=True)
async def send(ctx, *, message):
    await ctx.message.delete()
    await ctx.channel.send(message)

@bot.command()
@commands.has_permissions(administrator=True)
async def sendembed(ctx, *, message):
    await ctx.message.delete()
    embed = discord.Embed(description=message, color=discord.Color.blue())
    await ctx.channel.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def stats(ctx, category_name):
    category = discord.utils.get(ctx.guild.categories, name=category_name)
    if not category:
        await ctx.send("Category Vojod Nadarad!")
        return

    target_guild_id = 1407535480098001059
    target_guild = discord.utils.get(bot.guilds, id=target_guild_id)

    if not target_guild:
        await ctx.send("Guild Morede Nazar Peyda Nashod!")
        return

    member_count = len(target_guild.members)

    if category.id not in voice_stats:
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(connect=False)
        }
        vc = await ctx.guild.create_voice_channel(
            name=f"ArDev Members: {member_count}",
            category=category,
            overwrites=overwrites
        )
        voice_stats[category.id] = vc.id
    else:
        vc = bot.get_channel(voice_stats[category.id])
        await vc.edit(name=f"ArDev Members: {member_count}")


@bot.event
async def on_member_join(member):
    target_guild_id = 1407535480098001059
    target_guild = discord.utils.get(bot.guilds, id=target_guild_id)
    if not target_guild:
        return

    member_count = target_guild.member_count

    for cat_id, vc_id in voice_stats.items():
        vc = bot.get_channel(vc_id)
        await vc.edit(name=f"ArDev Members: {member_count}")

@bot.event
async def on_member_remove(member):
    target_guild_id = 1407535480098001059
    target_guild = discord.utils.get(bot.guilds, id=target_guild_id)
    if not target_guild:
        return

    member_count = target_guild.member_count

    for cat_id, vc_id in voice_stats.items():
        vc = bot.get_channel(vc_id)
        await vc.edit(name=f"ArDev Members: {member_count}")

@send.error
@sendembed.error
@stats.error
async def permission_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Shoma Permission Nadarid!")

bot.run("MTQxNjU5NzQxOTI5NDA2NDcwMA.Gjwpqv.w2rkianYMvnhViOIuAnkD-hSyRgN6cOVpAKtQE")