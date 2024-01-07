import cv2


class Image:
    def __init__(self, image_path: str) -> None:
        self.image_path = image_path

    def get_image(self):
        return cv2.imread(self.image_path)

    def set_image(self, new_image: cv2.Mat):
        cv2.imwrite(self.image_path, new_image)

    def save_image(self, save_path):
        cv2.imwrite(save_path, cv2.imread(self.image_path))

    def get_image_path(self):
        return self.image_path
    
    def get_size(self):
        return len(self.get_image()), len(self.get_image()[0])
