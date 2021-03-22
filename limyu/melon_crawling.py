import requests
from bs4 import BeautifulSoup

try:
    melonurl = 'https://www.melon.com/chart/index.htm'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57'}
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
        #print(f'{song_name[i]} / {artist_name[i]}')
        returnValue += str((i + 1)) + ")" + str(song_name[i]) + " " + str(artist_name[i]) + "\n"

    print(returnValue)
except Exception as e:
    print(str(e))
