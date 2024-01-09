import requests
import json
import cv2
import os

from pool_detection.utils.image_downloading import download_image


class GeoData:
    """
    A Geospatial Data class for operation based on geolocalisation problematic.

    Attributes:
    - address (str): Stores the address given from the user.
    - longitude (float): Stores the information about the longitude of the address.
    - latitude (float): Stores the information about the latitude of the address.
    - topleft_geoloc (float, float) : Stores the information about the top left geolocalisation of the address.
    - bottomright_geoloc (float, float): Stores the information about the bottom right geolocalisation of the address.
    - zoom (int < 21): Stores the information about the zoom chosen to download the image.
    - path_to_main_image (str): Stores the information about the path to where the satellite main image is saved.
    - filename (str): Stores the information about the file name.

    Methods:
    - get_address(): Gives the address string.
    - get_filepath(): Gives the filepath to the main image.
    - get_longitude(): Gives the longitude of the address.
    - get_latitude(): Gives the latitude of the address.
    - get_topleft_geoloc(): Gives the (longitude, latitude) of the top left corner of the image downloaded.
    - get_bottomright_geoloc(): Gives the (longitude, latitude) of the bottom right corner of the image downloaded.
    - retrieve_geolocalisation(): Converts the address into longitude, latitude if possible.
    - download_satellite_image(): Downloads and saves the satellite image.
    - convert_pixel_to_geolocalisation(x,y): Converts pixel position of a pool detected into its geolocalisation (longitude, latitude)
    """

    def __init__(self, address: str, zoom: int = 20) -> None:
        """
        Initialisation of the class GeoData

        Parameters:
        - address (str): Address chosen by the user.
        - zoom (int): Zoom used for the spatial resolution of the satellite image.
        ...

        Returns:
        None.
        """
        self.address = address
        self.longitude = 0
        self.latitude = 0
        self.topleft_geoloc = (0, 0)
        self.bottomright_geoloc = (0, 0)
        self.zoom = zoom
        self.path_to_main_image = "./ressources/Images/Images_raw/"
        self.filename = ""

    def get_address(self) -> str:
        """
        Get the address from the class.

        Parameters:
        None.

        Returns:
        str: address given by the user at the initialisation of the class.
        """
        return self.address

    def get_filepath(self) -> str:
        """
        Get the file path where the image is saved.

        Parameters:
        None.

        Returns:
        str: Image directory path.
        """
        return self.path_to_main_image + self.filename

    def get_longitude(self) -> float:
        """
        Get the longitude from the class.

        Parameters:
        None.

        Returns:
        float: longitude retrieved by the function retrieve_geolocalisation().
        """
        return self.longitude

    def get_latitude(self) -> float:
        """
        Get the latitude from the class.

        Parameters:
        None.

        Returns:
        float: latitude retrieved by the function retrieve_geolocalisation().
        """
        return self.latitude

    def get_topleft_geoloc(self) -> (float, float):
        """
        Get the top left geolocalisation calculated from the class.
        This information helps to know the spatial resolution in the function
        convert_pixel_to_geolocalisation(x,y).

        Parameters:
        None.

        Returns:
        (float, float): (longitude, latitude) of the top left corner of the image.
        """
        return self.topleft_geoloc

    def get_bottomright_geoloc(self) -> (float, float):
        """
        Get the bottom right geolocalisation calculated from the class.
        This information helps to know the spatial resolution in the function
        convert_pixel_to_geolocalisation(x,y).

        Parameters:
        None.

        Returns:
        (float, float): (longitude, latitude) of the bottom right corner of the image.
        """
        return self.bottomright_geoloc

    def retrieve_geolocalisation(self) -> None or print:
        """
        This function get a string that corresponds to a real address. 
        It uses geocode api to retrieve the corresponding geolocalisation (longitude, latitude)

        Parameters:
        None.

        Returns:
        If no error: None -> Data is being saved within the function.
        Else: print -> Print an error to the user.

        """
        # converting the address
        address_withplus = self.address.replace(' ', '+')
        geocode_api_key = os.environ['GEOCODE_API_KEY']

        try:
            url = f'https://geocode.maps.co/search?q={address_withplus}&api_key={geocode_api_key}'
            # print(url)
            r = requests.get(url)

            my_json = r.content.decode('utf-8')
            data = json.loads(my_json)

            self.latitude = float(data[0]['lon'])
            self.longitude = float(data[0]['lat'])

            self.bottomright_geoloc = (
                self.longitude - 0.002, self.latitude + 0.003)
            self.topleft_geoloc = (
                self.longitude + 0.002, self.latitude - 0.003)
        except:
            return print(f'The address : {self.address} is invalid.')

    def download_satellite_image(self):
        """
        Using the information for the geolocalisation of the address given by the 
        user, this function is used to download the satellite image using google_api.

        It saves the image downloaded at a path predefined (self.path_to_main_image)
        using the address, the zoom as name to save it. 

        Parameters:
        None.

        Returns:
        (float, float): (longitude, latitude) of the top left corner of the image.
        """
        self.filename = self.address.replace(',', '_').replace(
            ' ', '_').replace('__', '_') + '_zoom_' + str(self.zoom) + ".jpg"

        self.retrieve_geolocalisation()

        if not (os.path.isfile(self.path_to_main_image + self.filename)):

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

    def convert_pixel_to_geolocalisation(self, x: int, y: int) -> (float, float):
        """
        Convert the pixel localisation of pools detected into geolocalisation using
        Top Left and Bottom Right information. It is used to list the geospatial
        to the user.

        Parameters:
        x (int): horizontal position in the image (origin of the axis: top left)
        y (int): vertical position in the image (origin of the axis: top left)

        Returns:
        (float, float): (longitude, latitude) of the pool detected at (x, y).
        """
        # Add test to verify if the coord pixel (x,y) are in the image given
        # Add test to verify if the image exists in the path
        img = cv2.imread(self.get_filepath())

        width, height = len(img), len(img[0])
        width_geoloc, height_geoloc = self.bottomright_geoloc[0] - \
            self.topleft_geoloc[0], self.bottomright_geoloc[1] - \
            self.topleft_geoloc[1]

        res_x, res_y = width_geoloc / width, height_geoloc / height

        return (self.topleft_geoloc[0] + x * res_x, self.topleft_geoloc[1] + y * res_y)
