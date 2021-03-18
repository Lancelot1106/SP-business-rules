import csv
import pymongo


class Converter:
    def __init__(self):
        '''

        Initieer the converter self value's

        '''
        self.client = pymongo.MongoClient('localhost', 27017)
        self.database = self.client['HuWebshop']

    @staticmethod
    def mongo_to_csv(fieldnames, filename, collection):
        '''

        Convert the data from mongoDB to an csv file.

        :param fieldnames:
        :param filename:
        :param collection:
        :return:
        '''
        with open(filename, 'w', newline='', encoding='UTF-8') as csvout:
            '''
            If fieldname has a . in it strip everything befor the .
            '''
            print(f'Converten van {filename} begonnen!')
            writer = csv.DictWriter(csvout, fieldnames=[i if '.' not in i else i.split('.', 1)[1] for i in fieldnames])
            writer.writeheader()
            content = collection.find()
            c = 0
            for item in content:
                try:
                    '''
                    Loop through all the given items from the MongoDB and write in in a csv file.
                    '''
                    writer.writerow(
                        {
                            i if '.' not in i else i.split('.', 1)[1]: item.get(i) if '.' not in i else
                            item.get(i.split('.', 1)[0])[i.split('.', 1)[1]]
                            for i in fieldnames
                        }
                    )
                except:
                    continue
                c += 1
                if c % 10000 == 0:
                    print('{} records written...'.format(c))
        print('Finished creating the database content')

    def products(self, fieldnames, filename):
        '''
        Call the convert function with the wanted parameters to converts products.
        :param fieldnames:
        :param filename:
        :return:
        '''
        collection = self.database.products
        self.mongo_to_csv(fieldnames, filename, collection)

    def visitors(self, fieldnames, filename):
        '''
        Call the convert function with the wanted parameters to converts visitors.
        :param fieldnames:
        :param filename:
        :return:
        '''
        collection = self.database.visitors
        self.mongo_to_csv(fieldnames, filename, collection)

    def sessions(self, fieldnames, filename):
        '''
        Call the convert function with the wanted parameters to converts visitors.
        :param fieldnames:
        :param filename:
        :return:
        '''
        collection = self.database.sessions
        self.mongo_to_csv(fieldnames, filename, collection)
