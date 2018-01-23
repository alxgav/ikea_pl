# -*- coding: utf-8 -*-
import requests
import re
import csv
from googletrans import Translator
from bs4 import BeautifulSoup

URL = "http://www.ikea.com/pl/pl/"
URL_PRODUKT = "http://www.ikea.com"

# get url in text
def get_html(url):
    r = requests.get(url)
    return r.text
# get link of all produkt
def get_all_produkt(html):
    soup = BeautifulSoup(html, 'lxml')
    produkt = []
    image = soup.find_all('div', class_='parentContainer')
    #    id = 1
    for i in image:
       a = i.find('a').get('href')
       produkt.append(URL_PRODUKT + a)
    return produkt

def get_detail_produkt(html):
    soup = BeautifulSoup(html, 'lxml')
    price_pln = 0.00
    # kateg_name
    try:
        kateg = soup.find('ul', id='breadCrumbs').find_all('li')
        kateg_name =  kateg[-1].find('a').text

    except:
        kateg_name = ''
    # name of product
    try:
        name = soup.find('span', id='name').text.strip()
    except:
        name = ''
    # short description
    try:
        short_desk = soup.find('span', id='type').text.strip()
    except:
        short_desk = ''
    # PRICE PLN
    try:
        price1 = soup.find('span', id='price1').text.strip().replace("PLN", "").replace("/m²", "").replace(",", ".").replace(" ", "")
        price_pln = price1
    except:
        price_pln = '0.00'
    # PRICE GRN
    try:
        price_grn = int(price_pln) * 9
    except:
        price_grn = '0.00'
    # articul
    try:
        itemNumber = soup.find('div', id='itemNumber').text.strip()
    except:
        itemNumber = ''
    # description full
    try:
        deskr = soup.find('div', id='cbftssection').text.strip()
    except:
        deskr = ''
    # width heigth
    try:
        metric = soup.find('div', id = 'metric').text.strip()
    except:
        metric = ''
    # images
    try:
        data = soup.find_all('script')
        url_img = ''
        img = []
        num_img = 0
        for i in data:
            fd = i.text.strip()
            if "jProductData" in fd:
                large = fd
                for l in large.split(','):
                    if "/pl/pl/images/" in l:
                        img.append("http://www.ikea.com"+l.replace('"large":["', '').replace('"', '').replace(']}', ''))
                        # url_img += ",http://www.ikea.com"+l.replace('"large":["', '').replace('"', '').replace(']}', '')
        for images in img:
            if num_img > 3:
                continue
            url_img += "," + images
            num_img += 1

    except:
        url_img = ''
    data = {'kateg': kateg_name,
            'name': name,
            'short_desk': short_desk,
            'price_pln': price_pln,
            'price_grn': price_grn,
            'itemNumber': itemNumber,
            'metric': metric,
            'deskr': deskr,
            'url_img': url_img[1:]}
    return data
#translate
def translate(data):
    translator = Translator()
    return translator.translate(data, dest='ru').text
# create csv
def write_csv(data):
    csv_header = ['active', 'name', 'kateg', 'price_pln',
                  'price_grn', 'kol', 'min_kol', 'short_desk',
                  'deskr', 'order', 'show_price', 'image_url']
    csv.register_dialect('myDialect', delimiter=';', quoting=csv.QUOTE_ALL, quotechar='"')
    with open('goods.csv', "a", newline="") as file:
        writer = csv.writer(file, dialect='myDialect')
        writer.writerow(('1',
                         data['name'],
                         translate(data['kateg']),
                         data['price_pln'],
                         data['price_grn'],
                         data['itemNumber'],
                         '100',
                         '1',
                         translate(data['short_desk']),
                         translate(data['deskr']+data['metric']),
                         '1',
                         '1',
                         data['url_img']))

def main():
    links = get_all_produkt(get_html("http://www.ikea.com/pl/pl/search/?query=LINNMON&pageNumber=0"))
    for i in links:
        produkt = get_detail_produkt(get_html(i))
        print (translate(produkt['kateg']), produkt['name'], produkt['itemNumber'])
        print (produkt['price_pln'], produkt['price_grn'])
        print (translate(produkt['deskr']), translate(produkt['metric']))
        print (produkt['url_img'])
        print ('-----------------------------------------------------------------------')
        write_csv(get_detail_produkt(get_html(i)))

if __name__ == '__main__':
    main()
