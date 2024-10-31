from abc import ABC, abstractmethod
from PIL import Image

class ImageProcessor(ABC):
    """
    Interface for classes that handle image pre-processing before feeding images into an AI model
    """
    def __init__(self, file_path):
        self.file_path = file_path

    @abstractmethod
    def process_image(self):
        """
            Takes file at self.file_path and stores it within new_location for use within the data pipeline
            Depending on the AI Model being used, necessary pre_processing for the image will be applied before image is stored
            Ie: encoded into base_64 for Anthropic models.
            Inputs:
                - None
            Outputs:
                - None
        """
        pass

    #Current thumbnail image size estimate: 391 × 500 pixels
    #Current downloaded zip file image size: 4551 × 5873 pixels
    @abstractmethod
    def _resize(self,width,height):
        """
        Helper Function: takes image file and resize it to given width and height for optimal VLM processing
        Scale down to minimum required image size (given width and height
        Ie: For Gemini model, scale to 3072x3072
        Ie: For Claude, scale to 1000x1000
        Inputs:
            - width: maximum image width for processing
            - height: maximum image height for processing
        Outputs:
            - resized image file (JPEG)
        """
        with Image.open(self.file_path) as img:
            img = img.convert("RGB")

            img_size = img.size
            if img_size[0] < width or img_size[1] < height:
                img_size = img_size # keep original size if smaller
            else:
                img_size = (width, height) # resize to 1000X1000

            # resize the image
            resized_img = img.resize(img_size, Image.LANCZOS)
            resized_img.save(self.file_path, "JPEG")

    @abstractmethod
    def _grayscale(self):
        """
        Helper function: takes image file and converts it to grayscale
        Inputs:
            - None
        Outputs:
            - grayscaled image file
        """
        with Image.open(self.filepath) as img:
            greyscale_img = img.convert("L")
            greyscale_img.save(self.file_path)
