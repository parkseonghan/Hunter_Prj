from telegram.ext import Updater, MessageHandler, Filters

# 토큰을 통해 updater를 만들고 handler을 추가해주는 방식
api_key = '1592049270:AAEUp0Qwnqn2UmXRDFWlfXfELZDEFr5xss0'


# handler(dispatcher가 받아오면 handling함)
def get_message(update, context):
    text = update.message.text

    if "1" in text:
        update.message.reply_text("1. 반품문의를 선택하셨습니다.")
    elif "2" in text:
        update.message.reply_text("2. 교환문의를 선택하셨습니다.")
    elif "3" in text:
        update.message.reply_text("3. 배송문의를 선택하셨습니다.")
    elif "4" in text:
        update.message.reply_text("4. 기타문의를 선택하셨습니다.")
    else:
        update.message.reply_text("다시 입력해주세요")


# updater --> 봇 업데이트 사항이 있으면 가져오는 클래스
updater = Updater(api_key, use_context=True)

# 메세지(텍스트)에 대한 핸들러 --> (Filters.text:텍스트에 응답, get_message함수 호출)
message_handler = MessageHandler(Filters.text, get_message)
updater.dispatcher.add_handler(message_handler)

# polling 방식: 주기적으로 텔레그램 서버에 접속해서 새로운 메세지가 있으면 받아옴
# timeout은 polling에 걸리는 시간의 최대치
# clean은 deprecated --> drop_pending_updates로 서버에 저장되어 있던 업데이트 내용 삭제
updater.start_polling(timeout=3, drop_pending_updates=True)  # drop_pending_updates=True : to drop all pending updates

# updater가 종료되지 않고 계속 실행되도록 하는 함수
updater.idle()
