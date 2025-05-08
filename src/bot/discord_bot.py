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
        logger.info("Starting Discord job posting task")
        try:
            self.post_jobs.start()
            logger.info("Discord post_jobs task started")
            await self.post_jobs()  # Run immediately
            logger.info("Initial Discord post_jobs run completed")
        except Exception as e:
            logger.error(f"Error in setup_hook: {e}", exc_info=True)
    
    async def on_ready(self):
        logger.info(f"Discord bot {self.user} is ready!")
        logger.info(f"Connected to guilds: {[guild.name for guild in self.guilds]}")
        channel = self.get_channel(DISCORD_CHANNEL_ID)
        logger.info(f"Channel {DISCORD_CHANNEL_ID} found: {channel}")
        if channel:
            permissions = channel.permissions_for(channel.guild.me)
            logger.info(f"Bot permissions in channel {DISCORD_CHANNEL_ID}: {permissions}")
            logger.info(f"Send Messages: {permissions.send_messages}, Embed Links: {permissions.embed_links}")
            if not permissions.send_messages or not permissions.embed_links:
                logger.error("Bot lacks Send Messages or Embed Links permissions in channel")
    
    @tasks.loop(hours=1)
    async def post_jobs(self):
        logger.info("Starting Discord post_jobs")
        channel = self.get_channel(DISCORD_CHANNEL_ID)
        if not channel:
            logger.error("Discord channel not found!")
            return
        
        try:
            jobs = []
            try:
                indeed_jobs = scrape_indeed_jobs()
                logger.info(f"Scraped {len(indeed_jobs)} jobs from Indeed")
                jobs.extend(indeed_jobs)
            except Exception as e:
                logger.error(f"Failed to scrape Indeed: {e}")
            
            try:
                linkedin_jobs = scrape_linkedin_jobs()
                logger.info(f"Scraped {len(linkedin_jobs)} jobs from LinkedIn")
                jobs.extend(linkedin_jobs)
            except Exception as e:
                logger.error(f"Failed to scrape LinkedIn: {e}")
            
            try:
                ziprecruiter_jobs = scrape_ziprecruiter_jobs()
                logger.info(f"Scraped {len(ziprecruiter_jobs)} jobs from ZipRecruiter")
                jobs.extend(ziprecruiter_jobs)
            except Exception as e:
                logger.error(f"Failed to scrape ZipRecruiter: {e}")
            
            if not jobs:
                logger.warning("No jobs scraped from any platform")
                return
            
            for job in jobs:
                if not self.db.job_exists(job["id"]):
                    embed = format_discord_embed(job)
                    logger.info(f"Sending job to Discord: {job['title']}")
                    await channel.send(embed=embed)
                    self.db.add_job(job["id"], job["title"], job["company"], job["url"], job["platform"])
                    logger.info(f"Posted job to Discord: {job['title']}")
                else:
                    logger.info(f"Skipping duplicate job: {job['title']}")
        except Exception as e:
            logger.error(f"Error in Discord post_jobs: {e}", exc_info=True)
    
    @commands.command()
    async def refresh(self, ctx):
        await ctx.send("🔄 Fetching new cybersecurity jobs... Please wait!")
        try:
            await self.post_jobs()
            await ctx.send("✅ Job refresh complete! Check the channel for new postings. 🚀")
        except Exception as e:
            await ctx.send("❌ Error refreshing jobs. Check logs.")
            logger.error(f"Error in refresh command: {e}", exc_info=True)

def run_discord_bot():
    try:
        bot = CyberJobBot()
        bot.run(DISCORD_TOKEN, reconnect=True, max_messages=1000)
    except Exception as e:
        logger.error(f"Discord bot crashed: {e}", exc_info=True)