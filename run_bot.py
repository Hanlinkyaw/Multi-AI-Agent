#!/usr/bin/env python3

import os
import asyncio
import signal
import sys
from dotenv import load_dotenv

class TelegramBotRunner:
    def __init__(self):
        load_dotenv()
        self.running = False
        
    async def start_bot(self):
        """Start the Telegram bot."""
        try:
            from src.bot.telegram_bot import TelegramBot
            
            print("🤖 Starting Gemini DevOps Telegram Bot...")
            print(f"📱 Bot: @myassi_opcraw_bot")
            
            bot = TelegramBot()
            self.running = True
            
            # Set up signal handlers
            signal.signal(signal.SIGINT, self.signal_handler)
            signal.signal(signal.SIGTERM, self.signal_handler)
            
            print("🚀 Bot is starting...")
            print("📝 Send /start to begin using the bot")
            print("🔴 Press Ctrl+C to stop the bot")
            
            # Start the bot
            await bot.application.initialize()
            await bot.application.start()
            
            # Start polling
            await bot.application.updater.start_polling(
                drop_pending_updates=True,
                allowed_updates=None
            )
            
            print("✅ Bot is running successfully!")
            
            # Keep running
            while self.running:
                await asyncio.sleep(1)
                
        except Exception as e:
            print(f"❌ Bot error: {e}")
            raise
        finally:
            print("👋 Bot shutting down...")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print(f"\n🛑 Received signal {signum}. Shutting down...")
        self.running = False

async def main():
    """Main entry point."""
    runner = TelegramBotRunner()
    try:
        await runner.start_bot()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Bot startup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
