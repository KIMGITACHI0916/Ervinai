# Private AI Coding & Modding Bot (Railway Ready)

This repository is a starter template for a **private Telegram bot** that:
- Accepts large files (100-500MB) via Telegram DM
- Processes files locally (modding logic you provide)
- Uses an uncensored AI backend (OpenRouter / Nous Hermes) for natural-language tasks
- Designed for deployment on Railway or similar

**Important:** This project contains placeholders for AI/model usage and modding logic. Replace API keys in Railway environment variables.

## Files & Structure
See repository layout for details.

## Deploy on Railway
1. Push this repo to GitHub.
2. Create a Railway project -> Deploy from GitHub.
3. Set environment variables on Railway:
   - `BOT_TOKEN` (Telegram bot token)
   - `OPENROUTER_API_KEY` (OpenRouter API key)
   - `MAX_FILE_MB` (optional)
4. Deploy. Railway will run `python bot.py` by default (Procfile included).

