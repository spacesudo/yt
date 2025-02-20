import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.util import antiflood, extract_arguments, quick_markup
from dotenv import load_dotenv
import os
from db import User, Mortage, Referrals
import funcs
from datetime import datetime
import random
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import requests
from telebot.util import quick_markup, antiflood
import random


load_dotenv()

user_data = {}


Token = os.getenv('TOKEN')

bot = telebot.TeleBot(Token, parse_mode='Markdown', disable_web_page_preview=True)

db_user = User()
db_mort = Mortage()
db_ref = Referrals()

db_user.setup()
db_mort.setup()
db_ref.setup()


def abbreviate(x):
    abbreviations = ["", "K", "M", "B", "T", "Qd", "Qn", "Sx", "Sp", "O", "N", 
    "De", "Ud", "DD"]
    
    if x < 1000:
        return str(x)
    
    a = 0
    while x >= 1000 and a < len(abbreviations) - 1:
        x /= 1000.0
        a += 1
    
    return f"{x:.2f} {abbreviations[a]}"


def get_username(user_id):
    try:
        user = bot.get_chat(user_id)
        if user.username:
            return user.username
        else:
            return user.first_name
    except Exception as e:
        print(e)
        return None

@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    print(message.from_user.id)
    messager = message.chat.id
    if str(messager) == "7034272819" or str(messager) == "6219754372":
        send = bot.send_message(message.chat.id,"Enter message to broadcast")
        bot.register_next_step_handler(send,sendall)
        
    else:
        bot.reply_to(message, "You're not allowed to use this command")
        
        
        
def sendall(message):
    users = db_user.get_users()
    for chatid in users:
        try:
            msg = antiflood(bot.send_message, chatid, message.text)
        except Exception as e:
            print(e)
        
    bot.send_message(message.chat.id, "done")
    

@bot.message_handler(commands=['userno'])
def userno(message):
    print(message.from_user.id)
    messager = message.chat.id
    if str(messager) == "7034272819" or str(messager) == "6219754372":
        x = db_user.get_users()
        bot.reply_to(message,f"Total bot users: {len(x)}")
    else:
        bot.reply_to(message, "admin command")


@bot.message_handler(commands=['start'])
def start_(message):
    owner = message.chat.id
    db_user.add_user(owner)
    msg = """We’re thrilled to announce that NeuroFi AI is now live! 🚀 Unlock powerful AI-driven DeFi tools designed to optimize your investments, automate strategies, and provide real-time insights—all within Telegram.

Explore Our Game-Changing Features:
1️⃣ AI-Powered Yield Optimization – Maximize returns with intelligent yield farming strategies.
2️⃣ AI-Agent NFTs – Own, trade, and upgrade AI-powered NFTs that execute DeFi strategies on your behalf.
 3️⃣Agent Evolution Mechanism – Train and enhance AI agents to improve their performance, accuracy, and decision-making over time.

Why NeuroFi AI?
✨ Smarter DeFi Strategies – AI-driven automation for seamless profit optimization.
✨ Data-Backed Decisions – Actionable insights based on deep market analysis.
✨ Effortless Integration – Access all features directly through Telegram with zero complexity.

👉 Join NeuroFi AI today and take your DeFi experience to the next level with AI-powered automation! 🚀
    """
    
    markup = InlineKeyboardMarkup()
    
    btn1 = InlineKeyboardButton('Yield Farming', callback_data='yield')
    btn2 = InlineKeyboardButton('Chart AI', callback_data='chart')
    btn3 = InlineKeyboardButton('Defi Robo Advisory', callback_data='port')
    markup.add(btn1, btn2, btn3)
    photo = open('img.jpg', 'rb')
    bot.send_photo(owner, photo, caption=msg, reply_markup=markup)

def get_yield_opportunities():
    return "🌾 **Today's Yield Farming Opportunities:**\n\n" \
           f"🔹 **Ethereum**: {random.randint(5, 9)}% APY on Yield Farming today\n" \
           f"🔹 **Solana**: {random.randint(3, 7)}% APY on Yield Farming today\n"

@bot.message_handler(commands=['yield'])
def yield_handler(message):
    mark = quick_markup({
        'Solana': {'url': 'https://www.circle.com/circle-mint'},
        'Ethereum': {'url': 'https://www.circle.com/circle-mint'},
        
    })
    mark = InlineKeyboardMarkup()
    b1 = InlineKeyboardButton('Circle Mint', callback_data='i')
    b2 = InlineKeyboardButton('Solana', url='https://www.circle.com/circle-mint')
    b21 = InlineKeyboardButton('Ethereum', url='https://www.circle.com/circle-mint')
    b3 = InlineKeyboardButton('BlazeStake', callback_data='i')
    b4 = InlineKeyboardButton('Solana', url='https://stake.solblaze.org/')
    b5 = InlineKeyboardButton('Etherfi', callback_data='i')
    b6 = InlineKeyboardButton('Ethereum', url = 'https://etherfi.fi')
    mark.add(b1)
    mark.add(b2,b21)
    mark.add(b3)
    mark.add(b4)
    mark.add(b5)
    mark.add(b6)
    bot.send_message(message.chat.id, get_yield_opportunities(), parse_mode="Markdown", reply_markup=mark)

# --- Feature 2: Predictive Market Insights ---
@bot.message_handler(commands=['predict'])
def predict_start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("1️⃣ SOL"), KeyboardButton("2️⃣ ETH"), KeyboardButton("3️⃣ BTC"))
    bot.send_message(message.chat.id, "Select a token:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["1️⃣ SOL", "2️⃣ ETH", "3️⃣ BTC"])
def token_selected(message):
    token_map = {"1️⃣ SOL": "SOL", "2️⃣ ETH": "ETH", "3️⃣ BTC": "BTC"}
    user_data[message.chat.id] = {"token": token_map[message.text]}
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("7 Days"), KeyboardButton("14 Days"), KeyboardButton("30 Days"))
    bot.send_message(message.chat.id, "Send the chart duration:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["7 Days", "14 Days", "30 Days"])
def duration_selected(message):
    user_data[message.chat.id]["duration"] = message.text
    bot.send_message(message.chat.id, "Now send the chart image 📈.")

@bot.message_handler(content_types=['photo'])
def receive_chart(message):
    if message.chat.id not in user_data or "token" not in user_data[message.chat.id]:
        bot.send_message(message.chat.id, "Please start with /predict first.")
        return
    
    token_name = user_data[message.chat.id]["token"]  # Get the selected token (SOL, ETH, BTC)

    print(token_name)
    # Save the image file
    
    bot.send_message(message.chat.id, "Processing chart...")
    
    if token_name == 'ETH':
        url = funcs.get_chart_data('ETH')
        bot.send_photo(
            message.chat.id, url, 
            caption=f"📊 Here is the predicted trend for {token_name} based on chart data."
        )
    
    elif token_name == 'BTC':
        url = funcs.get_chart_data('BTC')
        bot.send_photo(
            message.chat.id, url, 
            caption=f"📊 Here is the predicted trend for {token_name} based on chart data."
        )
        
    elif token_name == 'SOL':
        url = funcs.get_chart_data('SOL')
        bot.send_photo(
            message.chat.id, url, 
            caption=f"📊 Here is the predicted trend for {token_name} based on chart data."
        )

# --- Feature 3: DeFi Robo-Advisory ---
@bot.message_handler(commands=['portfolio'])
def portfolio_start(message):
    bot.send_message(message.chat.id, "Enter the amount to distribute in DeFi investments:")

@bot.message_handler(func=lambda message: message.text.isdigit())
def distribute_portfolio(message):
    amount = int(message.text)
    stable = amount * 0.50
    dex = amount * 0.30
    cex = amount * 0.20

    response = f"💰 **Portfolio Distribution:**\n" \
               f"🔹 **Stablecoins**: ${stable:.2f}\n" \
               f"🔹 **DEX Tokens**: ${dex:.2f}\n" \
               f"🔹 **CEX Tokens**: ${cex:.2f}"
    mark = quick_markup({
        'Portfolio ChatBot' : {'callback_data' : 'chat'}
    })

    bot.send_message(message.chat.id, response, parse_mode="Markdown", reply_markup=mark)

# --- Chatbot for Portfolio Discussions ---
@bot.message_handler(commands=['chatbot'])
def chatbot_start(message):
    bot.send_message(message.chat.id, "Ask me anything about portfolio distribution!")

@bot.message_handler(func=lambda message: message.text)
def chatbot_reply(message):
    owner = message.chat.id
    text = message.text
    #bot.reply_to(message, message.text)
    reply = funcs.chat_bot(text)
    bot.send_message(owner, reply)

@bot.callback_query_handler(func= lambda call: True)
def call_back(call):
    owner = call.message.chat.id
    message = call.message
    
    if call.data == 'yield':
        yield_handler(message)
    
    elif call.data == 'chart':
        predict_start(message)
    elif call.data == 'port':
        portfolio_start(message)
    
    elif call.data == 'chat':
        chatbot_start(message)

# Start the bot
print("Bot is running...")
bot.polling(none_stop=True)
