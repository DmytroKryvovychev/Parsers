import requests
from bs4 import BeautifulSoup
import csv
import os

URL = 'https://www.amalgama-lab.com/songs/l'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.158 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
HOST = 'https://www.amalgama-lab.com'
FILE = 'bands.csv'
PROXIES = {'http': '148.216.17.24:8080', 'https': 'https://148.216.17.24:8080'}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params, proxies=PROXIES)
    return r


def get_content_bands(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='band_name_pict')

    bands = []
    for item in items:
        bands.append({
            'title': item.find('a').get_text(strip=True),
            'link': HOST + item.find('a').get('href')
        })
    return bands


def save_file_bands(items, path):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Band', 'Link'])
        for item in items:
            writer.writerow([item['title'], item['link']])


def get_content_songs(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('div', id='songs_nav').find_next('ul').find_next('ul').find_all('li')
    url = soup.find('link', rel='canonical').get('href')
    songs = []
    for item in items:
        songs.append({
            'title': item.find('a').get_text(strip=True),
            'link': url + item.find('a').get('href')
        })
    return songs


def save_file_songs(items, path):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Song', 'Link'])
        for item in items:
            writer.writerow([item['title'], item['link']])


def get_content_onlysong(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('div', id='click_area').find_all('div', class_=['string_container', 'empty_container'])

    lyrics = []
    for item in items[:-1]:
        lyrics.append({
            'original': item.find('div', class_='original').get_text(strip=True),
            'translate': item.find('div', class_='translate').get_text(strip=True)
        })
    return lyrics


def save_file_lyrics(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Original text', 'Translated text'])
        for item in items:
            writer.writerow([item['original'], item['translate']])


def main():
    URL = input('Input char: ')
    URL = HOST + '/songs/' + URL.strip()
    print(URL)
    html = get_html(URL)
    print(html)
    if html.status_code == 200:
        bands = []
        bands.extend(get_content_bands(html.text))
        save_file_bands(bands, FILE)
        print(f'Получено {len(bands)} групп')
        os.startfile(FILE)

        URL = input('Input band link: ')
        URL = URL.strip()
        html = get_html(URL)
        songs = []
        songs.extend(get_content_songs(html.text))
        songs_file = 'songs.csv'
        save_file_songs(songs, songs_file)
        print(f'Получено {len(songs)} песен')
        os.startfile(songs_file)

        URL = input('Input song link: ')
        URL = URL.strip()
        html = get_html(URL)
        lyrics = []
        lyrics.extend(get_content_onlysong(html.text))
        lyrics_file = 'lyrics.csv'
        save_file_lyrics(lyrics, lyrics_file)
        print(f'Получено {len(lyrics)} строк')

    else:
        print("Error")


if __name__ == '__main__':
    main()
