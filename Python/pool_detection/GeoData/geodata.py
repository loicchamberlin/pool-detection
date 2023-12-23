import requests
import json
import re
import cv2
import os

import numpy as np
import threading


class GeoData:
    def __init__(self, address: str) -> None:
        self.address = address
        self.longitude = 0
        self.latitude = 0
        self.topleft_geoloc = 0
        self.bottomright_geoloc = 0
        self.zoom = 19
        self.path_to_main_image = "./ressources/Images/Images_raw/"

    def get_address(self):
        return self.address

    def get_longitude(self):
        return self.longitude

    def get_latitude(self):
        return self.latitude

    def get_topleft_geoloc(self):
        return self.topleft_geoloc

    def get_bottomright_geoloc(self):
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
        try:
            r = requests.get(
                f'https://geocode.maps.co/search?q={address_withplus}')
            my_json = r.content.decode('utf-8')
            data = json.loads(my_json)

            print('Data : ', data)
            print('')
            print('')
            print('')

            self.latitude = float(data[0]['lon'])
            self.longitude = float(data[0]['lat'])

            self.bottomright_geoloc = (
                self.longitude - 0.002, self.latitude + 0.005)
            self.topleft_geoloc = (
                self.longitude + 0.002, self.latitude - 0.005)
        except:
            return print(f'The address : {self.address} is invalid.')

    def download_satellite_image(self):
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

        img = self.download_image(lat1, lon1, lat2, lon2, zoom, default_prefs['url'],
                                  default_prefs['headers'], tile_size, channels)

        name = "image2.jpg"  # Add a function, or variable for the name of the picture saved
        cv2.imwrite(os.path.join(default_prefs['dir'], name), img)

    def download_tile(self, url, headers, channels):
        response = requests.get(url, headers=headers)
        arr = np.asarray(bytearray(response.content), dtype=np.uint8)

        if channels == 3:
            return cv2.imdecode(arr, 1)
        return cv2.imdecode(arr, -1)

    # Mercator projection
    # https://developers.google.com/maps/documentation/javascript/examples/map-coordinates

    def project_with_scale(self, lat, lon, scale):
        siny = np.sin(lat * np.pi / 180)
        siny = min(max(siny, -0.9999), 0.9999)
        x = scale * (0.5 + lon / 360)
        y = scale * (0.5 - np.log((1 + siny) / (1 - siny)) / (4 * np.pi))
        return x, y

    def download_image(self, lat1: float, lon1: float, lat2: float, lon2: float,
                       zoom: int, url: str, headers: dict, tile_size: int = 256, channels: int = 3) -> np.ndarray:
        """
        Downloads a map region. Returns an image stored as a `numpy.ndarray` in BGR or BGRA, depending on the number
        of `channels`.

        Parameters
        ----------
        `(lat1, lon1)` - Coordinates (decimal degrees) of the top-left corner of a rectangular area

        `(lat2, lon2)` - Coordinates (decimal degrees) of the bottom-right corner of a rectangular area

        `zoom` - Zoom level

        `url` - Tile URL with {x}, {y} and {z} in place of its coordinate and zoom values

        `headers` - Dictionary of HTTP headers

        `tile_size` - Tile size in pixels

        `channels` - Number of channels in the output image. Also affects how the tiles are converted into numpy arrays.
        """

        scale = 1 << zoom

        # Find the pixel coordinates and tile coordinates of the corners
        tl_proj_x, tl_proj_y = self.project_with_scale(lat1, lon1, scale)
        br_proj_x, br_proj_y = self.project_with_scale(lat2, lon2, scale)

        tl_pixel_x = int(tl_proj_x * tile_size)
        tl_pixel_y = int(tl_proj_y * tile_size)
        br_pixel_x = int(br_proj_x * tile_size)
        br_pixel_y = int(br_proj_y * tile_size)

        tl_tile_x = int(tl_proj_x)
        tl_tile_y = int(tl_proj_y)
        br_tile_x = int(br_proj_x)
        br_tile_y = int(br_proj_y)

        img_w = abs(tl_pixel_x - br_pixel_x)
        img_h = br_pixel_y - tl_pixel_y
        img = np.zeros((img_h, img_w, channels), np.uint8)

        def build_row(tile_y):
            for tile_x in range(tl_tile_x, br_tile_x + 1):
                tile = self.download_tile(url.format(
                    x=tile_x, y=tile_y, z=zoom), headers, channels)

                if tile is not None:
                    # Find the pixel coordinates of the new tile relative to the image
                    tl_rel_x = tile_x * tile_size - tl_pixel_x
                    tl_rel_y = tile_y * tile_size - tl_pixel_y
                    br_rel_x = tl_rel_x + tile_size
                    br_rel_y = tl_rel_y + tile_size

                    # Define where the tile will be placed on the image
                    img_x_l = max(0, tl_rel_x)
                    img_x_r = min(img_w + 1, br_rel_x)
                    img_y_l = max(0, tl_rel_y)
                    img_y_r = min(img_h + 1, br_rel_y)

                    # Define how border tiles will be cropped
                    cr_x_l = max(0, -tl_rel_x)
                    cr_x_r = tile_size + min(0, img_w - br_rel_x)
                    cr_y_l = max(0, -tl_rel_y)
                    cr_y_r = tile_size + min(0, img_h - br_rel_y)

                    img[img_y_l:img_y_r,
                        img_x_l:img_x_r] = tile[cr_y_l:cr_y_r, cr_x_l:cr_x_r]

        threads = []
        for tile_y in range(tl_tile_y, br_tile_y + 1):
            thread = threading.Thread(target=build_row, args=[tile_y])
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        return img

    def image_size(self, lat1: float, lon1: float, lat2: float,
                   lon2: float, zoom: int, tile_size: int = 256):
        """ Calculates the size of an image without downloading it. Returns the width and height in pixels as a tuple. """

        scale = 1 << zoom
        tl_proj_x, tl_proj_y = self.project_with_scale(lat1, lon1, scale)
        br_proj_x, br_proj_y = self.project_with_scale(lat2, lon2, scale)

        tl_pixel_x = int(tl_proj_x * tile_size)
        tl_pixel_y = int(tl_proj_y * tile_size)
        br_pixel_x = int(br_proj_x * tile_size)
        br_pixel_y = int(br_proj_y * tile_size)

        return abs(tl_pixel_x - br_pixel_x), br_pixel_y - tl_pixel_y
