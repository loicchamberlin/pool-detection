from pool_detection.ImageClass.dataset import Dataset
from pool_detection.ImageClass.image import Image
from pool_detection.GeoData.geodata import GeoData

from datetime import datetime
import argparse
import os


def get_input() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--address", type=str, required=True,
                        help='address you want to use to detect pools around. Example : "12\ Chemin\ des\ Gardillots,\ 33610\ Cestas,\ France"')
    parser.add_argument("--zoom", type=int, default=19,
                        required=False, help='Zoom used to download the image')
    args = parser.parse_args()
    return args


def is_folder_structures_done() -> None:
    path_list = ["./ressources/",
                 "./ressources/model/",
                 "./ressources/metadata/",
                 "./ressources/Images/Images_raw/",
                 "./ressources/Images/Images_processed/",
                 "./ressources/Images/Images_cropped/"]

    for path in path_list:
        if not (os.path.isdir(path)):
            os.mkdir(path)


if __name__ == '__main__':
    inputs = get_input()
    is_folder_structures_done()

    first_time = datetime.now()

    first_address = GeoData(inputs.address, inputs.zoom)
    first_address.download_satellite_image()

    print('Time it took to download the satellite image download : ',
          (datetime.now() - first_time).total_seconds(), 'seconds.\n')

    image_test = Image(first_address.get_filepath())
    first_dataset = Dataset(image_test, first_address)

    first_dataset.create_imagette()
    first_dataset.apply_inference()
    first_dataset.recreate_image()

    first_dataset.delete_imagette_files()

    print('Time it took to end the program : ',
          (datetime.now() - first_time).total_seconds(), 'seconds.\n')
