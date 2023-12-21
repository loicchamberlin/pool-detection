import requests
import json


class GeoData:
    def __init__(self, address: str) -> None:
        self.address = address
        self.longitude = 0
        self.latitude = 0

    def get_address(self):
        return self.address

    def get_longitude(self):
        return self.longitude

    def get_latittude(self):
        return self.latitude

    def retrieve_geolocalisation(self) -> (float, float):
        """
        This function get a string that corresponds to a real address. 
        It uses geocode api to retrieve the corresponding geolocalisation (longitude, lattitude)

        :param address: string.
        :return tuple: (longitude, lattitude).
        """
        # converting the address
        address_withplus = self.address.replace(' ', '+')
        try:
            r = requests.get(
                f'https://geocode.maps.co/search?q={address_withplus}')
            my_json = r.content.decode('utf-8')
            data = json.loads(my_json)

            return float(data[0]['lat']), float(data[0]['lon'])
        except:
            return print(f'The address : {self.address} is invalid.')
