# 텔레그램 사용을 위한 import
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler  # import modules

# 파일경로 불러오기 위한 import
import os

my_token = '1715990639:AAG-WuMvwaSkvgEwzC29uTNM65JRCb6PjlI'

print('start telegram chat bot')

# 파일저장경로 설정 ( __file__ : 스크립트 절대경로)
dir_now = os.path.dirname(os.path.abspath(__file__))
# dir_now = os.path.dirname(os.path.abspath("c:\\"))

# 메세지 답장
def get_message(update, context) :
    if update.message.text == "1":
        update.message.reply_text("일")
    if update.message.text == "2":
        update.message.reply_text("이")

#    update.message.reply_text("got text")
#    update.message.reply_text(update.message.text)

# help 답장
def help_command(update, context) :
    print(context)
    update.message.reply_text(f"입력 가능 키워드 1, 2")

# photo 답장
def get_photo(update, context) :
    file_path = os.path.join(dir_now, 'Telegram_Auto_SaveImageFile.png') #파일명
    photo_id = update.message.photo[-1].file_id
    photo_file = context.bot.getFile(photo_id)
    photo_file.download(file_path)
    update.message.reply_text(f'이미지가 자동 저장되었습니다.\n저장경로:{dir_now}')

# file 답장
def get_file(update, context) :
    file_id_short = update.message.document.file_id
    file_url = os.path.join(dir_now, update.message.document.file_name)
    context.bot.getFile(file_id_short).download(file_url)
    update.message.reply_text(f'파일이 자동 저장되었습니다.\n저장경로:{dir_now}')

# Update가 있는지 체크하는 클래스
updater = Updater(my_token, use_context=True)

# 메세지중에서 command 제외
# Filters.text : 텍스트에 대한 응답
message_handler = MessageHandler(Filters.text & (~Filters.command), get_message)

# 입력된 텍스트에 대한 핸들추가
updater.dispatcher.add_handler(message_handler)

# CommandHandler에서 help는 /help에 응답합니다 (Command : 키워드 /, @)
help_handler = CommandHandler('help', help_command)
updater.dispatcher.add_handler(help_handler)

# 전송된 이미지에 대한 핸들추가
photo_handler = MessageHandler(Filters.photo, get_photo)
updater.dispatcher.add_handler(photo_handler)

# 전송된 파일에에 대한 핸들추가
file_handler = MessageHandler(Filters.document, get_file)
updater.dispatcher.add_handler(file_handler)

# polling 시작 (어떠한 상태를 주기적으로 체크해서 조건이 성립되면 송수신의 자료처리 수행)
# timeout=3 폴링에 대한 시간의 최대치로 설정 (낮으면 제대로 수행이 안될 수 있음)
# clean:True 텔레그램 서버에 저장된 업데이트 내역을 삭제.
updater.start_polling(timeout=3, clean=True)

# updater가 계속 수행되도록.
updater.idle()