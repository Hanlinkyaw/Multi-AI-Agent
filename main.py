import os
from dotenv import load_dotenv
from src.core.model import GeminiModel

def main():
    # Load environment variables
    load_dotenv()
    
    # Check required environment variables
    required_vars = ["GEMINI_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ အရေးကြီးသော environment variables များ မရှိပါ: {', '.join(missing_vars)}")
        print("ကျေးဇူးပြုပြီး .env.example ကို .env အဖြစ် copy ပြုလုပ်ပြီး API keys များဖြည့်စွက်ပါ။")
        return
    
    try:
        # Initialize Gemini model
        print("🤖 Gemini Model ကို initialize လုပ်နေပါသည်...")
        gemini = GeminiModel()
        
        print(f"✅ {gemini.get_model_name()} ကို အောင်မြင်စွာ initialize လုပ်ပြီးပါပြီ")
        
        # Test API connectivity with Myanmar language
        print("🔍 API connectivity ကို စမ်းသပ်နေပါသည်...")
        test_prompt = "မင်္ဂလာပါ။ ကျွန်ုပ်တို့၏ DevOps Assistant ကို စတင်တည်ဆောက်နေပါသည်။"
        
        response = gemini.generate_response(test_prompt)
        
        print("🎉 Gemini API ကို အောင်မြင်စွာချိတ်ဆက်နိုင်ပါပြီ!")
        print(f"📝 Test Response: {response[:100]}...")
        print("🚀 Gemini-powered Multi-Agent AI Assistant အတွက် အခြေခံ အဆောက်အအုံ အောင်မြင်ပါသည်!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("API key ကို စစ်ဆေးပြီး internet connection ရှိမရှိ စစ်ဆေးပါ။")

if __name__ == "__main__":
    main()
