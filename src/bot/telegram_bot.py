from telegram.ext import Application, CommandHandler
from src.utils.config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from src.utils.logger import setup_logger
from src.utils.database import JobDatabase
from src.utils.formatter import format_telegram_message
from src.api.indeed import scrape_indeed_jobs
from src.api.linkedin import scrape_linkesin_jobs
from src.api.other_platforms import scrape_ziprecruiter_jobs
import schedule
import asyncio
import threading

logger = setup_logger()

class CyberJobBot:
    def __init__(self):
        self.app = Application.builder().token(TELEGRAM_TOKEN).build()
        self.db = JobDatabase()
        self.setup_handlers()
    
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
    
    def schedule_jobs(self):
        schedule.every(1).hours.do(lambda: asyncio.run(self.post_jobs()))
        while True:
            schedule.run_pending()
    
    def run(self):
        threading.Thread(target=self.schedule_jobs, daemon=True).start()
        self.app.run_polling()

def run_telegram_bot():
    bot = CyberJobBot()
    bot.run()
