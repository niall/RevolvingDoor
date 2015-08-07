import requests

"""
Lookup Postcode information using postcodes.io
"""

def postcode_lookup(postcode, variable):
    api = 'http://api.postcodes.io/postcodes/'
    request = requests.get(api + postcode)

    data = request.json()
    return data['result'][variable]

def lat_lookup(postcode):
    return postcode_lookup(postcode, 'latitude')

def lon_lookup(postcode):
    return postcode_lookup(postcode, 'longitude')

def postcode_validate(postcode):
    api = 'http://api.postcodes.io/postcodes/'
    append = "/validate"
    request = requests.get(api + postcode + append)
    data = request.json()
    return data['result']

"""
Create Embed Map from Postcode
https://www.google.com/maps/embed/v1/place?q=ha35hx&key=AIzaSyDnb8mAYrrCipHmrbm3qbDooyjzh97Z7o0"
"""

def map_lookup(postcode):
    api_key = '&key=AIzaSyDnb8mAYrrCipHmrbm3qbDooyjzh97Z7o0'
    full_url = 'https://www.google.com/maps/embed/v1/place?q=' + postcode + api_key
    return full_url