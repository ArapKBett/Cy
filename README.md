# Cybersecurity Job Bot

A Telegram and Discord bot that scrapes cybersecurity jobs from Indeed, LinkedIn, ZipRecruiter, and more, posting them to designated channels.

## Features
- Scrapes jobs from Indeed, LinkedIn, and ZipRecruiter (global locations).
- Posts rich embeds (Discord) and formatted messages (Telegram).
- Avoids duplicates using a SQLite database.
- Supports commands: `/refresh` (Discord), `/start` and `/refresh` (Telegram).
- Runs every hour to fetch new jobs.

## Setup
1. **Install Python 3.8+** and dependencies:
   ```bash
   pip install -r requirements.txt


## Run
`cd ~/Cy
PYTHONPATH=$PWD python3 src/main.py`