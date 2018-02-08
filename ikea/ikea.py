# -*- coding: utf-8 -*-
import requests
import re
import csv
import sqlite3
from googletrans import Translator
from bs4 import BeautifulSoup

URL = "http://www.ikea.com/pl/pl/"
URL_PRODUKT = "http://www.ikea.com"

# get url in text
def get_html(url):
    r = requests.get(url)
    return r.text
#translate
def translate(data):
    translator = Translator()
    return translator.translate(data, dest='ru').text
# get link of all produkt
def get_all_produkt(html):
    soup = BeautifulSoup(html, 'lxml')
    produkt = []
    image = soup.find_all('div', class_='image')
    #    id = 1
    for i in image:
       a = i.find('a').get('href')
       produkt.append(URL_PRODUKT + a)
    return produkt
# get URL_PRODUKT
def get_detail_produkt(html):
    soup = BeautifulSoup(html, 'lxml')
    price_pln = 0.00
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
    data = {'name': name,
            'short_desk': short_desk,
            'itemNumber': itemNumber,
            'metric': metric,
            'deskr': deskr}
    return data
# javascript variables
def get_script(html, name_f, kateg):
    soup = BeautifulSoup(html, 'lxml')
    data = soup.find_all('script')
    type_= ''
    color = ''
    images = ''
    price_pln = 0
    price_grn = 0
    description = ''
    metric = ''
    art_num = ''
    short_desk = ''
    goods_name = ''
    img = []
    #file = open('testfile.txt', 'a')
    conn = sqlite3.connect('db/ikea')
    c = conn.cursor()
    file = open('error.txt','a')
    for i in data:
        fd = i.text.strip()
        if "jProductData" in fd:
            for l in fd.split(','):
                #url goods
                if '"url":' in l:
                    u = "http://www.ikea.com"+l.replace('"url":','').replace('"', '').replace(']}', '')
                    # print ('url', u)
                    data = get_detail_produkt(get_html(u))
                    art_num = data['itemNumber']
                    description = translate(data['deskr']+'\n'+data['metric'])
                    short_desk = translate(data['short_desk'])
                    goods_name = data['name']
                    #price goods
                if '"rawPrice":' in l:
                    price_pln = l.replace('"rawPrice":','').replace('"', '').replace('}', '')
                    #price_grn = round(float(price_pln) * 10)
                    try:
                        c.execute("insert into ikea (art_num, price_pln, goods_name, short_desk, description, parent_kateg, kateg) values('"
                                 +art_num+"','"
                                 +price_pln+"','"
                                 +goods_name+"','"
                                 +short_desk+"','"
                                 +description+"','"
                                 +name_f+"','"
                                 +kateg+"')")
                        conn.commit()
                    except:
                        print ('error:', art_num)
                        file.write('error: ' + art_num)

                # images
                if '/pl/pl/images/' in l:
                    images = "http://www.ikea.com"+l.replace('"large":["', '').replace('"', '').replace(']}', '')
                    c.execute("insert into ikea_img (art_num, images) values('"+art_num+"','"+images+"')")
                    conn.commit()
                    # print ('images', images)
                    # f.write(images+'\n')

    conn.close
    file.close()
#parsing by name of goods
def parse_by_goods(url, name_f, kateg):
    links = get_all_produkt(get_html(url))
    print (len(links))
    id = 1
    for i in links:
        print (id, '-------', kateg, '-------left--', len(links) - id )
        #write_csv(get_script(get_html(i)), name_f, kateg)
        get_script(get_html(i), name_f, kateg)
        print ('-----end------')
        id +=1
# main by
def main():
    with open('kategories.csv', newline="") as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            parse_by_goods(row[2], row[0], row[1])

if __name__ == '__main__':
    main()



#garbage
    #description of goods
# if '"custBenefit":' in l:
#     description = l.replace('"custBenefit":','')
#     print ('custBenefit', description)
#
#     file.write(description+'\n')
    #articul of goods
# if '[{"articleNumber":' in l:
#     art_num = l.replace('[','').replace('}','').replace('{','').replace('"','').replace(':','').replace('articleNumber','').replace('pkgInfoArr','')
#     art_num = art_num[0:3]+'.'+art_num[3:6]+'.'+art_num[6:]
#     print('articleNumber', art_num)
#     file.write(str(id)+'\n')
#     file.write(art_num+'\n')
#
#     id +=1
    # name of goods calculate with color
# if '"color":' in l:
#     color = l.replace('"color":','')
#     print('"color":', color)
#     file.write(color+'\n')
# if '"type":' in l:
#     if l[-1:] != ']' and l[-1:] != '}':
#         type_ = l.replace('"type":','')
#         print ('"type":', type_)
#         file.write(type_+'\n')
#     # size of goods
# if '"metric":' in l:
#     metric = l.replace('"metric":','')
#     print ('"metric":', metric)
#     file.write(metric+'\n')
