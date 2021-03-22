from telegram.ext import Updater, MessageHandler, Filters
import requests
from bs4 import BeautifulSoup
import json

bot_id = '1794898877:AAGcp6Kp_wUBdLvLiM5kcxZ--IdXuVIa3yA'

def getMelonChart():
    melonlist = 'Melon List'
    try:
        melonurl = 'https://www.melon.com/chart/index.htm'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57'}
        res = requests.get(melonurl, headers=headers).text
        soup = BeautifulSoup(res, "html.parser")

        artist_name = soup.select("#frm > div > table > tbody > tr > td > div > div > div.ellipsis.rank02")
        song_name = soup.select("#frm > div > table > tbody > tr > td > div > div > div.ellipsis.rank01")

        returnValue = ""

        for i in range(len(artist_name)):
            artist_name[i] = artist_name[i].select("div > a")
            for j in range(len(artist_name[i])):
                artist_name[i][j] = artist_name[i][j].text

        for k in range(len(song_name)):
            song_name[k] = song_name[k].select("div > span > a")
            for j in range(len(song_name[k])):
                song_name[k][j] = song_name[k][j].text

        for i in range(len(song_name)):
            # print(f'{song_name[i]} / {artist_name[i]}')
            returnValue += str((i + 1)) + ")" + str(song_name[i]) + " " + str(artist_name[i]) + "\n"

        melonlist = returnValue
    except Exception as e:
        print(str(e))

    return melonlist

def getJson(useText, jsondata) :
    keys = [key for key in jsondata]

    returnvalue = "안물안궁"

    for key in keys :
        if key in useText :
            returnvalue = jsondata[key]

    return returnvalue



def get_message(update , context):
    with open("../../json_test.json", "r", encoding='UTF8') as json_file:
        jsondata = json.load(json_file)

    useText = update.message.text

    if "실시간차트" in useText:
        update.message.reply_text(getMelonChart())
    else :
        update.message.reply_text(getJson(useText, jsondata))

updater = Updater(bot_id, use_context=True)

message_handler = MessageHandler(Filters.text, get_message)
updater.dispatcher.add_handler(message_handler)

updater.start_polling(timeout=3, clean=True)
updater.idle()