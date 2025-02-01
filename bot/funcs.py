import requests
import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv('OPEN_AI')

def get_chart_data(chain, studies=None, interval="4h", theme="dark"):
    url = "https://api.chart-img.com/v1/tradingview/advanced-chart/storage"
    
    api_key = "vnDrOf3wlruCCHf4b0jy8hcdqwYzjHc5MBQww6Ad"
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    symbol= f"BINANCE:{chain}USDT"
    params = {
        "symbol": symbol,
        "studies": studies or ["MACD", "CCI:10,close"],
        "interval": interval,
        "theme": theme
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()['url']
    else:
        return {"error": response.status_code, "message": response.text}



# Global variable to store conversation history
conversation_history = [
    {
        'role': 'system',
        'content': "You're a crypto portfolio and investment advisor bot only"
    }
]

def chat_bot(prompt):
    global conversation_history
    openai.api_key = openai_api_key
    
    if prompt:
        # Append user's prompt to the conversation history
        conversation_history.append({
            "role": "user",
            "content": prompt
        })
        
        # Generate a response from the bot
        chat = openai.chat.completions.create(
            model='gpt-4',
            messages=conversation_history
        )
        
        reply = chat.choices[0].message.content
        
        # Append the assistant's reply to the conversation history
        conversation_history.append({
            "role": "assistant",
            "content": reply
        })
        
        return reply