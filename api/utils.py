import math

def degreesToRadians(degrees):
    return degrees * math.pi / 180

def distanceInKmBetweenCoordinates(coords1, coords2):
    earthRadiusKm = 6371

    lat1, lon1 = coords1.split(',')
    lat2, lon2 = coords2.split(',')
    lat1 = float(lat1)
    lat2 = float(lat2)
    lon1 = float(lon1)
    lon2 = float(lon2)

    dLat = degreesToRadians(lat2-lat1)
    dLon = degreesToRadians(lon2-lon1)

    lat1 = degreesToRadians(lat1)
    lat2 = degreesToRadians(lat2)

    a = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return earthRadiusKm * c

def carbonFootprint(distance, vehicleType):
    carbonKgForKm = {
        "BUS": 0.1,
        "TRAIN": 0.04,
        "TRAM": 0.08,
        "BIKE": 0.00,
        "EBIKE": 0.05,
        "SCOOTER": 0.025,
        "MOTO": 0.085,
        "CAR": 0.151,
        "ECAR": 0.037
    }
    return distance * float(carbonKgForKm.get(vehicleType, 0.0))

def costOfTransport(distance, minutes, vehicleType):
    costForMinute = {
        "BUS": 0,
        "TRAIN": 0,
        "TRAM": 0,
        "BIKE": 20,
        "EBIKE": 30,
        "SCOOTER": 30,
        "MOTO": 50,
        "CAR": 80,
        "ECAR": 80
    }
    costForKm = {
        "BUS": 25,
        "TRAIN": 25,
        "TRAM": 25,
        "BIKE": 2,
        "EBIKE": 5,
        "SCOOTER": 4,
        "MOTO": 8,
        "CAR": 10,
        "ECAR": 10
    }
    return minutes * int(costForMinute.get(vehicleType, 0)) + distance * int(costForKm.get(vehicleType, 0))