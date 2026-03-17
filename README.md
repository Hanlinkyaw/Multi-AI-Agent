# Gemini-powered Multi-Agent AI Assistant for DevOps

## Project Overview

ဒီပရောဂျက်သည် DevOps engineers အတွက် အထူးရည်ရွယ်ပြီး တည်ဆောက်ထားသော Gemini-powered Multi-Agent AI Assistant ဖြစ်ပါသည်။ Google Gemini AI ကို အခြေခံအားဖြင့် အသုံးပြုပြီး၊ DevOps workflow များကို လွယ်ကူချောမွေ့စေရန် ရည်ရွယ်ပါသည်။

## Current Status

### ✅ Step 1: Project Foundation & Security (Completed)
- Project structure ကို တည်ဆောက်ပြီးပါပြီ
- Security configurations များ ထည့်သွင်းပြီးပါပြီ
- Environment setup ပြင်ဆင်ပြီးပါပြီ
- Core Gemini model integration ပြုလုပ်ပြီးပါပြီ

### ✅ Step 2: Multi-Agent Architecture (Completed)
- Base agent class တည်ဆောက်ပြီးပါပြီ
- Research Agent (web search) တည်ဆောက်ပြီးပါပြီ
- DevOps Agent (Docker, AWS, Linux) တည်ဆောက်ပြီးပါပြီ
- Agent Router (intent detection) တည်ဆောက်ပြီးပါပြီ
- General Agent (fallback) တည်ဆောက်ပြီးပါပြီ

### ✅ Step 4: Telegram Bot Interface (Completed)
- Telegram bot interface တည်ဆောက်ပြီးပါပြီ
- Multi-agent routing integration ပြုလုပ်ပြီးပါပြီ
- Myanmar language support ထည့်သွင်းပြီးပါပြီ
- Command handlers များတည်ဆောက်ပြီးပါပြီ
- Bot startup script တည်ဆောက်ပြီးပါပြီ

## Change Log

### Step 1 - Project Foundation & Security

**Created Files:**
- `src/core/`, `src/agents/`, `src/tools/`, `src/utils/` - Project folder structure
- `.gitignore` - Security: API keys နှင့် sensitive files များကို ignore လုပ်ရန်
- `.env.example` - Environment variables template
- `requirements.txt` - Python dependencies (google-generativeai, python-telegram-bot, python-dotenv, httpx)
- `src/core/model.py` - Gemini model initialization class (2.0 Flash နှင့် 1.5 Flash fallback)
- `main.py` - Entry point နှင့် API connectivity test (Myanmar language support)
- `README.md` - Project documentation

### Step 2 - Multi-Agent Architecture

**Created Files:**
- `src/agents/base_agent.py` - Abstract base class for all agents
- `src/agents/research_agent.py` - Web search and information gathering agent
- `src/agents/devops_agent.py` - DevOps specialized agent (Docker, AWS, Kubernetes, Linux)
- `src/agents/__init__.py` - Agent module initialization
- `src/core/router.py` - Message routing system with intent detection

### Step 3 - DevOps Tools Integration

**Created Files:**
- `src/tools/devops_tools.py` - Safe shell command execution system
- `src/tools/__init__.py` - Tools module initialization

**Updated Files:**
- `src/core/model.py` - Updated to use gemini-1.5-flash only for better free tier reliability
- `src/agents/devops_agent.py` - Integrated command execution capabilities

**Purpose:**
Safe shell command execution system တည်ဆောက်ခြင်း။ DevOps Agent ကို `df -h`, `docker ps` စသော system commands များကို လုံခြုံစွာ execute လုပ်နိုင်အောင် ပြုလုပ်ခြင်း။ Command safety checks နှင့် validation များဖြင့် security ကို ထိန်းချုပ်ခြင်း။

### Step 4 - Telegram Bot Interface

**Created Files:**
- `src/bot/telegram_bot.py` - Main Telegram bot interface
- `src/bot/__init__.py` - Bot module initialization
- `bot_runner.py` - Bot startup script

**Purpose:**
Telegram bot interface တည်ဆောက်ခြင်း။ Multi-agent system ကို Telegram နှင့် ချိတ်ဆက်ခြင်း။ Myanmar language interface ဖြင့် အသုံးပြုနိုင်အောင် ပြုလုပ်ခြင်း။

**Bot Features:**
- 🚀 /start - Bot စတင်ခြင်း
- ❓ /help - အကူအညီရယူခြင်း
- 📊 /status - System status ကြည့်ခြင်း
- 🤖 /agents - Available agents ကြည့်ခြင်း
- 🔧 /devops - DevOps commands များ
- 🔍 /research - Research လုပ်ခြင်း
- 💬 Myanmar language support
- 🤖 Multi-agent routing integration
- ⚡ Real-time message processing

## Next Steps

### Step 5: Advanced Features
- Tavily search API integration
- Agent collaboration mechanisms
- Error handling and logging system
- Performance monitoring and analytics

## Deployment

### 🚀 Deploy to AWS EC2 with Docker

This project includes automated deployment using GitHub Actions to deploy the bot as a Docker container on AWS EC2.

#### Prerequisites

1. **AWS EC2 Instance** with Docker installed
2. **GitHub Repository** with the code
3. **SSH Access** to the EC2 instance

#### Required GitHub Secrets

Set the following secrets in your GitHub repository (Settings → Secrets and variables → Actions):

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `EC2_HOST` | EC2 instance public IP or DNS | `ec2-xx-xx-xx-xx.compute.amazonaws.com` |
| `EC2_USERNAME` | SSH username for EC2 | `ubuntu` or `ec2-user` |
| `EC2_SSH_KEY` | Private SSH key content | `-----BEGIN RSA PRIVATE KEY-----...` |
| `ENV_FILE` | Complete .env file content | `GEMINI_API_KEY=...` |
| `DOCKER_USERNAME` (optional) | Docker Hub username | `yourusername` |
| `DOCKER_PASSWORD` (optional) | Docker Hub password/token | `yourtoken` |

#### Environment Variables

Create a `.env` file in your repository with the following content:

```bash
# Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Telegram Bot Configuration  
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Tavily Search API Configuration
TAVILY_API_KEY=your_tavily_api_key_here
```

⚠️ **Important**: 
- Never commit real API keys to your repository
- Use `ENV_FILE` secret for complete .env content
- The `ENV_FILE` should contain the entire .env file content as a single string

#### Deployment Process

1. **Push to main branch** triggers the GitHub Actions workflow
2. **Build Docker image** on GitHub Actions runner
3. **Transfer to EC2** via SSH
4. **Deploy container** using docker-compose
5. **Health check** verifies deployment

#### Manual Deployment (Alternative)

If you prefer manual deployment:

```bash
# On EC2 instance
sudo apt update && sudo apt install docker.io docker-compose -y
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Clone repository
git clone <your-repo-url>
cd gemini-powered-multi-agent

# Create .env file with your API keys
cp .env.example .env
# Edit .env with real values

# Deploy
docker-compose up -d --build

# Check status
docker-compose ps
docker-compose logs -f
```

#### Monitoring

- **Container Status**: `docker-compose ps`
- **Logs**: `docker-compose logs -f`
- **Health Check**: Automated health checks in docker-compose
- **Restart Policy**: `restart: always` ensures auto-recovery

#### Troubleshooting

1. **Container not starting**: Check logs with `docker-compose logs`
2. **SSH connection failed**: Verify EC2_HOST, EC2_USERNAME, and EC2_SSH_KEY secrets
3. **Build failures**: Check Dockerfile and requirements.txt
4. **Permission denied**: Ensure user has Docker permissions on EC2

#### Security Considerations

- Use SSH key-based authentication (not passwords)
- Restrict SSH access to specific IP addresses if possible
- Regularly update the EC2 instance and Docker
- Use environment variables for sensitive data
- Monitor container logs for unusual activity

## Local Development

### Setup Instructions

1. **Environment Setup:**
   ```bash
   cp .env.example .env
   # .env file ထဲမှာ API keys များဖြည့်စွက်ပါ
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Test:**
   ```bash
   python main.py
   ```

4. **Start Telegram Bot:**
   ```bash
   python run_bot.py
   ```

## Architecture Overview

```
Gemini-powered-Multi-Agent/
├── src/
│   ├── core/           # Core AI model and base classes
│   ├── agents/         # Specialized DevOps agents
│   ├── tools/          # DevOps tool integrations
│   ├── bot/            # Telegram bot interface
│   └── utils/          # Helper utilities
├── main.py            # Entry point
├── bot_runner.py      # Telegram bot startup
├── test_agents.py     # Multi-agent system test
├── requirements.txt   # Dependencies
├── .env.example      # Environment template
└── README.md         # Documentation
```

## Features (Planned)

- 🤖 Multi-agent DevOps assistance
- 🐳 Docker container management
- ☸️ Kubernetes cluster monitoring
- 🔄 CI/CD pipeline automation
- 💬 Telegram bot interface (Myanmar language)
- 🔍 Intelligent search capabilities
- 📊 Real-time monitoring and alerts

---

**Last Updated:** 2026-03-17  
**Current Step:** Step 4 - Telegram Bot Interface ✅  
**Next Step:** Step 5 - Advanced Features
