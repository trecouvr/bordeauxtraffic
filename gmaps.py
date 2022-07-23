import logging
import requests


logger = logging.getLogger(__name__)


class GmapAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_direction(self, origin, destination):
        url = 'https://maps.googleapis.com/maps/api/directions/json'
        params = {
            'origin': origin,
            'destination': destination,
            'mode': 'driving',
            'alternatives': 'false',
            'units': 'metric',
            'departure_time': 'now',
            'key': self.api_key,
        }
        r = requests.get(url, params=params)
        if r.status_code != 200:
            logger.error('API Error %s %r', r.status_code, r.content[:100])
        return r.json()

    def get_duration(self, origin, destination):
        data = self.get_direction(origin, destination)
        return data['routes'][0]['legs'][0]['duration_in_traffic']['value'] // 60
