from pool_detection.ImageClass.image import Image
from pool_detection.ImageClass.imagette import Imagette
from pool_detection.GeoData.geodata import GeoData


import cv2
import os
import numpy as np


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

        image_ = np.zeros((compositeHeight, compositeWidth, 3), dtype='uint8')

        for imagette in self.list_imagette:
            imagette_height = len(self.list_imagette[0].get_image())
            imagette_width = len(self.list_imagette[0].get_image()[0])
            image_[imagette.get_pos_x() * imagette_height:(imagette.get_pos_x()+1) * imagette_height,
                   imagette.get_pos_y() * imagette_width:(imagette.get_pos_y()+1) * imagette_width] = imagette.get_image()

        cv2.imwrite("./ressources/Images/Images_processed/" +
                    self.main_image.get_image_name() + "_processed.jpg", image_)

    def apply_inference(self):
        for imagette in self.list_imagette:
            # simple modification of the imagette, next thing is to
            # add bounding box from the inference data
            pt1 = (20, 20)
            pt2 = (200, 200)
            imagette_tmp = imagette.get_image()
            cv2.rectangle(imagette_tmp, pt1, pt2, (0, 0, 255), 2)

            imagette.set_image(imagette_tmp)
