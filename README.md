# GIF Ranking and Search System

## Overview
This project includes a Flask web application and a Telegram bot for searching and ranking GIFs. The system fetches GIFs from the Giphy API and ranks them based on user interactions such as views and clicks.

## Features
- **Web Application**: Search for GIFs and view rankings based on interactions.
- **Telegram Bot**: Search for GIFs and simulate views, displaying rankings.

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/yourrepository.git
   cd yourrepository
**Set Up the Flask Application**

Create a virtual environment:
python -m venv venv

Activate the virtual environment:
Windows: venv\Scripts\activate
macOS/Linux: source venv/bin/activate

**Install dependencies:**

pip install -r requirements.txt

**Set Up the Telegram Bot**

Replace TELEGRAM_BOT_TOKEN in bot.py with your bot token.


**Run the Flask Application**
python app.py

**Run the Telegram Bot**
python bot.py


**Usage**


# Flask Application

Visit http://localhost:5000 to use the web application.
Use the search form to find GIFs and view rankings.
Telegram Bot
Start the bot with /start.
Search for GIFs with /search <query>.
**Notes**
Ensure you have a valid Giphy API key and replace API_KEY in both app.py and bot.py.
The gif_views dictionary in bot.py simulates view counts and should be replaced with real interaction data