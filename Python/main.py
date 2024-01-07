from pool_detection.ImageClass.dataset import Dataset
from pool_detection.ImageClass.image import Image
from pool_detection.GeoData.geodata import GeoData
from datetime import datetime

first_time = datetime.now()

address = "12 Chemin des Gardillots, 33610 Cestas, France"

first_address = GeoData(address, 18)
first_address.download_satellite_image()

print('Time it took to download the satellite image download : ', (datetime.now() - first_time).total_seconds(), 'seconds.\n')

image_test = Image(first_address.get_filepath())
first_dataset = Dataset(image_test, first_address)

first_dataset.create_imagette()
first_dataset.apply_inference()
first_dataset.recreate_image()

first_dataset.delete_imagette_files()

last_time = datetime.now()

print('Time it took to end the program : ', (last_time - first_time).total_seconds(), 'seconds.\n')