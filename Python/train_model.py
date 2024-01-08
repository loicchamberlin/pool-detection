import detectron2
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.engine import DefaultTrainer
from detectron2.structures import BoxMode 
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import xml.etree.ElementTree as ET
import os
import argparse, json

from pool_detection.ImageClass.config_deeplearning_model import create_config

def parse_xml(img_dir, file, index):
    tree = ET.parse(file)
    root = tree.getroot()

    file_dict = {}

    file_dict["file_name"] = os.path.join(img_dir.replace('labels', 'images'), root.find('filename').text)
    file_dict["height"] = int(root.find("size/height").text)
    file_dict["width"] = int(root.find("size/width").text)
    file_dict["image_id"] = index

    list_with_all_boxes = []
    for boxes in root.iter('object'):
        ymin, xmin, ymax, xmax = None, None, None, None
        
        ymin = round(float(boxes.find("bndbox/ymin").text))
        xmin = round(float(boxes.find("bndbox/xmin").text))
        ymax = round(float(boxes.find("bndbox/ymax").text))
        xmax = round(float(boxes.find("bndbox/xmax").text))

        obj = {
            "bbox": [xmin, ymin, xmax, ymax],
            "bbox_mode": BoxMode.XYXY_ABS,
            "category_id": 0,
        }
        list_with_all_boxes.append(obj)
    file_dict["annotations"] = list_with_all_boxes
    return file_dict

def parse_dir_xml(annotation_folder):
    fichiers = [f for f in os.listdir(annotation_folder) if os.path.isfile(os.path.join(annotation_folder, f))]
    dataset_dicts = []
    index = 0

    for data in fichiers:
        record = parse_xml(annotation_folder ,os.path.join(annotation_folder, data), index)
        dataset_dicts.append(record)
        index += 1
    return dataset_dicts

def register_metadatacatalog():
    for d in ["training", "testing"]:
        DatasetCatalog.register("pool_" + d, lambda d=d: parse_dir_xml("./Images/pool_dataset_extended/" + d + "/labels/"))
        MetadataCatalog.get("pool_" + d).set(thing_classes=["pool"])

def save_metadatacatalog(pool_metadata_json:dict, name:str = "Metadata.json"):
    json_object = json.dumps(pool_metadata_json, indent=4)
    with open("./ressources/metadata/pool_metadata.json", "w") as outfile:
        outfile.write(json_object)

def get_input():
    parser = argparse.ArgumentParser()
    # parser.add_argument("--save_path", type=str, default="./ressources/Images/Images_processed/" ,required=False, help='Saving path where you want to save the processed image')
    parser.add_argument("--model_directory", type=str, required=True, help='Directory name where the model will be saved. Example : "PoolDetection"')
    parser.add_argument("--base_lr", type=float, default=0.002, help='Value for the learning rate')
    parser.add_argument("--max_iter", type=int, default=600, required=False, help='Value for the max_iteration parameter')
    parser.add_argument("--batch_size_per_image", type=int, default=512, required=False, help='Value for the number of images processed at each operation')
    args = parser.parse_args() 
    return args

def is_folder_structures_done():
    path_list = ["./ressources/",
                 "./ressources/model/",
                 "./ressources/metadata/",
                 "./ressources/Images/Images_raw/",
                 "./ressources/Images/Images_processed/",
                 "./ressources/Images/Images_cropped/"]
    
    for path in path_list:
        if not (os.path.isdir(path)):
            os.mkdir(path)

if __name__ == "__main__":
    inputs = get_input()


    # Registering the data for the DatasetCatalog and MetadataCatalog
    register_metadatacatalog()
    pool_metadata = MetadataCatalog.get("pool_training")

    # Saving the metadata of the Dataset
    save_metadatacatalog(pool_metadata_json=pool_metadata.as_dict())

    # creation of the config file
    cfg = create_config(base_lr=inputs.base_lr, max_iter=inputs.max_iter, batch_size_per_img=inputs.batch_size_per_image, directory_name=inputs.model_directory)

    os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
    trainer = DefaultTrainer(cfg)

    # Training the model
    trainer.resume_or_load(resume=False)
    trainer.train()