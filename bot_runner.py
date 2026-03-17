#!/usr/bin/env python3

import os
import sys
import asyncio
from dotenv import load_dotenv

async def main():
    """Main function to run the Telegram bot."""
    
    # Load environment variables
    load_dotenv()
    
    # Check required environment variables
    required_vars = ["TELEGRAM_BOT_TOKEN", "GEMINI_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file")
        sys.exit(1)
    
    print("🤖 Starting Gemini DevOps Telegram Bot...")
    print(f"📱 Telegram Bot Token: {os.getenv('TELEGRAM_BOT_TOKEN')[:10]}...")
    print(f"🧠 Gemini API Key: {os.getenv('GEMINI_API_KEY')[:10]}...")
    
    try:
        # Import and run the bot
        from src.bot.telegram_bot import TelegramBot
        
        bot = TelegramBot()
        await bot.set_bot_commands()
        
        print("🚀 Bot is running...")
        print("📝 Send /start to begin using the bot")
        
        # Run the bot with proper async handling
        await bot.application.initialize()
        await bot.application.start()
        await bot.application.updater.start_polling(
            drop_pending_updates=True,
            allowed_updates=None
        )
        
        # Keep the bot running
        print("✅ Bot is running successfully!")
        print("🔴 Press Ctrl+C to stop the bot")
        
        # Wait for shutdown
        await bot.application.updater.running
        
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
        await bot.application.updater.stop()
        await bot.application.stop()
        await bot.application.shutdown()
    except Exception as e:
        print(f"❌ Bot error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Bot startup failed: {e}")
        sys.exit(1)
