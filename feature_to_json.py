from geojson import Feature, Point, FeatureCollection

my_point = Point((-3.68, 40.41))
my_point_properties = {"country": "Spain"}

my_point2 = Point((-4.68, 41.41))
my_point_properties2 = {"country": "Italy"}

my_point3 = Point((-5.68, 42.41))
my_point_properties3 = {"country": "Russia"}

feat1 = Feature(geometry=my_point, properties=my_point_properties)
feat2 = Feature(geometry=my_point2, properties=my_point_properties2)
feat3 = Feature(geometry=my_point3, properties=my_point_properties3)

test=FeatureCollection([feat1,feat2,feat3])

print test