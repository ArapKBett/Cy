import discord
from discord.ext import commands, tasks
from src.utils.config import DISCORD_TOKEN, DISCORD_CHANNEL_ID
from src.utils.logger import setup_logger
from src.utils.database import JobDatabase
from src.utils.formatter import format_discord_embed
from src.api.indeed import scrape_indeed_jobs
from src.api.linkedin import scrape_linkedin_jobs
from src.api.other_platforms import scrape_ziprecruiter_jobs

logger = setup_logger()

class CyberJobBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="/", intents=intents)
        self.db = JobDatabase()
    
    async def setup_hook(self):
        self.post_jobs.start()
    
    async def on_ready(self):
        logger.info(f"Discord bot {self.user} is ready!")
    
    @tasks.loop(hours=1)
    async def post_jobs(self):
        channel = self.get_channel(DISCORD_CHANNEL_ID)
        if not channel:
            logger.error("Discord channel not found!")
            return
        
        jobs = []
        jobs.extend(scrape_indeed_jobs())
        jobs.extend(scrape_linkedin_jobs())
        jobs.extend(scrape_ziprecruiter_jobs())
        
        for job in jobs:
            if not self.db.job_exists(job["id"]):
                embed = format_discord_embed(job)
                await channel.send(embed=embed)
                self.db.add_job(job["id"], job["title"], job["company"], job["url"], job["platform"])
                logger.info(f"Posted job to Discord: {job['title']}")
    
    @commands.command()
    async def refresh(self, ctx):
        await ctx.send("🔄 Fetching new cybersecurity jobs... Please wait!")
        await self.post_jobs()
        await ctx.send("✅ Job refresh complete! Check the channel for new postings. 🚀")

def run_discord_bot():
    bot = CyberJobBot()
    bot.run(DISCORD_TOKEN)
