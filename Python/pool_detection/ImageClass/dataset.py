from pool_detection.ImageClass.image import Image
from pool_detection.ImageClass.imagette import Imagette
from pool_detection.GeoData.geodata import GeoData
from pool_detection.ImageClass.config_deeplearning_model import create_config

import cv2
import os
import numpy as np
from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import Visualizer


class Dataset:
    path_to_imagette = "./ressources/Images/Images_cropped/"
    path_to_main_image = "./ressources/Images/Images_raw/"

    def __init__(self, main_image: Image, address: GeoData) -> None:
        self.main_image = main_image
        self.address = address
        self.list_imagette = []
        self.length = 0
        self.number_of_pools = 0
        self.list_coordinates_pools = []
        self.list_geocoordinates_pools = []

    def list_dataset(self):
        for index, imagette in enumerate(self.list_imagette):
            print(
                f"Here's lie the image number {index} : {imagette[index].get_image_name()} \n")

    def get_main_image(self):
        pass

    def create_imagette(self):
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
                self.length += 1

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
            
        
        for coord in self.list_coordinates_pools:
            image_[coord[1]-5:coord[1]+5, coord[0]-5:coord[0]+5] = (0,0,255)

        cv2.imwrite("./ressources/Images/Images_processed/" +
                    self.main_image.get_image_name() + "_processed.jpg", image_)

    def apply_inference(self):
        cfg = create_config(weights_path="./output/model_final.pth")
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7   # set a custom testing threshold
        predictor = DefaultPredictor(cfg)

        for imagette in self.list_imagette:
            # add bounding box from the inference data
            imagette_tmp = imagette.get_image()

            outputs = predictor(imagette_tmp)  # format is documented at https://detectron2.readthedocs.io/tutorials/models.html#model-output-format

            for output in outputs["instances"].get('pred_boxes'):
                output = output.cpu().numpy()

                x, y = imagette.get_pos_x(), imagette.get_pos_y()

                pos_x_tl = output[0]
                pos_y_tl = output[1]
                pos_x_br = output[2]
                pos_y_br = output[3]

                mid_pos_x = (pos_x_tl + pos_x_br) / 2
                mid_pos_y = (pos_y_tl + pos_y_br) / 2

                height, width = imagette.get_size()

                coord_x, coord_y = int(mid_pos_x + height * y), int(mid_pos_y + width * x)

                geoloc_x, geoloc_y = self.address.convert_pixel_to_geolocalisation(coord_x, coord_y) 

                self.list_coordinates_pools.append((coord_x, coord_y))
                self.list_geocoordinates_pools.append((geoloc_x, geoloc_y))
                self.number_of_pools +=1


            v = Visualizer(imagette_tmp[:, :, ::-1], scale=1)
            out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
            imagette.set_image(out.get_image()[:, :, ::-1])


        print(self.number_of_pools)
        print('')
        print(self.list_coordinates_pools)
        print('')
        print(self.list_geocoordinates_pools)


