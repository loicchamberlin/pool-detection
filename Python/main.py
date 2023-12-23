from pool_detection.ImageClass.dataset import Dataset
from pool_detection.ImageClass.image import Image
from pool_detection.GeoData.geodata import GeoData

path2img = "./ressources/Images/Images_raw/gojo4k.jpg"
name = "GOJO"
address = "Mairie,40660 Messanges, France"

image_test = Image(path2img, name)
first_dataset = Dataset(image_test)
first_address = GeoData(address)

first_dataset.create_imagette()
first_dataset.apply_inference()
first_dataset.recreate_image()

first_address.retrieve_geolocalisation()
print('longitude : ', first_address.get_longitude())
print('latitude : ', first_address.get_latitude())

print('TL : ', first_address.get_topleft_geoloc())
print('BR : ', first_address.get_bottomright_geoloc())

first_address.download_satellite_image()
