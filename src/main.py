from src.bot.discord_bot import run_discord_bot
from src.bot.telegram_bot import run_telegram_bot
import threading
from src.utils.logger import setup_logger

logger = setup_logger()

def main():
    logger.info("Starting Cybersecurity Job Bot...")
    
    discord_thread = threading.Thread(target=run_discord_bot, daemon=True)
    telegram_thread = threading.Thread(target=run_telegram_bot, daemon=True)
    
    discord_thread.start()
    telegram_thread.start()
    
    try:
        discord_thread.join()
        telegram_thread.join()
    except KeyboardInterrupt:
        logger.info("Shutting down bots...")
        exit(0)

if __name__ == "__main__":
    main()
