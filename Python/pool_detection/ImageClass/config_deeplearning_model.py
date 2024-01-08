import os

from detectron2.config import get_cfg
from detectron2 import model_zoo

# Definition of the config
def create_config(weights_path:str = None, base_lr:float = 0.002, max_iter:int = 600, batch_size_per_img:int = 512, directory_name:str = ""):

    if weights_path != None and not os.path.exists(weights_path):
        raise Exception("The path given doesn't exist. Find the correct path towards the save weights.")
    
    cfg = get_cfg()
    cfg.MODEL.DEVICE = "cuda"

    cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_DC5_3x.yaml"))
    cfg.DATASETS.TRAIN = ("pool_training")
    cfg.DATASETS.TEST = ()
    cfg.DATALOADER.NUM_WORKERS = 2
    if weights_path != None:
        cfg.MODEL.WEIGHTS = weights_path 
    else:
        cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_50_DC5_3x.yaml") 
    cfg.SOLVER.IMS_PER_BATCH = 4
    cfg.SOLVER.BASE_LR = base_lr  
    cfg.SOLVER.MAX_ITER = max_iter   
    cfg.SOLVER.STEPS = []        
    cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = batch_size_per_img   
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1 

    input_particularity = "_base_lr_" + str(base_lr) + "_max_iter_" + str(max_iter) + "_batch_size_per_img_" + str(batch_size_per_img) + "/"
    if directory_name == "":
        cfg.OUTPUT_DIR = "./ressources/model/" + input_particularity
    else:
        cfg.OUTPUT_DIR = "./ressources/model/" + directory_name + input_particularity

    return cfg