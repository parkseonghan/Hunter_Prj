
#텔레그램 모듈을 가져옵니다.
import telegram

#토큰을 변수에 할당
my_token = '1715990639:AAG-WuMvwaSkvgEwzC29uTNM65JRCb6PjlI'

bot = telegram.Bot(token = my_token)   #bot을 선언합니다.

updates = bot.getUpdates()  #업데이트 내역을 받아옵니다.

for u in updates :   # 내역중 메세지를 출력합니다.
    print(u.message)

#chat_id = bot.getUpdates()[-1].message.chat.id #가장 최근에 온 메세지의 chat id를 가져옵니다

#bot.sendMessage(chat_id = chat_id, text="저는 봇입니다.")