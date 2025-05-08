from discord import Embed, Colour
from datetime import datetime

def format_discord_embed(job):
    embed = Embed(
        title=job["title"],
        url=job["url"],
        description=f"**Company**: {job['company']}\n**Location**: {job.get('location', 'N/A')}\n**Platform**: {job['platform']}",
        colour=Colour.blue(),
        timestamp=datetime.utcnow()
    )
    embed.set_author(name="Cybersecurity Job Alert 🚨")
    embed.set_footer(text="Stay secure, land your dream job! 🔒")
    return embed

def format_telegram_message(job):
    return (
        "🔒 *New Cybersecurity Job Alert* 🔒\n\n"
        f"📌 *Title*: {job['title']}\n"
        f"🏢 *Company*: {job['company']}\n"
        f"📍 *Location*: {job.get('location', 'N/A')}\n"
        f"🌐 *Platform*: {job['platform']}\n"
        f"🔗 *Apply*: {job['url']}\n\n"
        "🚀 Stay secure, land your dream job!"
    )
