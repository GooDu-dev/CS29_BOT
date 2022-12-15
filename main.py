import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import json
from pathlib import Path
import datetime
from online import keep_alive

bot_json = json.load(open("./bot.json", encoding="utf-8"))

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = discord.Client(intents=intents)
bot = commands.Bot(command_prefix=bot_json["COMMAND_PREFIX"],
                   intents=intents,
                   help_command=None)


@bot.event
async def on_ready():
  print(f"\n{bot.user} Online\n")


@bot.event
async def on_member_join(member):
  channel = bot.get_channel(int(os.environ["WELCOME_CHANNEL_ID"]))
  embed = discord.Embed(
    title="Welcome to Computer Science KMITL",
    description="Congratulations! You are computer science now.",
    color=discord.Color(int(bot_json["EMBED_COLOR"], 16)))
  embed.set_thumbnail(url=member.display_avatar.url)
  embed.set_author(icon_url=member.guild.icon.url, name="CS29")
  embed.set_footer(text=member)
  embed.timestamp = datetime.datetime.utcnow()
  await channel.send(embed=embed)


@bot.event
async def on_message(message):
  if message.channel.id == os.environ["VERIFY_CHANNEL_ID"]:
    if len(message.split(" ")) == 3:
      with open("data.env", "a+") as data_env:
        data_env.write(message.author.id + "=" + message.content)
    await message.delete()
  await bot.process_commands(message)


@bot.command(name="test")
async def test(ctx):
  await ctx.channel.send("Hello")


@bot.command(name="law")
async def law(ctx):
  embed = discord.Embed(title="กฏการใช้ดิสนี้",
                        description="",
                        color=discord.Color(int(bot_json["EMBED_COLOR"], 16)))
  for i in range(len(bot_json["RULES"])):
    embed.description += str(i + 1) + "." + bot_json["RULES"][i] + "\n"
  embed.set_thumbnail(url=ctx.guild.icon.url)
  embed.add_field(
    name="อย่าลืมไปยืนยันตัวตนกันนะ",
    value=f"{bot.get_channel(int(os.environ['VERIFY_CHANNEL_ID'])).mention}")
  await ctx.channel.send(embed=embed)
  await ctx.message.delete()


@bot.command(name="verify")
async def verify_alert(ctx):
  embed = discord.Embed(title="ยืนยันตัวตน",
                        description="พิมพ์ ^comsci",
                        color=discord.Color(int(bot_json["EMBED_COLOR"], 16)))
  embed.set_thumbnail(url=ctx.guild.icon.url)
  embed.add_field(
    name="พบปัญหาโปรดแจ้ง",
    value=f"{ctx.guild.get_role(int(os.environ['ADMIN_ROLE_ID'])).mention}")
  await ctx.send(embed=embed)


@bot.command(name="comsci")
async def verify(ctx):
  embed = discord.Embed(
    title="วิธีการยืนยันตัวตน",
    description=
    "พิมพ์ตามที่ลิงบอกอย่าเคร่งครัด ไม่งั้นเดี๋ยวโปรแกรมบัคเด้ออ5555555",
    color=discord.Color(int(bot_json["EMBED_COLOR"], 16)))
  embed.add_field(
    name="วิธีการพิมพ์ชื่อ-นามสกุล",
    value="ใช้พิมพ์ชื่อ นามสกุล\nเช่น นายโดนัทยังมีรู แล้วเมื่อไหรยูจะมีใจ",
    inline=False)
  embed.add_field(name="รอบที่เข้า",
                  value="ให้พิมพ์เเค่เลขรอบ เช่น 1, 2, 3",
                  inline=False)
  embed.add_field(name="ตัวอย่างการตอบ",
                  value="นายโดนัทยังมีรู แล้วเมื่อไหรยูจะมีใจ 1",
                  inline=False)
  await ctx.channel.send(embed=embed)
  await ctx.channel.send(
    discord.Embed(
      title="ลิงขอทราบ ชื่อ-สกุล รอบที่เข้า ของน้องๆหน่อยนะเจี๊้ยก!"))
  await ctx.message.delete()


keep_alive()
try:
  bot.run(os.environ['BOT_TOKEN'])
except discord.errors.HTTPException:
  os.system("kill 1")
  os.system("python restart.py")
