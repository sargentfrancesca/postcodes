import requests
from django.conf import settings
from django.http import Http404
from operator import attrgetter
from django.shortcuts import render
from app.utils import get_locations, get_items


def index(request):
    """Index view to return store list alphabetically."""
    locations = get_locations()

    context = {
        'locations': sorted(locations, key=attrgetter('name')),
    }

    return render(request, 'app/index.html', context)


def radius(request, postcode, radius):
    """
    Functionality to list stores within radius of any given postcode.

    Outputs store locations from north to south order.
    """
    stores = get_locations()

    context = {
        'locations': [],
    }

    search_data = {
        'radius': radius,
        'limit': 100,
    }

    response = requests.get('{}{}'.format(
        settings.POSTCODE_URL, postcode
    ))

    if response.status_code != 200:
        raise Http404('Postcode not found. Please use a valid UK postcode.')

    items = get_items(response)

    radius_response = requests.get('{}{}/nearest'.format(
        settings.OUTCODES_URL, items.get('outcode')
    ), params=search_data)

    radius_items = get_items(radius_response)

    outcodes = [x['outcode'] for x in radius_items]
    store_postcodes = [x.postcode.split(' ')[0] for x in stores]

    intersection = tuple(set(outcodes).intersection(store_postcodes))
    locations = [x for x in stores if x.postcode.startswith(intersection)]

    if not locations:
        context.update({
            'messages': ['Unfortunately, there are no stores within this area. Please try again.']
        })

    context.update(
        {
            'locations': sorted(locations, key=attrgetter('longitude'), reverse=True)
        }
    )

    return render(request, 'app/index.html', context)
