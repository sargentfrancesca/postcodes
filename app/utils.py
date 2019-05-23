import os
from collections import defaultdict, namedtuple
import json
import requests
from django.conf import settings
from django.http import Http404


def _get_json_data():
    """Load store data from json file."""
    current_directory = os.path.realpath(os.path.dirname(__file__))
    fixture = os.path.join(current_directory, 'fixtures', 'locations.json')

    locations = []
    with open(fixture, 'r') as f:
        locations = json.load(f)
    return locations


def _get_api_data(locations):
    """Return postcode data from postcodes.io for given locations list."""
    postcodes = [x['postcode'] for x in locations]
    data = {'postcodes': postcodes}
    response = requests.post(settings.POSTCODE_URL, data=data)

    if response.status_code != 200:
        raise Http404('Postcode not found. Please use a valid UK postcode.')

    return response.json()


def _zip_data_dict(locations):
    """Merge latitude and longitude values from API data with existing store data."""
    response_json = _get_api_data(locations)

    merged_values = defaultdict(dict)
    for item in locations:
        merged_values[item['postcode']].update(item)

    for item in response_json['result']:
        result = item.get('result')

        geodata = {
            'longitude': result.get('longitude', 'NA') if result else 'NA',
            'latitude': result.get('latitude', 'NA') if result else 'NA',
        }
        merged_values[item['query']].update(geodata)

    return merged_values


def _postcode_objects(locations):
    """Return list of valid Location classes."""
    Location = namedtuple('Location', 'name postcode longitude latitude')
    return[
        Location(
            locations[x]['name'].replace('_', ' '),
            locations[x]['postcode'],
            locations[x]['longitude'],
            locations[x]['latitude']
        ) for x in locations
    ]


def get_locations():
    """Return list of locations with json and postcodes.io data."""
    initial_location_data = _get_json_data()
    consolidated_location_data = _zip_data_dict(initial_location_data)
    return _postcode_objects(consolidated_location_data)


def get_items(response):
    """Return postcodes.io result from API response."""
    data = response.json()
    return data.get('result')
