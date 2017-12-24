import csv
import os


def garb_csv():
    id = 0
    row_id = 1000
    filename = 1

    with open('goods_translate_ru.csv') as rFile:
        reader = csv.reader(rFile)
        for row in reader:
          #  print(row)
            if id == row_id:
                writeCsv(row, 'file')
                print('------', id, '------')
                row_id +=1000

            id +=1

def writeCsv(row, filename):
    csv.register_dialect('myDialect', delimiter=';', quoting=csv.QUOTE_NONE)
    myFile = open(filename+'.csv', 'w')
    with myFile:
        writer = csv.writer(myFile, dialect='myDialect')
        writer.writerows(row)

def csv_w():
    myFile = open('goods.csv', 'w')
    csv.register_dialect('myDialect', delimiter=';', quoting=csv.QUOTE_NONE)
    with myFile:
        myFields = ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12']
        writer = csv.DictWriter(myFile, dialect='myDialect', fieldnames=myFields)
        writer.writeheader()



def main():
    garb_csv()


if __name__ == '__main__':
    main()

def func():
	mas = [1,2,3,4,5,6,7,8]
	a = mas[0]
