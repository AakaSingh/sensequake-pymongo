from bson import ObjectId

from config import database_config

database = database_config.DAO.get_database()

# a) Write a mongo query that finds all cities in the database that do not have the name "hello".


def get_cities_without_string(city_name):
    cities_collection = database["cities"]

    if database is not None:
        return cities_collection.find({'name': {'$ne': city_name}})
    else:
        return database


def get_roads():
    cities_with_string = database["cities"].find({'name': "hello"})
    city_ids = []

    for city in cities_with_string:
        city_ids.append(city["_id"])

    roads_result = database["roads"].find(
        {
            "$and": [
                {"endpoints": {"$nin": city_ids}},
                {"length": {"$gt": 0}}
            ]
        }
    )

