import logging
from datetime import datetime as dt, timedelta

from .config import Config
from .utils import convert_to_seconds

import httpx
from rush import quota, throttle
from rush.limiters import gcra
from rush.stores import dictionary as dict_store

class MBTAClient:
    def __init__(self, log: logging.Logger, config: Config):
        self.log = log
        self.rate_limiter = throttle.Throttle(
            rate=quota.Quota(period=timedelta(seconds=convert_to_seconds(config.Period)),
            count=config.Count,
            maximum_burst=1
            ),
            limiter=gcra.GenericCellRatelimiter(store=dict_store.DictionaryStore(store=dict()))
        )
        self.client : httpx.Client = httpx.Client(
            headers={'x-api-key': 'b2088516068a4f779951cff2df404ff3'},
            base_url="https://api-v3.mbta.com"
        )
    
    def get_routes(self):
        is_limited = self.rate_limiter.check("key",1).limited
    
        while is_limited:
            is_limited = self.rate_limiter.check("key",1).limited
        resp = self.client.get('/routes')            
        if resp.status_code == 400:
            self.log.debug(f"Bad Request - {resp.json().get('detail', 'Unknown error')}")
            return []
        if resp.status_code == 403:
            self.log.debug(f"Forbidden")
            return []
        if resp.status_code == 429:
            self.log.debug(f"Too Many Requests")
            return []
        route_data: dict = resp.json()
        records: list[dict] = route_data['data']
        return records

    def get_filtered_routes(self):
        is_limited = self.rate_limiter.check("key",1).limited
    
        while is_limited:
            is_limited = self.rate_limiter.check("key",1).limited

        # Get all the routes, but only pull the subways (type 0 or 1)
        resp = self.client.get('/routes', params={"filter[type]": "0,1"})
        if resp.status_code == 400:
            self.log.debug(f"Bad Request - {resp.json().get('detail', 'Unknown error')}")
            return []
        if resp.status_code == 403:
            self.log.debug(f"Forbidden")
            return []
        if resp.status_code == 429:
            self.log.debug(f"Too Many Requests")
            return []
        filtered_routes_data: dict = resp.json()
        records: list[dict] = filtered_routes_data['data']
        return records

    def get_stops_by_route(self):
        # Grab the filtered routes
        routes = self.get_filtered_routes()
        stops = dict()
        for route in routes:
            is_limited = self.rate_limiter.check("key",1).limited
    
            while is_limited:
                is_limited = self.rate_limiter.check("key",1).limited
            # Looping over each subway route, get all the stops for that corresponding route using the id param of routes
            resp = self.client.get('/stops', params={
                "filter[route]": route['id'],
                "include": "route"
            })
            if resp.status_code == 400:
                self.log.debug(f"Bad Request - {resp.json().get('detail', 'Unknown error')}")
                return []
            if resp.status_code == 403:
                self.log.debug(f"Forbidden")
                return []
            if resp.status_code == 429:
                self.log.debug(f"Too Many Requests")
                return []
            stops_for_route_data: dict = resp.json()
            stops[route['id']] = stops_for_route_data['data']
        return stops