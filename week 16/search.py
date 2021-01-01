import pymongo


class CONFIG:
    """
    """
    MONGOURL = 'mongodb://{}:{}@localhost:27017/?authSource=admin'

    @staticmethod
    def connect_db(user, pwd):
        """
        """
        db = pymongo.MongoClient(CONFIG.MONGOURL.format(user, pwd))
        return db

    @staticmethod
    def close_db(db):
        """
        """
        db.close()
        pass


class DBSearch:
    """
    """
    def __init__(self, db, dbname: str, colname: str):
        self.db = db
        self.col = db[dbname][colname]
        pass

    def search(self, field, keyword):
        print('Result for keyword {} in field {}...'.format(keyword, field))
        res = self.col.find({field: {'$regex': keyword}})
        for index, doc in enumerate(res, start=1):
            print(index, doc['ID'], doc['title'])
        pass

    def run(self):
        try:
            while True:
                skey = input('Enter the keyword (@@@exit@@@ for exit) : ')
                if skey == '@@@exit@@@':
                    print('exit')
                    break
                elif skey == '':
                    continue
                else:
                    key = skey.split()[0]
                    try:
                        field = skey.split()[1]
                    except IndexError:
                        field = 'text'
                    self.search(field, key)
        except:
            raise
        finally:
            CONFIG.close_db(self.db)


def main():
    db = CONFIG.connect_db('root', 'root')
    dbs = DBSearch(db, 'admin', 'VOA')
    dbs.run()
    pass


if __name__ == '__main__':
    main()
    pass
