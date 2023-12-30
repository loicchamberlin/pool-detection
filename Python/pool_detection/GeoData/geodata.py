import requests
import json
import cv2
import os

from pool_detection.GeoData.image_downloading import download_image


class GeoData:
    def __init__(self, address: str) -> None:
        self.address = address
        self.longitude = 0
        self.latitude = 0
        self.topleft_geoloc = 0
        self.bottomright_geoloc = 0
        self.zoom = 20
        self.path_to_main_image = "./ressources/Images/Images_raw/"
        self.filename = ""

    def get_address(self) -> str:
        return self.address

    def get_longitude(self) -> float:
        return self.longitude

    def get_latitude(self) -> float:
        return self.latitude

    def get_topleft_geoloc(self) -> (float, float):
        return self.topleft_geoloc

    def get_bottomright_geoloc(self) -> (float, float):
        return self.bottomright_geoloc

    def retrieve_geolocalisation(self) -> (float, float):
        """
        This function get a string that corresponds to a real address. 
        It uses geocode api to retrieve the corresponding geolocalisation (longitude, lattitude)

        :param address: string.
        :return tuple: (longitude, lattitude).
        """
        # converting the address
        address_withplus = self.address.replace(' ', '+')
        geocode_api_key = os.environ['GEOCODE_API_KEY']

        try:
            r = requests.get(
                f'https://geocode.maps.co/search?q={address_withplus}&api_key={geocode_api_key}')

            my_json = r.content.decode('utf-8')
            data = json.loads(my_json)

            self.latitude = float(data[0]['lon'])
            self.longitude = float(data[0]['lat'])

            self.bottomright_geoloc = (
                self.longitude - 0.002, self.latitude + 0.005)
            self.topleft_geoloc = (
                self.longitude + 0.002, self.latitude - 0.005)
        except:
            return print(f'The address : {self.address} is invalid.')

    def download_satellite_image(self):
        self.filename = self.address.replace(',', '_').replace(
            ' ', '_').replace('__', '_') + ".jpg"

        if not (os.path.isfile(self.path_to_main_image + self.filename)):
            self.retrieve_geolocalisation()

            default_prefs = {
                'url': 'https://mt.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
                'tile_size': 256,
                'channels': 3,
                'dir': self.path_to_main_image,
                'headers': {
                    'cache-control': 'max-age=0',
                    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'none',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
                },
                'tl': self.topleft_geoloc,
                'br': self.bottomright_geoloc,
                'zoom': self.zoom
            }

            lat1, lon1 = default_prefs['tl']
            lat2, lon2 = default_prefs['br']

            zoom = int(default_prefs['zoom'])
            channels = int(default_prefs['channels'])
            tile_size = int(default_prefs['tile_size'])
            lat1 = float(lat1)
            lon1 = float(lon1)
            lat2 = float(lat2)
            lon2 = float(lon2)

            img = download_image(lat1, lon1, lat2, lon2, zoom, default_prefs['url'],
                                 default_prefs['headers'], tile_size, channels)

            # name = "image2.jpg"  # Add a function, or variable for the name of the picture saved
            cv2.imwrite(os.path.join(default_prefs['dir'], self.filename), img)

    def get_filepath(self) -> str:
        return self.path_to_main_image + self.filename

    def convert_pixel_to_geolocalisation(self, x: int, y: int) -> (float, float):
        # Add test to verify if the coord pixel (x,y) are in the image given
        # Add test to verify if the image exists in the path
        img = cv2.imread(self.get_filepath())

        width, height = len(img), len(img[0])
        width_geoloc, height_geoloc = self.bottomright_geoloc[0] - \
            self.topleft_geoloc[0], self.bottomright_geoloc[1] - \
            self.topleft_geoloc[1]

        res_x, res_y = width_geoloc / width, height_geoloc / height

        return (self.topleft_geoloc[0] + x * res_x, self.topleft_geoloc[1] + y * res_y)
