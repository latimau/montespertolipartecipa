import sys
from pygeocoder import Geocoder
from pygeolib import GeocoderError

indirizzo = raw_input('type an adress here: ')


try:
  address = Geocoder.geocode(indirizzo)
except GeocoderError:
  print "The address entered could not be geocoded"
  sys.exit(1)

#if not address.valid_address:
#  print "The address entered is not valid, but we did get some info"

#print "address.valid_address: ", address.valid_address
#print "address.street_number: ", address.street_number
#print "address.route: ", address.route
#print "address.sublocality: ", address.sublocality
#print "address.locality: ", address.locality
#print "address.administrative_area_level_1: ", address.administrative_area_level_1
#print "address.country: ", address.country
#print "address.postal_code: ", address.postal_code
print "address.coordinates: ", address.coordinates
print "address.formatted_address: ", address.formatted_address