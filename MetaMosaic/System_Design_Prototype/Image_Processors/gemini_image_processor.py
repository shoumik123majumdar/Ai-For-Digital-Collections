from image_processor import ImageProcessor
import google.generativeai as genai
import os
from PIL import Image

class GeminiImageProcessor(ImageProcessor):
    """
    Class Implementation of ImageProcessor interface for use with Gemini Models
    """
    def __init__(self, file_path):
        super().__init__(file_path)
        API_KEY = os.environ.get("GOOG_KEY")
        genai.configure(api_key = API_KEY)

    def process_image(self):
        """
            Uploads given image to Gemini API as a JPEG

            Inputs:
                - None
            Outputs:
                - image file object
        """
        return genai.upload_file(self.file_path)

    def grayscale(self):
        with Image.open(self.file_path) as img:
            grayscale_img = img.convert("L")
            return grayscale_img

    def resize(self):
