import os
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TOKEN = os.environ.get("8954121053:AAFrDuNqprFnZfiNVfWsTiWOsPKInspoA3E")

def calculate_bet(text):
    text = text.strip().lower()
    
    # ဒဲ့ ( - ) ဥပမာ - 12-500
    if '-' in text and 'r' not in text:
        parts = text.split('-')
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            num = parts[0].strip()
            amt = int(parts[1].strip())
            return [num], amt, 1
    
    # R အာ (ဥပမာ - 12r500)
    r_match = re.match(r'(\d+)r(\d+)', text)
    if r_match:
        num = r_match.group(1)
        amt = int(r_match.group(2))
        if len(num) == 2:
            rev = num[1] + num[0]
            return [num, rev], amt, 2
        return [num], amt, 1
    
    # ပတ် (ဥပမာ - 9ပတ်1000)
    if 'ပတ်' in text:
        match = re.match(r'(\d+)ပတ်(\d+)', text)
        if match:
            num = int(match.group(1))
            amt = int(match.group(2))
            numbers = [f"{num}{i}" for i in range(10)]
            return numbers, amt, 19
    
    # ထိပ် (ဥပမာ - 2ထိပ်500)
    if 'ထိပ်' in text:
        match = re.match(r'(\d+)ထိပ်(\d+)', text)
        if match:
            num = int(match.group(1))
            amt = int(match.group(2))
            numbers = [f"{num}{i}" for i in range(10)]
            return numbers, amt, 10
    
    # အပူး (ဥပမာ - အပူး500)
    if 'အပူး' in text or 'ပူး' in text:
        match = re.search(r'(\d+)$', text)
        if match:
            amt = int(match.group(1))
            numbers = [f"{i}{i}" for i in range(10)]
            return numbers, amt, 10
    
    # ပုံမှန်တစ်ကွက် (ဥပမာ - 12 500)
    parts = text.split()
    if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
        return [parts[0]], int(parts[1]), 1
    
    return None, 0, 0

async def start(update, context):
    await update.message.reply_text("""🎰 2D Betting Bot ကို ကြိုဆိုပါတယ်။

ထိုးနည်းပုံစံများ:
• 12-500 (တစ်ကွက်)
• 12r500 (12 နဲ့ 21 နှစ်ကွက်)
• 9ပတ်1000 (ဂဏန်း 19 ကွက်)
• 2ထိပ်500 (ဂဏန်း 10 ကွက်)
• အပူး500 (ဂဏန်း 10 ကွက်)

ကံကောင်းပါစေ 🍀""")

async def handle_message(update, context):
    user = update.effective_user.first_name
    text = update.message.text
    
    numbers, amt, combos = calculate_bet(text)
    
    if numbers is None:
        await update.message.reply_text("ပုံစံမှားနေပါတယ်။\n\nဥပမာများ:\n12-500\n12r500\n9ပတ်1000\n2ထိပ်500\nအပူး500")
        return
    
    total = amt * combos
    cashback = (total * 7) // 100
    final = total - cashback
    
    reply = f"""👤 {user}
Mega Total = {total} ကျပ်
7% Cash Back = {cashback} ကျပ်
Total = {final} ကျပ် ဘဲ လွဲပါရှင်
ကံကောင်းပါစေ 🧸🍀"""
    
    await update.message.reply_text(reply)

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()
