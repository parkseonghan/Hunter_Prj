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

# get_message FLAG
msg: bool = False

# Init Message
bot.sendMessage(chat_id=chat_id, text="진료예약 시작을 위해 입력창에 /help를 입력해주세요")


# ==== FUNCTION ==== #
# Create Button Menu
def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols]
            for i in range(0, len(buttons), n_cols)]  # range(start, stoop, step)

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
    button_list = [InlineKeyboardButton("1. 김ㅇㅇ", callback_data="1"),
                   InlineKeyboardButton("2. 박ㅇㅇ", callback_data="2"),
                   InlineKeyboardButton("3. 이ㅇㅇ", callback_data="3"),
                   InlineKeyboardButton("4. 기타문의", callback_data="4")]
    show_markup = InlineKeyboardMarkup(build_menu(button_list, len(button_list) - 1))  # make markup

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
        if data_selected == "1":
            button_list = build_button([date1, date2, date3, "cancel"], data_selected)
            show_markup = InlineKeyboardMarkup(build_menu(button_list, len(button_list) - 1))
            context.bot.edit_message_text(text="{0}이(가 선택되었습니다.\n 예약 가능한 날짜 중 원하는 날짜를 선택해주세요.".format("1. 김ㅇㅇ"),  # format(update.callback_query.data)
                                          chat_id=update.callback_query.message.chat_id,
                                          message_id=update.callback_query.message.message_id,
                                          reply_markup=show_markup)

        # BTN2
        elif data_selected == "2":
            button_list = build_button([date2, date3, date4, date5, "cancel"], data_selected)
            show_markup = InlineKeyboardMarkup(build_menu(button_list, len(button_list) - 3))
            context.bot.edit_message_text(text="{0}이(가 선택되었습니다.\n 예약 가능한 날짜 중 원하는 날짜를 선택해주세요.".format("2. 박ㅇㅇ"),
                                          chat_id=update.callback_query.message.chat_id,
                                          message_id=update.callback_query.message.message_id,
                                          reply_markup=show_markup)

        # BTN3
        elif data_selected == "3":
            button_list = build_button([date3, date4, "cancel"], data_selected)
            show_markup = InlineKeyboardMarkup(build_menu(button_list, len(button_list) - 1))
            context.bot.edit_message_text(text="{0}이(가) 선택되었습니다.\n 예약 가능한 날짜 중 원하는 날짜를 선택해주세요.".format("3. 이ㅇㅇ"),
                                          chat_id=update.callback_query.message.chat_id,
                                          message_id=update.callback_query.message.message_id,
                                          reply_markup=show_markup)

        # BTN4
        elif data_selected == "4":
            global msg
            msg = True
            button_list = build_button(["cancel"], data_selected)
            show_markup = InlineKeyboardMarkup(build_menu(button_list, len(button_list)))
            context.bot.edit_message_text(text="{0}가 선택되었습니다. 기타 문의사항을 입력해주세요.".format("4. 기타문의"),
                                          chat_id=update.callback_query.message.chat_id,
                                          message_id=update.callback_query.message.message_id,
                                          reply_markup=show_markup)

    # 2nd Selection
    elif len(data_selected.split(",")) == 2:
        print("length = 2")
        cur_time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        date = data_selected.split(", ")[1]
        print(data_selected)
        print(date)
        context.bot.edit_message_text(text="{0}가 선택되었습니다.".format(update.callback_query.data),
                                      chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id)
        sql = f"INSERT INTO serena VALUES('serena', '01084849797', '1234', '{date}', '15:00', '{cur_time}', '{data_selected}')"
        insert_sql(sql)


# Message Reply
def get_message(update, context):
    global msg
    cur_time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    text = update.message.text
    print("get_message: " + text)

    # 4. 기타문의로 들어올 경우
    if msg:
        sql = f"INSERT INTO serena VALUES('serena', '01084849797', '1234', '-', '-', '{cur_time}', '{text}')"
        insert_sql(sql)
        update.message.reply_text("문의가 등록되었습니다.")
        msg = False
    else:
        update.message.reply_text("다시 입력해주세요.")


# Photo Reply
def get_photo(update, context):
    file_path = os.path.join(cur_dir, 'telegram_Image.png')
    photo_id = update.message.photo[-1].file_id
    context.bot.getFile(photo_id).download(file_path)
    update.message.reply_text('photo saved')


# File Reply
def get_file(update, context):
    file_path = os.path.join(cur_dir, update.message.document.file_name)
    file_id = update.message.document.file_id
    context.bot.getFile(file_id).download(file_path)
    update.message.reply_text('file saved')


# Insert SQL
def insert_sql(sql):
    print("++++++++ " + sql + " ++++++++")
    db_con.Db_conn().insert_query(sql)



# ==== DB CONNECTION ==== #
# http://pythonstudy.xyz/python/article/202-MySQL-%EC%BF%BC%EB%A6%AC
# db_cls = db_con.Db_conn()
# dbcon = db_cls.connection()
# cursor = dbcon.cursor()  # cursor 객체 생성 : db에 sql문 수행하고 조회된 결과 가지고 오는 역할
# cursor.execute("SELECT name, pNum, pwd, DATE_FORMAT(date, '%Y%m%d'), time, writeDate FROM serena")
# rows = cursor.fetchall()  # fetchall : 조회된 결과 모두 리스트로 반환
# print(rows)

# db_cls = db_con.Db_conn()
# dbcon = db_cls.connection()
# cursor = dbcon.cursor()  # cursor 객체 생성 : db에 sql문 수행하고 조회된 결과 가지고 오는 역할
# print(sql)
# cursor.execute(sql)  # execute : sql문 실행
# dbcon.commit()
# rows = cursor.fetchall()  # fetchall : 조회된 결과 모두 리스트로 반환
# print(rows)
# dbcon.close()



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
# updater.dispatcher.add_handler(CallbackQueryHandler(get_message))

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
