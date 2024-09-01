import aiohttp
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

API_KEY = 'KHZ9nMOb8Ukyp7vnwwYuszqsG4jePJzQ'
GIPHY_URL = 'https://api.giphy.com/v1/gifs/search'
TELEGRAM_BOT_TOKEN = '7026963493:AAG7DAafA7zjcX7ZNzLjXeYi-v6xqlQgajA'

gif_views = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Welcome! Use /search <query> to search for GIFs.')

async def search_gif(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = ' '.join(context.args)
    if not query:
        await update.message.reply_text('Please provide a search query.')
        return

    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
            async with session.get(GIPHY_URL, params={
                'api_key': API_KEY,
                'q': query,
                'limit': 5
            }) as response:
                if response.status == 200:
                    data = await response.json()
                    if data['data']:
                        gifs = data['data']
                        for gif in gifs:
                            gif_url = gif['images']['original']['url']
                            gif_id = gif['id']
                            
                            # Simulate viewing and ranking
                            gif_views[gif_id] = gif_views.get(gif_id, 0) + 1
                            
                            await update.message.reply_animation(gif_url)
                            await update.message.reply_text(f"Views: {gif_views[gif_id]}")
                    else:
                        await update.message.reply_text('No GIFs found for your query.')
                else:
                    await update.message.reply_text('Failed to fetch GIFs. Please try again later.')
    except aiohttp.ClientError as e:
        await update.message.reply_text(f'An error occurred: {e}')

def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('search', search_gif))
    application.run_polling()

if __name__ == '__main__':
    main()
