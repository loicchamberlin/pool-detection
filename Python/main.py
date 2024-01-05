from pool_detection.ImageClass.dataset import Dataset
from pool_detection.ImageClass.image import Image
from pool_detection.GeoData.geodata import GeoData
from datetime import datetime

first_time = datetime.now()

address = "12 Chemin des Gardillots, 33610 Cestas, France"

first_address = GeoData(address)
first_address.download_satellite_image()

print('time difference during sattelite image download : ', (datetime.now() - first_time).total_seconds(), 'seconds')

image_test = Image(first_address.get_filepath(), 'ychoux maison test zoom 20 size 448')
first_dataset = Dataset(image_test, first_address)

first_dataset.create_imagette()
first_dataset.apply_inference()
first_dataset.recreate_image()

last_time = datetime.now()

print('Time it took to end the program : ', (last_time - first_time).total_seconds(), 'seconds')