import requests
import json

def ipinfo(ip_address):
    try:
        if ip_address == "127.0.0.1":
            ip_address = "152.58.57.53"
        response = requests.get(f"http://ipinfo.io/{ip_address}/json")
        if response.status_code == 200:
            data = json.loads(response.text)
            return data
        else:
            return False
    except requests.exceptions.RequestException as e:
        print(e)
        return False

# print(get_geolocation('152.58.57.144'))