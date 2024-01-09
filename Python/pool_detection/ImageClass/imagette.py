from pool_detection.ImageClass.image import Image


class Imagette(Image):
    """
    An Imagette class for operation based on imagette.
    This class inherits the attributes and methods from the Image Class.
    Imagette can be considered as a tile from a main image.

    Attributes:
    - image_path (str): Stores the image_path from the downloaded satellite image.
    - pos_x (int): Stores the x position of the imagette from the main image.
    - pos_y (int): Stores the y position of the imagette from the main image.

    Methods:
    - get_pos_x(): Gives the position x of the imagette.
    - get_pos_y(): Gives the position y of the imagette.
    """

    def __init__(self, image_path: str, pos_x: int, pos_y: int) -> None:
        super().__init__(image_path)
        self.pos_x = pos_x
        self.pos_y = pos_y

    def get_pos_x(self) -> int:
        """
        Gives the position x of the imagette.

        Parameters:
        None.

        Returns:
        int: position x.
        """
        return self.pos_x

    def get_pos_y(self) -> int:
        """
        Gives the position y of the imagette.

        Parameters:
        None.

        Returns:
        int: position y.
        """
        return self.pos_y
