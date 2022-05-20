from config import database_config

# saving the Database "local" in the database variable
database = database_config.DAO.get_database()


# a) Write a mongo query that finds all cities in the database that do not have the name "hello".
def get_cities_without_string(city_name):
    # checking if database was returned or not
    if database is not None:
        # returning all rows where name is not equal to the provided string, in this case "hello"
        return database["cities"].find({'name': {'$ne': city_name}})
    else:
        return None


# Write a mongo query that finds all roads in the database that have a length greater than zero and connect
# two of the cities found in a) (i.e. exclude roads that connect to any city not found previously).
def get_roads():
    # checking if database was returned or not
    if database is not None:
        # fetching all rows that have the name "hello"
        cities_with_string = database["cities"].find({'name': "hello"})
        city_ids = []

        # saving all ids of cities named "hello" which will be used to exclude all roads that have any of these ids
        # as one of the endpoints.
        for city in cities_with_string:
            city_ids.append(city["_id"])

        return database["roads"].find(
            {
                "$and": [
                    # condition for excluding the ids of the cities with the name "hello" using the city_ids array
                    {"endpoints": {"$nin": city_ids}},
                    # condition for all roads that have length greater than 0
                    {"length": {"$gt": 0}}
                ]
            }
        )
    else:
        return None


# c) Consider that every "island" contains at least one city, and that if it is possible to travel between
# two cities by roads if and only if the cities are on the same island.Write a function that, given the cities
# and roads, counts the number of islands.

# creating a function to call the function "count_islands" with the required parameters "cities" and "roads"
def get_no_of_islands():
    cities_collection = list(database["cities"].find())
    road_collection = list(database["roads"].find())
    return count_islands(cities_collection, road_collection)


def count_islands(cities, roads):
    # initializing the variable
    no_of_islands = 0

    # running the while loop till the cities list isn't empty
    while len(cities) > 0:
        # initializing the island_cities list with the first city and removing it from the cities list. This array
        # is used to save connected cities and to find other connected cities.
        island_cities = [cities[0]]
        cities.pop(0)

        # loop iterating through cities list
        for city in cities:
            # flag used to determine if the city has already been added to island_cities list and removed from cities,
            # then break the loop iterating through roads, to prevent removing city that does not exist.
            flag = 0

            # iterating through the roads list
            for road in roads:
                # checking if the road connects the current city with another city
                if city["_id"] in list(road["endpoints"]):
                    for island_city in island_cities:
                        # checking if the current city is connected with any of the island_cities, it means it's on
                        # the same island
                        if island_city["_id"] in list(road["endpoints"]):
                            # adding the city to island_cities
                            island_cities.append(city)

                            # removing the city from cities
                            cities.remove(city)

                            # setting the flag to break the roads loop
                            flag = 1
                            break
                # breaking the roads loop if the city was removed from the cities list
                if flag:
                    break
        # incrementing the no_of_islands
        no_of_islands += 1
    return no_of_islands


# We want to connect directly or indirectly all the cities on each island with electrical power lines.
# Power lines can only be placed along roads, so a power line segment connecting 2 cities will have a length
# matching that of the road.Write a function that, given cities and roads, finds the shortest total length of
# power lines needed to connect the cities. Note that if two cities are on different islands, they do not need
# to be connected.
#
# ASSUMING roads with length < 0 are also to be considered even though length cannot be negative.
# creating a function to call the function "compute_powerline_length" with the required parameters "cities" and "roads"
def get_powerline_length():
    cities_collection = list(database["cities"].find())
    road_collection = list(database["roads"].find())
    return compute_powerline_length(cities_collection, road_collection)


# using the Minimum Spanning Tree algorithm to find the shortest total length required to connect all cities, some
# cities are not connected to any other city, so they cannot be connected with power lines.
def compute_powerline_length(cities, roads):
    # asserting that roads is a list so that it can use functions of a list
    assert(type(roads) is list)

    # sorting the roads list based on the length in ascending order
    roads.sort(key=lambda row: (row["length"]))

    # initializing the variable
    total_powerline_length = 0

    # initializing list to save the ids of all the cities already connected by power lines
    connected_city_ids = []

    # iterating through sorted roads list
    for road in roads:
        # checking if both endpoints of the city already connected with the power lines
        if road["endpoints"][0] in connected_city_ids and road["endpoints"][0] in connected_city_ids:
            # skipping to the next iteration is condition is true
            continue
        # adding the endpoints of the road to the connected_city_ids
        # note: some city ids will be added multiple times but that doesn't affect the result
        connected_city_ids.append(road["endpoints"][0])
        connected_city_ids.append(road["endpoints"][1])

        # adding the road length to the total_powerline_length
        total_powerline_length += road["length"]

    return total_powerline_length
