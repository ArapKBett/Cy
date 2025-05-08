from telegram.ext import Application, CommandHandler
from src.utils.config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from src.utils.logger import setup_logger
from src.utils.database import JobDatabase
from src.utils.formatter import format_telegram_message
from src.api.indeed import scrape_indeed_jobs
from src.api.linkedin import scrape_linkedin_jobs
from src.api.other_platforms import scrape_ziprecruiter_jobs
import asyncio
import schedule

logger = setup_logger()

class CyberJobBot:
    def __init__(self):
        try:
            self.app = Application.builder().token(TELEGRAM_TOKEN).build()
            self.db = JobDatabase()
            self.setup_handlers()
            logger.info("Telegram bot initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Telegram bot: {e}")
            raise
    
    def setup_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("refresh", self.refresh))
    
    async def start(self, update, context):
        await update.message.reply_text(
            "👋 Welcome to the Cybersecurity Job Bot! 🚨\n"
            "I'll post new cybersecurity jobs every hour. Use /refresh to fetch jobs now!"
        )
    
    async def refresh(self, update, context):
        await update.message.reply_text("🔄 Fetching new cybersecurity jobs... Please wait!")
        await self.post_jobs()
        await update.message.reply_text("✅ Job refresh complete! Check the channel for new postings. 🚀")
    
    async def post_jobs(self):
        logger.info("Starting Telegram post_jobs")
        try:
            jobs = []
            jobs.extend(scrape_indeed_jobs())
            jobs.extend(scrape_linkedin_jobs())
            jobs.extend(scrape_ziprecruiter_jobs())
            
            for job in jobs:
                if not self.db.job_exists(job["id"]):
                    message = format_telegram_message(job)
                    await self.app.bot.send_message(
                        chat_id=TELEGRAM_CHAT_ID,
                        text=message,
                        parse_mode="Markdown"
                    )
                    self.db.add_job(job["id"], job["title"], job["company"], job["url"], job["platform"])
                    logger.info(f"Posted job to Telegram: {job['title']}")
        except Exception as e:
            logger.error(f"Error in Telegram post_jobs: {e}")
    
    async def schedule_jobs(self):
        logger.info("Starting Telegram job scheduler")
        schedule.every(1).hours.do(lambda: asyncio.create_task(self.post_jobs()))
        await self.post_jobs()  # Run immediately on startup
        while True:
            schedule.run_pending()
            await asyncio.sleep(1)
    
    async def run(self):
        try:
            await self.app.initialize()
            await self.app.start()
            await self.app.updater.start_polling()
            logger.info("Telegram bot polling started")
            await self.schedule_jobs()
        except Exception as e:
            logger.error(f"Error in Telegram run: {e}")
        finally:
            await self.app.updater.stop()
            await self.app.stop()
            await self.app.shutdown()
    
    def start(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.run())
        except Exception as e:
            logger.error(f"Telegram bot crashed: {e}")
        finally:
            loop.close()

def run_telegram_bot():
    try:
        bot = CyberJobBot()
        bot.start()
    except Exception as e:
        logger.error(f"Telegram bot thread crashed: {e}")