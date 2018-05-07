"""
This contains helper functions for getting pub recommendations.
"""

import googlemaps


from config import google_api_key
from loggers import mlog

gmaps = googlemaps.Client(google_api_key)


def get_pub_suggestions(location, number=3, maximum_distance=None, initial_distance=50):
    suggestions = []
    radius = initial_distance
    while len(suggestions) < number:
        mlog.debug(f"collected {len(suggestions)} so far.")
        if radius < maximum_distance:
            res = gmaps.places("pub", location=location['geometry']['location'],
                               radius=radius, open_now=True
                               )
        else:
            res = gmaps.places("pub", location=location['geometry']['location'],
                               radius=radius, open_now=True, page_token=next_page_token)
        suggestions += res['results']
        next_page_token = res['next_page_token']
        radius = min(radius*2, maximum_distance)
    #TODO sort
    #truncate suggestions list to specified length
    suggestions = suggestions[:number]
    for pub in suggestions:
        res = gmaps.place(pub['place_id'])['result']
        print(f"{res['name']}")
    print(f"{res.keys()}")
    return suggestions






def get_location(location_string):

    location = gmaps.places(location_string)

    if location['status'] == 'OK':
        location = location['results']
        if len(location) > 1:
            #TODO: ask for confirmation
            mlog.warn("multiple locations found - trusting google's recommendation")
            return location[0]
        else:
            return location[0]
    else:
        raise

if __name__ == "__main__":
    location = get_location("36 King street, Covent Garden")

    suggestions = get_pub_suggestions(location, maximum_distance=201, number=5)
