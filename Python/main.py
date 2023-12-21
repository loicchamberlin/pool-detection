from pool_detection.ImageClass.dataset import Dataset
from pool_detection.ImageClass.image import Image

path2img = "./ressources/Images/Images_raw/gojo4k.jpg"
name = "GOJO"

image_test = Image(path2img, name)
first_dataset = Dataset(image_test)

first_dataset.create_imagette()

first_dataset.apply_inference()
first_dataset.recreate_image()

first_dataset.delete_imagette_files()
