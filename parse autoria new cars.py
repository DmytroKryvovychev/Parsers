import requests
from bs4 import BeautifulSoup
import csv
import os

URL = 'https://auto.ria.com/newauto/marka-kia/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.158 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
HOST = 'https://auto.ria.com'
FILE = 'cars.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='proposition')

    cars = []
    for item in items:
        uah_price = item.find('span', class_='grey size13')
        if uah_price:
            uah_price = uah_price.get_text(strip=True)
        else:
            uah_price = 'Уточняйте цену'
        cars.append({
            'title': item.find('h3', class_='proposition_name').find_next('a').get_text(strip=True),
            'subtitle': item.find('div', class_='proposition_equip').find_next('a').get_text(strip=True),
            'link': HOST + item.find('h3', class_='proposition_name').find_next('a').get('href'),
            'usd_price': item.find('span', class_='green').get_text(strip=True),
            'uah_price': uah_price,
            'city': item.find('svg', class_='svg svg-i16_pin').find_next('strong').get_text(strip=True)
        })
    return cars


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='mhide')
    if pagination:
        return int(pagination[-1].get_text().replace(' ', ''))
    else:
        return 1


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Марка', 'Подтип', 'Ссылка', 'Цена в $', 'Цена в грн', 'Город'])
        for item in items:
            writer.writerow([item['title'], item['subtitle'], item['link'],
                             item['usd_price'], item['uah_price'], item['city']])


def parse():
    URL = input('Input URL: ')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
        save_file(cars, FILE)
        print(f'Получено {len(cars)} автомобилей')
        os.startfile(FILE)
    else:
        print('Error')


parse()
