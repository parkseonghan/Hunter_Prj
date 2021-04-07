from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import inc_file.dbconn as db_con
import telegram
import os
import datetime


api_key = '1761478694:AAGxcdmuFKv92evUb6VwxY2TRPaf9MXLlFY'

bot = telegram.Bot(token=api_key)

chat_id = 978800864

cur_dir = os.path.dirname(os.path.abspath(__file__))  # D:\4.dev\Python\PythonProject\Serena

db = db_con.Db_conn()

# get_message FLAG
msg: bool = False

# Init Message
bot.sendMessage(chat_id=chat_id, text="진료예약 시작을 위해 입력창에 /help를 입력해주세요")


# ==== FUNCTION ==== #
# Create Button Menu
def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols]
            for i in range(0, len(buttons), n_cols)]  # range(start, stoop, step), 2차원배열

    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


# Make Button List
def build_button(text_list, callback_header=""):  # make button list
    button_list = []
    text_header = callback_header

    if callback_header != "":
        text_header += ", "

    for text in text_list:
        button_list.append(InlineKeyboardButton(text, callback_data=text_header + text))

    return button_list


# Help Command
# https://blog.psangwoo.com/coding/2018/08/20/python-telegram-bot-4.html
def help_command(update, context):
    button_list = [InlineKeyboardButton("1. 김ㅇㅇ", callback_data="김ㅇㅇ"),
                   InlineKeyboardButton("2. 박ㅇㅇ", callback_data="박ㅇㅇ"),
                   InlineKeyboardButton("3. 이ㅇㅇ", callback_data="이ㅇㅇ"),
                   InlineKeyboardButton("4. 기타문의", callback_data="기타문의")]
    show_markup = InlineKeyboardMarkup(build_menu(button_list, len(button_list) - 1))  # make markup
    # show_markup = InlineKeyboardMarkup(button_list)

    update.message.reply_text("예약을 원하시는 의사 선생님을 선택해주세요.", reply_markup=show_markup)


# Button Callbacks
def callback_help(update, context):
    data_selected = update.callback_query.data
    print("callback: " + data_selected)  # 1, 2, 3, 4

    # Cancel
    if data_selected.find("cancel") != -1:
        context.bot.edit_message_text(text="취소하였습니다.",
                                      chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id)
        return

    # 1st Selection
    if len(data_selected.split(",")) == 1:
        print("len1")
        date1 = str(datetime.date.today() + datetime.timedelta(days=1))
        date2 = str(datetime.date.today() + datetime.timedelta(days=2))
        date3 = str(datetime.date.today() + datetime.timedelta(days=3))
        date4 = str(datetime.date.today() + datetime.timedelta(days=4))
        date5 = str(datetime.date.today() + datetime.timedelta(days=5))

        # BTN1
        if data_selected == "김ㅇㅇ":
            button_list = build_button([date1, date2, date3, "cancel"], data_selected)
            text = "{0}이(가 선택되었습니다.\n 예약 가능한 날짜 중 원하는 날짜를 선택해주세요.".format("1. 김ㅇㅇ")
            edit_msg(context, update, button_list, len(button_list) - 1, text)

        # BTN2
        elif data_selected == "박ㅇㅇ":
            button_list = build_button([date2, date3, date4, date5, "cancel"], data_selected)
            text = "{0}이(가 선택되었습니다.\n 예약 가능한 날짜 중 원하는 날짜를 선택해주세요.".format("2. 박ㅇㅇ")
            edit_msg(context, update, button_list, len(button_list) - 3, text)

        # BTN3
        elif data_selected == "이ㅇㅇ":
            button_list = build_button([date3, date4, "cancel"], data_selected)
            text = "{0}이(가) 선택되었습니다.\n 예약 가능한 날짜 중 원하는 날짜를 선택해주세요.".format("3. 이ㅇㅇ")
            edit_msg(context, update, button_list, len(button_list) - 1, text)

        # BTN4
        elif data_selected == "기타문의":
            global msg
            msg = True
            button_list = build_button(["cancel"], data_selected)
            text = "{0}가 선택되었습니다. 기타 문의사항을 입력해주세요.".format("4. 기타문의")
            edit_msg(context, update, button_list, len(button_list), text)

    # 2nd Selection
    elif len(data_selected.split(",")) == 2:
        print("length = 2")
        cur_time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        doc = data_selected.split(", ")[0]
        date = data_selected.split(", ")[1]
        sql = f"INSERT INTO serena VALUES('serena', '01084849797', '1234', '{date}', '15:00', '{cur_time}', '{data_selected}')"
        context.bot.edit_message_text(text="{0}선생님 {1}일에 예약 완료되었습니다. 감사합니다."
                                           "\n병원 위치 : https://place.map.kakao.com/11272379".format(doc, date),
                                      chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id,
                                      parse_mode="Markdown")
        db.db_insert(sql)


# Get Button List and Reply with it
def edit_msg(context, update, button_list, btnlen, text):
    show_markup = InlineKeyboardMarkup(build_menu(button_list, btnlen))
    context.bot.edit_message_text(text=text,
                                  chat_id=update.callback_query.message.chat_id,
                                  message_id=update.callback_query.message.message_id,
                                  reply_markup=show_markup)


# Message Reply
def get_message(update, context):
    global msg
    cur_time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    text = update.message.text
    print("get_message: " + text)

    # 4. 기타문의로 들어올 경우
    if msg:
        sql = f"INSERT INTO serena VALUES('serena', '01084849797', '1234', '-', '-', '{cur_time}', '{text}')"
        db.db_insert(sql)
        update.message.reply_text("문의가 등록되었습니다.")
        msg = False
    else:
        update.message.reply_text("다시 입력해주세요.")


# Photo Reply
def get_photo(update, context):
    file_name = 'telegram_Image.png'
    file_id = update.message.photo[-1].file_id
    text = '사진이 저장되었습니다. "{}"'.format(file_name)
    upload(update, context, file_name, file_id, text)


# File Reply
def get_file(update, context):
    file_name = update.message.document.file_name
    file_id = update.message.document.file_id
    text = '파일이 저장되었습니다. "{}"'.format(file_name)
    upload(update, context, file_name, file_id, text)


# When File/Photo Uploaded
def upload(update, context, file_name, file_id, text):
    context.bot.getFile(file_id).download(file_name)
    update.message.reply_text(text)


# ==== api_key 통해 updater를 만들고 handler을 추가해주는 방식 ==== #

# updater --> 봇 업데이트 사항이 있으면 가져오는 클래스
updater = Updater(api_key, use_context=True)

# https://blog.psangwoo.com/coding/2018/01/09/python-telegram-bot-3.html
# ==== HANDLER(dispatcher가 받아오면 handling함) ==== #
# Handler for Help Command
help_handler = CommandHandler('help', help_command)
updater.dispatcher.add_handler(help_handler)

# Handler for Callback
updater.dispatcher.add_handler(CallbackQueryHandler(callback_help))

# Handler for Message(Text) --> (Filters.text:텍스트에 응답, get_message 함수 호출)
message_handler = MessageHandler(Filters.text, get_message)
updater.dispatcher.add_handler(message_handler)

# Handler for Photo
photo_handler = MessageHandler(Filters.photo, get_photo)
updater.dispatcher.add_handler(photo_handler)

# Handler for File
file_handler = MessageHandler(Filters.document, get_file)
updater.dispatcher.add_handler(file_handler)

# polling 방식: 주기적으로 텔레그램 서버에 접속해서 새로운 메세지가 있으면 받아옴
# timeout은 polling에 걸리는 시간의 최대치
# clean은 deprecated --> drop_pending_updates로 서버에 저장되어 있던 업데이트 내용 삭제
updater.start_polling(timeout=3, drop_pending_updates=True)  # drop_pending_updates=True : to drop all pending updates

# updater가 종료되지 않고 계속 실행되도록 하는 함수
updater.idle()





# message.reply_markup.inline_keyboard
# {'id': '4203917700656931534',
#  'chat_instance': '-8653369940690708398',
#  'message': {
#      'message_id': 124,
#      'date': 1617244543,
#      'chat': {
#          'id': 978800864,
#          'type': 'private',
#          'first_name': '예원',
#          'last_name': '서'
#      },
#      'text': '원하시는 문의 유형을 번호로 입력해주세요.',
#      'entities': [],
#      'caption_entities': [],
#      'photo': [],
#      'new_chat_members': [],
#      'new_chat_photo': [],
#      'delete_chat_photo': False,
#      'group_chat_created': False,
#      'supergroup_chat_created': False,
#      'channel_chat_created': False,
#      'reply_markup': {
#          'inline_keyboard': [
#              [
#                  {'text': '1. 반품문의', 'callback_data': 'btn1'},
#                  {'text': '2. 교환문의',  'callback_data': 'btn2'}
#              ],
#              [
#                  {'text': '3. 배송문의', 'callback_data': 'btn3'},
#                  {'text': '4. 기타문의', 'callback_data': 'btn4'}
#              ]
#          ]
#         },
#      'from': {
#          'id': 1761478694,
#           'first_name': 'Serena',
#           'is_bot': True,
#           'username': 'Serena_chatbot'
#      }
#  },
#  'data': 'btn1',
#  'from': {
#      'id': 978800864,
#           'first_name': '예원',
#           'is_bot': False,
#           'last_name': '서',
#           'language_code': 'ko'
#     }
#  }
