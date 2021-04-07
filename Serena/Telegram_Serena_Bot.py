from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import db_file.dbconn as db_con
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


# #################################### Menu / Button #################################### #
# Create Button Menu
def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    # range(start, end, step), 2차원배열
    # [[1,2], [3,4], [5]]

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


# Get Button List and Reply with it
def edit_msg(context, update, button_list, btnlen, text):
    show_markup = InlineKeyboardMarkup(build_menu(button_list, btnlen))
    context.bot.edit_message_text(text=text,
                                  chat_id=update.callback_query.message.chat_id,
                                  message_id=update.callback_query.message.message_id,
                                  reply_markup=show_markup)


# ################################# Help Command / Callbacks ################################### #
# Help Command
# https://blog.psangwoo.com/coding/2018/08/20/python-telegram-bot-4.html
def help_command(update, context):
    print("help command")
    button_list = [[InlineKeyboardButton("1. Dr.Kim", callback_data="Kim"),
                   InlineKeyboardButton("2. Dr.Park", callback_data="Park")],
                   [InlineKeyboardButton("3. Dr.Lee", callback_data="Lee"),
                   InlineKeyboardButton("4. Dr.Choi", callback_data="Choi")],
                   [InlineKeyboardButton("기타문의", callback_data="기타문의")],
                   [InlineKeyboardButton(text="병원 웹사이트 바로가기", url='https://www.naver.com')]]
    # show_markup = InlineKeyboardMarkup(build_menu(button_list, len(button_list) - 4))  # make markup
    show_markup = InlineKeyboardMarkup(button_list)

    if update.message is not None:
        print("111")
        update.message.reply_text("예약을 원하시는 의사 선생님을 선택해주세요.", reply_markup=show_markup)
    else:
        print("222")
        context.bot.edit_message_text(text="예약을 원하시는 의사 선생님을 선택해주세요.",
                                      chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id,
                                      reply_markup=show_markup)


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
        if data_selected == "Kim":
            button_list = build_button([date1, date2, date3, "back", "cancel"], data_selected)
            text = "{0} 선생님이 선택되었습니다.\n 예약 가능한 날짜 중 원하는 날짜를 선택해주세요.".format("1. Kim")
            edit_msg(context, update, button_list, len(button_list) - 2, text)

        # BTN2
        elif data_selected == "Park":
            button_list = build_button([date2, date3, date4, date5, "back", "cancel"], data_selected)
            text = "{0} 선생님이 선택되었습니다.\n 예약 가능한 날짜 중 원하는 날짜를 선택해주세요.".format("2. Park")
            edit_msg(context, update, button_list, len(button_list) - 2, text)

        # BTN3
        elif data_selected == "Lee":
            button_list = build_button([date3, date4, "back", "cancel"], data_selected)
            text = "{0} 선생님이 선택되었습니다.\n 예약 가능한 날짜 중 원하는 날짜를 선택해주세요.".format("3. Lee")
            edit_msg(context, update, button_list, len(button_list) - 2, text)

        # BTN4
        elif data_selected == "Choi":
            button_list = build_button([date3, date4, "back", "cancel"], data_selected)
            text = "{0} 선생님이 선택되었습니다.\n 예약 가능한 날짜 중 원하는 날짜를 선택해주세요.".format("4. Choi")
            edit_msg(context, update, button_list, len(button_list) - 2, text)

        # BTN5
        elif data_selected == "기타문의":
            global msg
            msg = True
            button_list = build_button(["cancel"], data_selected)
            text = "{0}가 선택되었습니다. 기타 문의사항을 입력해주세요.".format("기타문의")
            edit_msg(context, update, button_list, len(button_list), text)


    # 2nd Selection
    elif len(data_selected.split(",")) == 2:
        print("length = 2")

        if data_selected.split(", ")[1] == "back":
            help_command(update, context)

        else:
            cur_time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            doc = data_selected.split(", ")[0]
            date = data_selected.split(", ")[1]
            sql = f"INSERT INTO serena VALUES('serena', '01084849797', '1234', '{date}', '15:00', '{cur_time}', '{data_selected}')"
            context.bot.edit_message_text(text="{0}선생님 {1}일에 예약 완료되었습니다. 감사합니다."
                                               "\n\n오시는길 : https://place.map.kakao.com/11272379".format(doc, date),
                                          chat_id=update.callback_query.message.chat_id,
                                          message_id=update.callback_query.message.message_id,
                                          parse_mode="Markdown")
            db.db_insert(sql)


# ###################################### Messages ###################################### #
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


# ################################## Handlers ################################## #
# ###################### dispatcher가 받아오면 handling함 ######################## #
# https://blog.psangwoo.com/coding/2018/01/09/python-telegram-bot-3.html

# updater --> 봇 업데이트 사항이 있으면 가져오는 클래스
updater = Updater(api_key, use_context=True)

# Handler for Help Command
updater.dispatcher.add_handler(CommandHandler('help', help_command))
updater.dispatcher.add_handler(MessageHandler(Filters.text, get_message))
updater.dispatcher.add_handler(MessageHandler(Filters.photo, get_photo))
updater.dispatcher.add_handler(MessageHandler(Filters.document, get_file))

# Handler for Callback
updater.dispatcher.add_handler(CallbackQueryHandler(callback_help))

# polling 방식: 주기적으로 텔레그램 서버에 접속해서 새로운 메세지가 있으면 받아옴
# timeout은 polling에 걸리는 시간의 최대치
updater.start_polling(timeout=3, clean=True)

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
