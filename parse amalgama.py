import requests
from lxml import etree
import lxml.html
import csv


def parse(url):
    api = requests.get(url)
    tree = lxml.html.document_fromstring(api.text)
    text_original = tree.xpath('//*[@id="click_area"]/div//*[@class="original"]/text()')
    print(text_original)


def main():
    parse("https://www.amalgama-lab.com/songs/l/linkin_park/and_one.html")


if __name__ == "__main__":
    main()
