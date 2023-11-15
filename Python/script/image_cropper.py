import cv2
import argparse
import os

def img_cropper(save_path, image_path, image_name,resolution=224, size=448):
    img = cv2.imread(image_path)
    height, width = len(img), len(img[0])

    for i in range(0,height//size):
        for j in  range(0,width//size):
            img_tmp = cv2.resize(img[i*size:(i+1)*size,j*size:(j+1)*size,:], (resolution,resolution))
            cv2.imwrite(filename=f"{save_path}/{image_name}_x{i}_y{j}.jpg", img=img_tmp)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--save_path", type=str, required=True, help='Saving path where you want to save your images cropped')
    parser.add_argument("--image_name", type=str, required=True, help='Beginning of the image name that will be saved with for all cropped image')
    parser.add_argument("--image_path", type=str, required=True, help='The path of the image you want to cropped')
    parser.add_argument("--resolution", type=int, default=224, required=False, help='Resolution your image will have once saved')
    parser.add_argument("--size", type=int, default=448, required=False, help='Size which will be used to cropped your image before resizing')
    args = parser.parse_args() 

    if not os.path.exists(args.save_path):
        raise Exception("The path given doesn't exist. Either change the path, or create the directory associated.")
    
    if not os.path.exists(args.image_path):
        raise Exception("The path given for the image doesn't exist.")

    img_cropper(args.save_path, args.image_path, args.image_name, args.resolution, args.size)

    print(f'You can find your images cropped in : {args.save_path}')