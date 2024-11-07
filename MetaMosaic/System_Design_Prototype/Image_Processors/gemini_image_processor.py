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
        #self._grayscale() ONLY GRAYSCALE IF IMAGE IS A BACK_IMAGE
        self._resize(3072,3072) # Resizes the image (saved in same location)
        return genai.upload_file(self.file_path)

    def _grayscale(self):
        super()

    def _resize(self,width,height):
        super(width,height)
    #Look into resizing image too much
