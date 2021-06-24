from .logging import start_logger
from .config import Config, get_config
from .httpclient import MBTAClient
from .state import SQLITE3Datastore

from collections import defaultdict


class Project:
    def __init__(self, config_path: str):
        self.config = get_config(config_path)
        self.log = start_logger(self.config)
        self.client = MBTAClient(log=self.log, config=self.config)
        self.state = SQLITE3Datastore(log=self.log, filepath=self.config.DatabasePath)
        self.get_all_type0or1_long_names()
        self.get_most_stops_route()
        self.get_least_stops_route()
        self.get_stops_with_multiple_routes()

    def get_all_type0or1_long_names(self):
        # Use the http client to get a list of all available routes
        routes = self.client.get_routes()

        # Use list comprehension to filter the list down to only subways (type 0 or 1), and return the long names for them
        route_long_names = [route['attributes']['long_name'] for route in routes if route['attributes']['type'] in (0,1)]
        print("Problem 1: Route long names are", route_long_names, "\n")

    def get_most_stops_route(self):
        # Use the http client to get a list of all the stops for each route
        stops = self.client.get_stops_by_route()

        # Sort the stops using a (key, value) pair, where the key is the route and the value is the list of all stops on that route
        # Sorted in increasing order by the length of the list of stops (kvpair[1] aka the count of the number of stops on the route)
        # and return the tuple (route, stops) at the bottom of the list to get the route with the long list of stops
        most_stops_route, stops = sorted(stops.items(), key=lambda kvpair: len(kvpair[1]))[-1] # end of list
        print("Problem 2: The route with the most stops is", most_stops_route, "which has", len(stops), "stops\n")

    def get_least_stops_route(self):
        # The process is identical to Problem 2, but since we want the least number of stops we just grab the tuple at the top of the list (0)
        stops = self.client.get_stops_by_route()
        least_stops_route, stops = sorted(stops.items(), key=lambda kvpair: len(kvpair[1]))[0] # top of list
        print("Problem 3: The route with the least stops is", least_stops_route, "which has", len(stops), "stops\n")

    def get_stops_with_multiple_routes(self):
        # Get routes filtered by subway (type 0 or 1)
        routes = self.client.get_filtered_routes()

        # Get all stops on each filtered route
        stops = self.client.get_stops_by_route()

        routes_by_stop_id = defaultdict(list)
        stops_by_stop_id = {}

        # Build a dictionary by 'id' so we can access it easier later
        routes_by_route_id = {r['id']:r for r in routes}

        # Loop over every stop
        for route_id in stops:
            # Loop over every stop again
            for stop in stops[route_id]:
                # Append the current route going through this stop to routes_by_stop_id for the current stop id
                routes_by_stop_id[stop['id']].append(routes_by_route_id[route_id])

                # Set stops_by_stop_id for this stop's ID to the current stop
                stops_by_stop_id[stop['id']] = stop        


        # Loop over each stop and each route in routes_by_stop_id, if the length is greater than 1 (2+ routes for that stop),
        # populate pruned_routes_by_stop_id with the stop name and the routes that run through it
        pruned_routes_by_stop_id = {
            stops_by_stop_id[stop_id]['attributes']['name']:[route['attributes']['long_name'] for route in routes]
            for stop_id, routes in routes_by_stop_id.items()
            if len(routes) > 1
        }

        # Create a list to display the data in a more readable fashion
        list_of_routes = list(pruned_routes_by_stop_id.items())[:len(pruned_routes_by_stop_id.items())]

        print("\nProblem 4: The stops with mutiple routes (2+) and their corresponding routes are\n")
        for route in range(len(list_of_routes)):
            print("\t", list_of_routes[route])
