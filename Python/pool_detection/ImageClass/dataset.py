from image import Image
from imagette import Imagette

import cv2
import os


class Dataset:
    length = 0
    path_to_imagette = "./ressources/Images/Images_cropped/"
    path_to_main_image = "./ressources/Images/Images_raw/"
    list_imagette = []

    def __init__(self, main_image: Image) -> None:
        self.main_image = main_image

    def list_dataset(self):
        for index, imagette in enumerate(self.list_imagette):
            print(
                f"Here's lie the image number {index} : {imagette[index].get_image_name()} \n")

    def get_main_image():
        pass

    def create_imagette():
        pass

    def delete_imagette_files():
        for imagette_path in os.listdir():
            print(imagette_path)

    def recreate_image():
        pass

    def apply_inference():
        pass
