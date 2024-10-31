from image_processor import ImageProcessor
import base64
import os
import anthropic
from PIL import Image


class ClaudeImageProcessor(ImageProcessor):
    """
    Class Implementation of ImageProcessor interface for use with Claude Models
    """
    def __init__(self, file_path):
        super().__init__(file_path)

    def process_image(self):
        """
            Processes given image at self.file_path and converts it to base_64 encoding for use with Anthropic's Claude API
            Inputs:
                - None
            Outputs:
                - base_64 encoding of given image
        """
        with open(self.file_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def _greyscale_image(self):
        with Image.open(self.filepath) as img:
            greyscale_img = img.convert("L")
            greyscale_img.save(self.file_path)

    def _resize_image(self):
        with Image.open(self.file_path) as img:
            img = img.convert("RGB")

            img_size = img.size
            if img_size[0] < 1000 or img_size[1] < 1000:
                img_size = img_size # keep original size if smaller
            else:
                img_size = (1000, 1000) # resize to 1000X1000

            # resize the image
            resized_img = img.resize(img_size, Image.LANCZOS)
            resized_img.save(self.file_path, "JPEG")
