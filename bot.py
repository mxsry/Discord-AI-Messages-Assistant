import discord
from discord import app_commands
from discord.ext import commands
import asyncio

from config.settings import DISCORD_TOKEN, MAX_SUMMARY_MESSAGES, SUMMARY_CONTEXT_MESSAGES, MAX_PROMPT_CHARS
from services.gemini_call import GeminiService


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
)

gemini = GeminiService()

def split_message(text: str, limit: int = 2000) -> list[str]:
    """
    Split long text into multiple Discord messages.
    Tries to split on newlines instead of cutting words.
    """
    chunks = []
    current = ""
    for paragraph in text.split("\n"):
        if len(current) + len(paragraph) + 1 > limit:
            chunks.append(current)
            current = paragraph
        else:
            if current:
                current += "\n"
            current += paragraph
    if current:
        chunks.append(current)
    return chunks

async def send_response(interaction: discord.Interaction, text: str):
    """ Send one or more Discord messages depending on length. """
    for chunk in split_message(text):
        await interaction.followup.send(chunk)

async def get_recent_messages(channel: discord.TextChannel) -> tuple[str, str]:
    history = []
    current_size = 0

    async for message in channel.history(limit=MAX_SUMMARY_MESSAGES):
        if message.author.bot:
            continue
        if not message.content.strip():
            continue

        timestamp = message.created_at.strftime("%H:%M")
        text = (
            f"[{timestamp}] "
            f"{message.author.display_name}: "
            f"{message.content}"
        )

        if current_size + len(text) > MAX_PROMPT_CHARS:
            break

        history.append(text)
        current_size += len(text)
        
    history.reverse()

    context = history[:-SUMMARY_CONTEXT_MESSAGES]
    recent = history[-SUMMARY_CONTEXT_MESSAGES:]

    return (
        "\n".join(context),
        "\n".join(recent),
    )


@bot.event
async def on_ready():

    print("=" * 50)
    print(f"Logged in as: {bot.user}")
    print(f"Bot ID: {bot.user.id}")

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")

    except Exception as e:
        print(e)

    print("=" * 50)


# Slash Commands
@bot.tree.command(name="ask", description="Ask Minh anything.") # Ask

@app_commands.describe(prompt="Your question")

async def ask(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer(thinking=True)
    try:
        response = await asyncio.to_thread(gemini.ask, prompt)
        await send_response(
            interaction,
            response,
        )
    except Exception as e:
        await interaction.followup.send(
            f"Error: {e}"
        )


@bot.tree.command(name="summary", description="Summarize discussion") # Summary
async def summary(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    try:
        context, messages = await get_recent_messages(
            interaction.channel
        )
        summary = await asyncio.to_thread(
            gemini.sumarize,
            context,
            messages,
        )

        print(summary)
        print(type(summary))

        await send_response(
            interaction,
            summary,
        )

    except Exception as e:
        await interaction.followup.send(str(e))


bot.run(DISCORD_TOKEN)