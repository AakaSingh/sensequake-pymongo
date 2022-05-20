import pymongo

# setting up connection to the database
client = pymongo.MongoClient("localhost", 9999)


class DAO:

    def __init__(self):
        pass

    @staticmethod
    def get_database():
        # checking if the connection was successful
        if client is not None:
            # returning the database named "local" where we have the collections "roads" and "cities"
            return client["local"]
        else:
            return None
