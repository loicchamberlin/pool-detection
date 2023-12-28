from pool_detection.ImageClass.dataset import Dataset
from pool_detection.ImageClass.image import Image
from pool_detection.GeoData.geodata import GeoData

address = "Mairie, Bordeaux 33000, France"


first_address = GeoData(address)
first_address.download_satellite_image()

image_test = Image(first_address.get_filepath(), 'test')
first_dataset = Dataset(image_test)

first_dataset.create_imagette()
first_dataset.apply_inference()
first_dataset.recreate_image()
