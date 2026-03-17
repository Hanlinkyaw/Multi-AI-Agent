import os
import asyncio
import logging
from typing import Dict, Any, Optional
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from src.core.router import AgentRouter

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBot:
    """
    Telegram Bot interface for Gemini-powered Multi-Agent AI Assistant.
    Myanmar language support with multi-agent routing.
    """
    
    def __init__(self):
        """Initialize the Telegram bot."""
        load_dotenv()
        
        # Get Telegram bot token
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN is required")
        
        # Initialize agent router
        self.router = AgentRouter()
        
        # Bot configuration
        self.bot_commands = [
            BotCommand("start", "🚀 Bot ကို စတင်ခြင်း"),
            BotCommand("help", "❓ အကူအညီရယူခြင်း"),
            BotCommand("status", "📊 System status ကြည့်ခြင်း"),
            BotCommand("agents", "🤖 Available agents များကြည့်ခြင်း"),
            BotCommand("devops", "🔧 DevOps commands များ"),
            BotCommand("research", "🔍 Research လုပ်ခြင်း")
        ]
        
        # Initialize application
        self.application = Application.builder().token(self.token).build()
        
        # Setup handlers
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup command and message handlers."""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CommandHandler("agents", self.agents_command))
        self.application.add_handler(CommandHandler("devops", self.devops_command))
        self.application.add_handler(CommandHandler("research", self.research_command))
        
        # Message handler for text messages
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        welcome_message = """
🤖 **Gemini DevOps Assistant မှ ကြိုဆိုပါသည်!**

ကျွန်ုပ်သည် DevOps engineers အတွက် အထူးရည်ရွယ်ပြီး တည်ဆောက်ထားသော Multi-Agent AI Assistant ဖြစ်ပါသည်။

🔥 **အဓိကလုပ်ဆောင်ချက်များ:**
- 🐳 Docker container management
- ☸️ Kubernetes monitoring
- 🖥️ System administration
- 🔍 Web research & information
- 💬 Myanmar language support

📝 **အသုံးပြုရန်:**
မည်သည့် message ကိုမဆို ရိုက်ထည့်ပါ။ ကျွန်ုပ်က သင့်လိုအပ်သော agent ကို ရွေးချယ်ပေးပါမည်။

/help - အကူအညီရယူရန်
/status - System status ကြည့်ရန်
/agents - Available agents များကြည့်ရန်

စတင်ပြောဆိုလိုက်ပါ! 🚀
        """
        
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        help_message = """
❓ **အကူအညီ - Help**

🤖 **Available Commands:**
/start - Bot ကို စတင်ခြင်း
/help - ဤအကူအညီစာမျက်နှာ
/status - System status စစ်ဆေးခြင်း
/agents - Available agents များကြည့်ခြင်း
/devops - DevOps commands များ
/research - Research လုပ်ခြင်း

💬 **Message Examples:**
- "docker ps ကို လုပ်ပေးပါ"
- "system status ကို စစ်ဆေးပေးပါ"
- "လောလောဆယ်သတင်းများကို ရှာပေးပါ"
- "run df -h"

🔧 **DevOps Agent လုပ်နိုင်သောအရာများ:**
- Docker commands (docker ps, docker images, etc.)
- System monitoring (df -h, free -h, etc.)
- Linux commands
- Infrastructure management

🔍 **Research Agent လုပ်နိုင်သောအရာများ:**
- Web search
- Information gathering
- Documentation lookup
- Latest news & updates

မေးခွန်းများရှိပါက မေးမြန်းလိုက်ပါ! 🚀
        """
        
        await update.message.reply_text(help_message, parse_mode='Markdown')
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command."""
        try:
            # Get system status using DevOps agent
            result = self.router.route_message("system status ကို စစ်ဆေးပေးပါ")
            
            if result['success']:
                status_message = f"""
📊 **System Status**

🤖 **Agent:** {result['agent']}
🧠 **Model:** {result['model']}

{result['response']}
                """
            else:
                status_message = f"❌ Status check failed: {result['error']}"
            
            await update.message.reply_text(status_message, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def agents_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /agents command."""
        try:
            status = self.router.get_agent_status()
            
            agents_message = """
🤖 **Available Agents**

"""
            
            for agent_type, agent_info in status['agents'].items():
                agents_message += f"""
**{agent_info['name']}**
- Type: {agent_type}
- Model: {agent_info['model']}
"""
            
            agents_message += f"\n📊 **Total Agents:** {status['total_agents']}"
            
            await update.message.reply_text(agents_message, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def devops_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /devops command."""
        devops_message = """
🔧 **DevOps Commands**

အောက်ပါ commands များကို စမ်းကြည့်နိုင်ပါသည်:

📋 **System Commands:**
- "run df -h" - Disk usage ကြည့်ရန်
- "run free -h" - Memory usage ကြည့်ရန်
- "run docker ps" - Running containers ကြည့်ရန်
- "run docker images" - Docker images ကြည့်ရန်

🔍 **System Status:**
- "system status" - Full system status
- "server information" - Server details
- "disk space" - Disk usage only

⚠️ **Safety Notice:**
ဘေးအန္တရာယ်ကင်းရှင်းသော commands များကိုသာ execute လုပ်ပါသည်။

လိုအပ်သော command ကို ရိုက်ထည့်ပါ! 🚀
        """
        
        await update.message.reply_text(devops_message, parse_mode='Markdown')
    
    async def research_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /research command."""
        research_message = """
🔍 **Research Agent**

Research Agent သည် အောက်ပါအရာများကို လုပ်ဆောင်နိုင်ပါသည်:

📰 **Information Gathering:**
- "လောလောဆယ်သတင်းများကို ရှာပေးပါ"
- "latest DevOps news ကို ရှာပေးပါ"
- "Docker အကြောင်း documentation ရှာပေးပါ"

🔍 **Search Examples:**
- "Kubernetes best practices ရှာပေးပါ"
- "AWS နေရာတွင် server setup လုပ်နည်း"
- "Linux commands အကြောင်း ရှာပေးပါ"

📚 **Documentation:**
- Technical documentation lookup
- Tutorial search
- Best practices research

ရှာဖွေလိုသောအကြောင်းအရာကို ရိုက်ထည့်ပါ! 🔍
        """
        
        await update.message.reply_text(research_message, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages."""
        try:
            user_message = update.message.text
            user_id = update.effective_user.id
            
            logger.info(f"User {user_id}: {user_message}")
            
            # Show typing indicator
            await context.bot.send_chat_action(
                chat_id=update.effective_chat.id, 
                action="typing"
            )
            
            # Route message to appropriate agent
            result = self.router.route_message(user_message)
            
            if result['success']:
                response = f"""
🤖 **{result['agent']}**

{result['response']}
                """
                
                await update.message.reply_text(response, parse_mode='Markdown')
            else:
                error_message = f"""
❌ **Error Occurred**

{result.get('error', 'Unknown error')}

ကျေးဇူးပြုပြီး ပြန်လည်ကြိုးစားကြည့်ပါ။
                """
                
                await update.message.reply_text(error_message, parse_mode='Markdown')
                
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await update.message.reply_text("❌ တစ်ခုခုမှားယွင်းနေပါသည်။ ပြန်လည်ကြိုးစားကြည့်ပါ။")
    
    async def set_bot_commands(self):
        """Set bot commands."""
        await self.application.bot.set_my_commands(self.bot_commands)
        logger.info("Bot commands set successfully")
    
    def run(self):
        """Run the bot."""
        print("🤖 Starting Telegram Bot...")
        print(f"📱 Bot Token: {self.token[:10]}...")
        
        # Set bot commands
        asyncio.run(self.set_bot_commands())
        
        # Start the bot
        print("🚀 Bot is running...")
        print("📝 Send /start to begin using the bot")
        
        self.application.run_polling(
            drop_pending_updates=True,
            allowed_updates=Update.ALL_TYPES
        )

def main():
    """Main function to run the Telegram bot."""
    try:
        bot = TelegramBot()
        bot.run()
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        print(f"❌ Bot startup failed: {e}")

if __name__ == "__main__":
    main()
