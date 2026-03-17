#!/usr/bin/env python3

import os
import asyncio
from dotenv import load_dotenv

async def test_bot():
    """Simple bot test."""
    load_dotenv()
    
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN not found")
        return
    
    print("🤖 Testing Telegram Bot...")
    print(f"📱 Token: {token[:10]}...")
    
    try:
        from telegram import Bot
        from telegram.ext import Application
        
        # Test basic bot connection
        bot = Bot(token=token)
        bot_info = await bot.get_me()
        
        print(f"✅ Bot connected successfully!")
        print(f"🤖 Bot Name: {bot_info.first_name}")
        print(f"🆔 Bot Username: @{bot_info.username}")
        
        # Test application
        app = Application.builder().token(token).build()
        await app.initialize()
        print("✅ Application initialized successfully!")
        
        await app.shutdown()
        print("✅ Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_bot())
