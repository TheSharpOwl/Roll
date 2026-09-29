# Roll
My AI Assistant Bot: a Telegram bot that answers questions about my experience
using a Hugging Face model, hosted on Vercel.

## Live Demo on telegram:
[@RollAssistant_bot](https://t.me/RollAssistant_bot)

## How it works
Telegram sends each message to the Vercel function `api/telegram.py`. The
function sends the question plus the contents of `knowledge/about.md` to a
Hugging Face chat model and replies with the answer.

## Setup
1. Fill in `knowledge/about.md` with the information the bot should know.
2. Create a Hugging Face token (Inference Providers permission) and a Telegram
   bot token (@BotFather).
3. Deploy:
   ```
   npm i -g vercel
   vercel login
   vercel env add HF_TOKEN
   vercel env add TELEGRAM_TOKEN
   vercel env add WEBHOOK_SECRET   # any random string
   vercel env add HF_MODEL         # optional, default meta-llama/Llama-3.1-8B-Instruct
   vercel --prod
   ```
4. Point Telegram at the deployment:
   ```
   curl "https://api.telegram.org/bot<TELEGRAM_TOKEN>/setWebhook" \
     -d url=https://<your-project>.vercel.app/api/telegram \
     -d secret_token=<WEBHOOK_SECRET>
   ```
