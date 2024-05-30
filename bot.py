import discord
from discord.ext import commands
from discord import app_commands
import requests
from bs4 import BeautifulSoup

#---------- Informations required for the bot ----------#
token = 'YOUR_BOT_TOKEN'
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents)

#---------- Commands ----------#
# Get Fluxus Key
@bot.tree.command(description="Get fluxus android key.")
@app_commands.describe(
    hwid='Enter your HWID'
)
async def key(interaction: discord.Interaction, hwid: str):
    print(f"User: {interaction.user.name} | Server: {interaction.guild.name} | HWID: {hwid}")

    if not hwid.startswith("https://flux.li/android/external/start.php?HWID="):
        url = f"https://flux.li/android/external/start.php?HWID={hwid}"
    else:
        url = hwid

    await interaction.response.defer()

    start_header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.71 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    }

    header = {
        "Referer": "https://linkvertise.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.71 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    }

    check_1 = "https://flux.li/android/external/check1.php"
    key_url = "https://flux.li/android/external/main.php"

    session = requests.Session()

    response = session.get(url, headers=start_header).text
    if "You will be redirected in" in response:
        session.get(check_1, headers=header)
        key = BeautifulSoup(str(session.get(key_url, headers=header).text), 'html.parser').find_all(attrs={"data-aos": "fade-left"})[2].text.strip()
        await interaction.edit_original_response(content=f"```{key}```")
    else:
        await interaction.edit_original_response(content="Can't get key!")

@key.error
async def key_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    print(f"ERROR: {error}")

#---------- Bot's events ----------#
#-- Log on --#
@bot.event
async def on_ready():
    #--- Sync commands ---#
    await bot.tree.sync()
    print(f'Logged on as {bot.user}')

#---------- Run bot ----------#
bot.run(token)
