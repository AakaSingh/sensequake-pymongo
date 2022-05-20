from bson import ObjectId

from config import database_config

database = database_config.DAO.get_database()

# a) Write a mongo query that finds all cities in the database that do not have the name "hello".


def get_cities_without_string(city_name):

    if database is not None:
        return database["cities"].find({'name': {'$ne': city_name}})
    else:
        return None


def get_roads():
    if database is not None:
        cities_with_string = database["cities"].find({'name': "hello"})
        city_ids = []

        for city in cities_with_string:
            city_ids.append(city["_id"])

        return database["roads"].find(
            {
                "$and": [
                    {"endpoints": {"$nin": city_ids}},
                    {"length": {"$gt": 0}}
                ]
            }
        )
    else:
        return None


def get_no_of_islands():
    cities_collection = list(database["cities"].find())
    road_collection = list(database["roads"].find())
    return count_islands(cities_collection, road_collection)


def count_islands(cities, roads):
    no_of_islands = 0

    while len(cities) > 0:
        island_cities = [cities[0]]
        cities.pop(0)
        for city in cities:
            flag = 0
            for road in roads:
                if city["_id"] in list(road["endpoints"]):
                    for island_city in island_cities:
                        if island_city["_id"] in list(road["endpoints"]):
                            island_cities.append(city)
                            cities.remove(city)
                            flag = 1
                            break
                if flag:
                    break
        no_of_islands += 1
    return no_of_islands

# Assuming roads with length < 0 are also to be considered
def compute_powerline_length:
