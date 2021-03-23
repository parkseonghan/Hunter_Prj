
#텔레그램 모듈을 가져옵니다.
import telegram

#토큰을 변수에 할당
my_token = '1715990639:AAG-WuMvwaSkvgEwzC29uTNM65JRCb6PjlI'

#bot 선언
bot = telegram.Bot(token = my_token)

#업데이트 내역을 받아옵니다.
#updates = bot.getUpdates()

#내역중 메세지를 출력합니다.
#for u in updates:
#    print(u.message)

#가장 최근에 온 메세지의 chat id를 할당
chat_id = bot.getUpdates()[-1].message.chat.id

bot.sendMessage(chat_id = chat_id, text="할로")