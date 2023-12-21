from pool_detection.ImageClass.image import Image
from pool_detection.ImageClass.imagette import Imagette

import cv2
import os


class Dataset:
    length = 0
    path_to_imagette = "./ressources/Images/Images_cropped/"
    path_to_main_image = "./ressources/Images/Images_raw/"

    def __init__(self, main_image: Image) -> None:
        self.main_image = main_image
        self.list_imagette = []

    def list_dataset(self):
        for index, imagette in enumerate(self.list_imagette):
            print(
                f"Here's lie the image number {index} : {imagette[index].get_image_name()} \n")

    def get_main_image(self):
        pass

    def create_imagette(self):
        print(self.main_image.get_image_name())
        image_to_crop = self.main_image.get_image()
        resolution = 224
        size = 448

        height = len(image_to_crop)
        width = len(image_to_crop[0])

        imgette_number_width = width // size
        imgette_number_height = height // size

        for i in range(0, imgette_number_height):
            for j in range(0, imgette_number_width):
                imagette_tmp_name = self.main_image.get_image_name() + \
                    f"_x_{i}_y_{j}.jpg"

                imagette_tmp_path = self.path_to_imagette + imagette_tmp_name

                image_cropped = cv2.resize(
                    image_to_crop[i*size:(i+1)*size, j*size:(j+1)*size, :], (resolution, resolution))
                cv2.imwrite(
                    filename=f"{self.path_to_imagette}/{self.main_image.get_image_name()}_x_{i}_y_{j}.jpg", img=image_cropped)

                imagette_tmp = Imagette(
                    imagette_tmp_path, imagette_tmp_name, i, j)

                self.list_imagette.append(imagette_tmp)

    def delete_imagette_files(self):
        for imagette_path in os.listdir(self.path_to_imagette):
            os.remove(self.path_to_imagette + imagette_path)

    def recreate_image(self):
        maxX, maxY = 0, 0
        for imagette in self.list_imagette:
            maxX = max(maxX, imagette.get_pos_x())
            maxY = max(maxY, imagette.get_pos_y())

        compositeHeight = (maxX + 1) * len(self.list_imagette[0].get_image())
        compositeWidth = (maxY + 1) * len(self.list_imagette[0].get_image()[0])

    def apply_inference(self):
        pass
