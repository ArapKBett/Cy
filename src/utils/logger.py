import logging
import os

def setup_logger():
    logger = logging.getLogger("CyberJobBot")
    logger.setLevel(logging.INFO)
    
    os.makedirs("logs", exist_ok=True)
    
    file_handler = logging.FileHandler("logs/bot.log")
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ))
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    ))
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
