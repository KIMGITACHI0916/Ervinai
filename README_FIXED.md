# Fixed Bot Notes

Changes made:
- Validate environment variables at startup (utils/config.py)
- Improved OpenRouter client error handling and key validation (ai_client.py)
- Delete any existing Telegram webhook before starting polling to avoid 'Conflict' errors (bot.py)
- Added a global error handler skeleton to log uncaught handler exceptions (bot.py)

Deployment checklist:
1. Set environment variables in your host (do NOT commit .env to repo):
   - BOT_TOKEN
   - OPENROUTER_API_KEY (must start with sk- or sk-or-)
2. Restart the service.
3. If you prefer webhook mode, remove polling and configure webhook endpoint; ensure no polling instances run.
4. Monitor logs on startup; missing env vars will be reported.

