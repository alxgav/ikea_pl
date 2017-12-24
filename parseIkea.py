import requests
import re
import csv
import json


from bs4 import BeautifulSoup
from datetime import datetime
from multiprocessing import Pool

URL = "http://www.ikea.com/pl/pl/"
URL_PRODUKT = "http://www.ikea.com"


def get_html(url):
    r = requests.get(url)
    return r.text


# get category
def get_list_category(html):

    soup = BeautifulSoup(html, 'lxml')
    categ = []
    parent_category = ''
    ul = soup.find('ul', class_='header-nav-sublist').find_all('li', class_='header-nav-sublist-title')
    data_produkt = []

    for i in ul:
        a = i.find('a').get('href')
        if a == '#':
            parent_category = i.find(class_='non-active-link').text.strip()
            print('----', parent_category, '----')
        # li = i.find('div', class_='col-3').find_all('li')
        col = i.find_all('div', class_='col-3')

        for col3 in col:
            li = col3.find('ul').find_all('li')
            for a in li:
                link = a.find('a').get('href')
                link_produkt = 'http://' + str(link)[2:]
                print(len(get_all_produkt(get_html(link_produkt))))
                if len(get_all_produkt(get_html(link_produkt))) != 0:
                    for k in get_all_produkt(get_html(link_produkt)):
                        #    print(re.sub("\s\s+", " ", a.find('a').text), k)
                        data_produkt.append(k);
                        writeTextFile(k)

    return data_produkt


# get all link of ikea produkt
def get_all_produkt(html):
    soup = BeautifulSoup(html, 'lxml')
    produkt = []
    image = soup.find_all('div', class_='image')
    #    id = 1
    for i in image:
        a = i.find('a').get('href')
        produkt.append(URL_PRODUKT + a);
    return produkt


# get detail produkt
def get_detail_produkt(html):
    soup = BeautifulSoup(html, 'lxml')
    price_pln = 0.00
    # name of product
    try:
        name = soup.find('div', id='name').text.strip()
    except:
        name = ''
    # short description
    try:
        type = soup.find('div', id='type').text.strip()
    except:
        type = ''
    # PRICE PLN
    try:
        price1 = soup.find('span', id='price1').text.strip().replace("PLN","").replace("/m²","").replace(",",".").replace(" ","")
        price_pln = price1
    except:
        price_pln = '0.00'
    # PRICE GRN
    try:
        price_grn = price1 * 9
    except:
        price_grn = '0.00'
    # articul
    try:
        itemNumber = soup.find('div', id='itemNumber').text.strip()
    except:
        itemNumber = ''
    # image
    try:
        product_img = URL_PRODUKT + soup.find('img', id='productImg').get('src')
    except:
        product_img = ''
    # description full
    try:
        sales_arg = soup.find('div', id='salesArg').text.strip()
    except:
        sales_arg = ''

    data = {'name': name,
            'type': type,
            'price1': price1,
            'price_grn': price_grn,
            'itemNumber': itemNumber,
            'product_img': product_img,
            'salesArg': sales_arg}
    return data


# csv file
def write_csv(data):
    csv_header = ['name', 'type', 'price1', 'itemNumber', 'productImg', 'salesArg']
    csv.register_dialect('myDialect', delimiter=';', quoting=csv.QUOTE_ALL, quotechar='"') #, escapechar='\\'
    with open('category.csv', "a", newline="") as file:
        writer = csv.writer(file, dialect='myDialect')
        writer.writerow((data['name'],
                         data['type'],
                         data['price1'],
                         data['price_grn'],
                         data['itemNumber'],
                         data['product_img'],
                         data['salesArg']))
        print(data['name'],
              data['type'],
              data['price1'],
              data['itemNumber'],
              data['product_img'],
              data['salesArg'])


# write text file
def writeTextFile(text):
    file = open("tmp.txt","a")
    file.write(text+"\n")
    file.close()

def make_data_all(url):
    data = get_detail_produkt(get_html(url))
    write_csv(data)

# images
def get_images(html):
    soup = BeautifulSoup(html, 'lxml')
    data = soup.find_all("script")[19].string
    p = re.compile('var jProductData = (.*?);')
    m = p.findall(data)
    stocks = json.loads(m[0])
    for stock in stocks:
        print(stock)


def main():
    #get_images(get_html("http://www.ikea.com/pl/pl/catalog/products/40363126/"))
    link_produkt = get_list_category(get_html(URL))
    link_produkt.sort()
    # for url in list(set(link_produkt)):
    #     data = get_detail_produkt(get_html(url))
    #     write_csv(data)
    #     print(url)
    #     #writeTextFile(url)
    #print(len(url))
    with Pool(40) as p:
        p.map(make_data_all, set(link_produkt))


if __name__ == '__main__':
    main()
