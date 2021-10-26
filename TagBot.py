# This program is not completed and still has a few bugs. Despite bugs, it is still capable of running a game of tag over discord.

import discord
from discord.ext import commands
import os
from datetime import datetime

client = discord.Client()

# TAG Variables
date_last_tagged = datetime.now()
tag_history = [" "]
cur_tagger = " "

bot = commands.Bot(command_prefix='$', case_insensitive=True)


@bot.event
async def on_ready():
    print('logged in')

@bot.command()
@commands.has_role("Tagger")
async def tag(ctx, member:discord.Member):
  print("In tag")
  if (tag_history[-1] != member.name):
    print("Tagging...")
    tagrole= discord.utils.get(ctx.guild.roles, name="Tagger")
    await member.add_roles(tagrole)
    await ctx.author.remove_roles(tagrole)
    await ctx.send("{} is it! Run!".format(member.mention))
    tag_history.append(ctx.author.name)
    tag_history.pop(0)
    cur_tagger = member.name
    print("Current Tagger: ", cur_tagger)
    print("Tag History: ", tag_history)
  else:
    await ctx.send("{} no tag backs!".format(ctx.author.name))

@bot.command()
@commands.has_role("Admin")
async def cleartag(ctx):
  print("Clearing taggers")
  tagrole = discord.utils.get(ctx.guild.roles, name="Tagger")
  tagger_ary = []
  for member in tagrole.members:
    print(member.name)
    tagger_ary.append(member)
  print(tagger_ary)
  for tagger in tagger_ary:
    tagger.remove_roles(tagrole)
    print(tagger.name)
    await ctx.send("{} is no longer it.".format(tagger.name))


@bot.command()
async def settagger(ctx, member:discord.Member):
  print("Setting Tagger")

  tagrole = discord.utils.get(ctx.guild.roles, name="Tagger")
  try:
    user = discord.utils.get(ctx.guild.members, name = cur_tagger)
    user.remove_roles(tagrole)
    pass
  except UnboundLocalError:
    pass
  
  await member.add_roles(tagrole)
  await ctx.send("{} is it! Run!".format(member.mention))
  cur_tagger = member.name

  tag_history.pop(0)
  print("Tag History: ", tag_history)

bot.run(os.getenv('TOKEN'))
