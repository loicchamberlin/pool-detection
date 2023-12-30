from pool_detection.ImageClass.image import Image
from pool_detection.ImageClass.imagette import Imagette


import cv2
import os
import numpy as np
import torch
import torchvision

from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import Visualizer
# Definition of the config
def create_config(weights_path:str, base_lr:float = 0.002, max_iter:int = 600, batch_size_per_img:int = 512):
    if not os.path.exists(weights_path):
        raise Exception("The path given doesn't exist. Find the correct path towards the save weights.")
    
    cfg = get_cfg()
    cfg.MODEL.DEVICE = "cuda"

    cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_DC5_3x.yaml"))
    cfg.DATASETS.TRAIN = ("pool_training")
    cfg.DATASETS.TEST = ()
    cfg.DATALOADER.NUM_WORKERS = 2
    cfg.MODEL.WEIGHTS = weights_path # Let training initialize from model zoo
    cfg.SOLVER.IMS_PER_BATCH = 4
    cfg.SOLVER.BASE_LR = base_lr  # pick a good LR
    cfg.SOLVER.MAX_ITER = max_iter    # 300 iterations seems good enough for this toy dataset; you will need to train longer for a practical dataset
    cfg.SOLVER.STEPS = []        # do not decay learning rate
    cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = batch_size_per_img   # faster, and good enough for this toy dataset (default: 512)
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1  # only has one class (ballon). (see https://detectron2.readthedocs.io/tutorials/datasets.html#update-the-config-for-new-datasets)
    return cfg


class Dataset:
    path_to_imagette = "./ressources/Images/Images_cropped/"
    path_to_main_image = "./ressources/Images/Images_raw/"

    def __init__(self, main_image: Image) -> None:
        self.main_image = main_image
        self.list_imagette = []
        self.length = 0

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
            v = Visualizer(imagette_tmp[:, :, ::-1], scale=1)
            out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
            imagette.set_image(out.get_image()[:, :, ::-1])
