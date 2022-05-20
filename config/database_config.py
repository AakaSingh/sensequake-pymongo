import pymongo

client = pymongo.MongoClient("localhost", 9999)


class DAO:

    def __init__(self):
        pass

    @staticmethod
    def get_database():
        if client is not None:
            return client["local"]
        else:
            return None
