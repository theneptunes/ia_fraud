import math

# Dado uma Latitude 1, Longitude 1, Latitude 2, Longitude 2, encontra a distância entre o local 1 e 2 em km.
def haversine(lat1, lon1, lat2, lon2):
    r = 6371  # radius of Earth in kilometers
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (pow(math.sin(dlat / 2), 2) + math.cos(lat1) * math.cos(lat2) * pow(math.sin(dlon / 2), 2))
    c = 2 * math.asin(math.sqrt(a))
    return c * r