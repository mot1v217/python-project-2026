import requests

API_KEY = "a82677ff-e7ff-4082-bba8-73f61d122ecb"

def get_coordinates(address):
    """ Принимает адрес (например, "Ленина, 22"). Возвращает (lat, lon) или (None, None), если не найдено."""
    full_address = f"Иркутск, {address}"
    
    url = "https://geocode-maps.yandex.ru/v1/"
    params = {
        "apikey": API_KEY,
        "geocode": full_address,
        "format": "json",
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code != 200:
            return None, None
            
        data = response.json()
        
        pos = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
        lon, lat = pos.split()
        
        return float(lat), float(lon)
    except (IndexError, KeyError, requests.RequestException):
        return None, None