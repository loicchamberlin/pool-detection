from pool_detection.ImageClass.image import Image


class Imagette(Image):
    def __init__(self, image_path: str, pos_x: int, pos_y: int) -> None:
        super().__init__(image_path)
        self.pos_x = pos_x
        self.pos_y = pos_y

    def get_pos_x(self):
        return self.pos_x

    def get_pos_y(self):
        return self.pos_y
