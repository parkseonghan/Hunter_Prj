import telegram

api_key = '1761478694:AAGxcdmuFKv92evUb6VwxY2TRPaf9MXLlFY'

bot = telegram.Bot(token=api_key)

chat_id = bot.get_updates()[-1].message.chat_id
# 978800864

print(chat_id)

bot.sendMessage(chat_id=chat_id, text='hi')