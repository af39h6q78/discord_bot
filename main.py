import discord
import asyncio
from discord import app_commands

# Enable necessary bot intents
intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True
intents.members = True  # Required for moderation commands & mentions

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    print(f"✅ Bot is ready as {client.user} and commands are synced!")

# `/help` command (Lists all commands)
@tree.command(name="help", description="Lists all available commands and their usage.")
async def help_command(interaction: discord.Interaction):
    help_text = (
        "**📖 Bot Command Guide**\n\n"
        "🔹 **/help** → Shows this message.\n"
        "🔹 **/say <message>** → Bot repeats your message.\n"
        "🔹 **/devbadge** → Links the discord developer page.\n"
        "🔹 **/warn <user> <reason>** → Warns a user.\n"
        "🔹 **/kick <user> <reason>** → Kicks a user (Requires `Kick Members`).\n"
        "🔹 **/ban <user> <reason>** → Bans a user (Requires `Ban Members`).\n"
        "🔹 **/sping <user> <pings_per_message> <messages>** → Spams mentions in controlled messages.\n"
        "============================================\n"
        "**📌 `/sping` Limits:**\n"
        "- Keep in mind that the limits are so discord does not limit or block the bot\n"
        "� Max **10 mentions per message**\n"
        "� Max **20 messages per command**\n"
        "� **1-second delay** between messages to avoid rate-limiting\n"
        "� Requires **Manage Messages permission**\n"
        "============================================\n"
        "made by me 😪"
    )
    await interaction.response.send_message(help_text)

# `/devbadge` command 
@tree.command(name="devbadge", description="Get the Developer Badge")
async def devbadge(interaction: discord.Interaction):
    await interaction.response.send_message("Check the [Discord Developer Portal](<https://discord.com/developers/active-developer>) to claim")

# `/warn` command
@tree.command(name="warn", description="Warns a user")
async def warn(interaction: discord.Interaction, user: discord.Member, reason: str):
    await interaction.response.send_message(f"⚠️ {user.mention} has been warned for: **{reason}**")

# `/kick` command
@tree.command(name="kick", description="Kicks a user")
async def kick(interaction: discord.Interaction, user: discord.Member, reason: str):
    if interaction.user.guild_permissions.kick_members:
        await user.kick(reason=reason)
        await interaction.response.send_message(f"👢 {user.mention} has been kicked for: **{reason}**")
    else:
        await interaction.response.send_message("❌ You do not have permission to kick members.", ephemeral=True)

# `/ban` command
@tree.command(name="ban", description="Bans a user")
async def ban(interaction: discord.Interaction, user: discord.Member, reason: str):
    if interaction.user.guild_permissions.ban_members:
        await user.ban(reason=reason)
        await interaction.response.send_message(f"🔨 {user.mention} has been banned for: **{reason}**")
    else:
        await interaction.response.send_message("❌ You do not have permission to ban members.", ephemeral=True)

# '/sping` command (Spam Ping with user, pings per message, and total messages)
@tree.command(name="sping", description="Spam ping a user multiple times with custom message count")
async def sping(interaction: discord.Interaction, user: discord.Member, pings_per_message: int, messages: int):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("❌ You do not have permission to use this command.", ephemeral=True)
        return

    # Set limits here
    max_pings_per_message = 10
    max_messages = 20
    pings_per_message = min(pings_per_message, max_pings_per_message)
    messages = min(messages, max_messages)

    await interaction.response.send_message(f"🚨 Spamming {user.mention} **{pings_per_message} times per message** for **{messages} messages**...")

    ping_text = " ".join([user.mention] * pings_per_message)  

    for _ in range(messages):
        await interaction.channel.send(ping_text)
        await asyncio.sleep(1)  # Prevent rate-limiting

# Run the bot
TOKEN_PATH = "token.txt"
with open(TOKEN_PATH, "r") as file:
    TOKEN = file.read().strip()

client.run(TOKEN)
