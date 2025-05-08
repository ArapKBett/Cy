from src.bot.discord_bot import run_discord_bot
from src.bot.telegram_bot import run_telegram_bot
import threading
from src.utils.logger import setup_logger

logger = setup_logger()

def main():
    logger.info("Starting Cybersecurity Job Bot...")
    
    discord_thread = threading.Thread(target=run_discord_bot, daemon=True, name="DiscordBot")
    telegram_thread = threading.Thread(target=run_telegram_bot, daemon=True, name="TelegramBot")
    
    discord_thread.start()
    telegram_thread.start()
    
    try:
        while True:
            if not discord_thread.is_alive():
                logger.error("Discord thread stopped unexpectedly")
                discord_thread = threading.Thread(target=run_discord_bot, daemon=True, name="DiscordBot")
                discord_thread.start()
            if not telegram_thread.is_alive():
                logger.error("Telegram thread stopped unexpectedly")
                telegram_thread = threading.Thread(target=run_telegram_bot, daemon=True, name="TelegramBot")
                telegram_thread.start()
            threading.Event().wait(60)  # Check every minute
    except KeyboardInterrupt:
        logger.info("Shutting down bots...")
        exit(0)
    except Exception as e:
        logger.error(f"Main thread error: {e}")

if __name__ == "__main__":
    main()