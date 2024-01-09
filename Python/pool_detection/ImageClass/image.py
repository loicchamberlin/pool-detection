import cv2


class Image:
    """
    An Image class for operation based on image.

    Attributes:
    - image_path (str): Stores the image_path from the downloaded satellite image.

    Methods:
    - get_image(): Gives the image using OpenCV.
    - set_image(new_image): Rewrites the image stored by a new one.
    - save_image(save_path): Saves an image to a chosen path.
    - get_image_path(): Gives the image path.
    - get_size(): Gives the height and width of the image.
    """

    def __init__(self, image_path: str) -> None:
        self.image_path = image_path

    def get_image(self) -> cv2.Mat:
        """
        Reads the image using OpenCV.

        Parameters:
        None.

        Returns:
        cv2.Mat: Image read from the image_path information.
        """
        return cv2.imread(self.image_path)

    def set_image(self, new_image: cv2.Mat) -> None:
        """
        Rewrites the image stored at image path using OpenCV.

        Parameters:
        - new_image (cv2.Mat): Matrix of a new image to saved instead of the old one.

        Returns:
        None.
        """
        cv2.imwrite(self.image_path, new_image)

    def save_image(self, save_path: str) -> None:  # is this function even used ?
        """
        Save the image stored at a certain path using OpenCV.

        Parameters:
        - save_path (str): Path to the new image saved (might have a new name also).

        Returns:
        None.
        """
        cv2.imwrite(save_path, cv2.imread(self.image_path))

    def get_image_path(self) -> str:
        """
        Gives the image path.

        Parameters:
        None.

        Returns:
        str: Image path to the image
        """
        return self.image_path

    def get_size(self) -> (int, int):
        """
        Gives the height and width of the image.

        Parameters:
        None.

        Returns:
        (int, int): Couple of int giving height and width of the image
        """
        image = self.get_image()
        return len(image), len(image[0])
