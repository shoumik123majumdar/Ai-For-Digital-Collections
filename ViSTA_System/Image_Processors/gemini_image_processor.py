from .image_processor import ImageProcessor
import google.generativeai as genai
import os
from PIL import Image

class GeminiImageProcessor(ImageProcessor):
    """
    Class Implementation of ImageProcessor interface for use with Gemini Models
    """
    def __init__(self):
        API_KEY = os.environ.get("GOOG_KEY")
        genai.configure(api_key = API_KEY)

    def process_image(self,file_path):
        """
            Uploads given image to Gemini API as a JPEG

            Inputs:
                - file_path: image file path
            Outputs:
                - image file object
        """
        #self._grayscale() ONLY GRAYSCALE IF IMAGE IS A BACK_IMAGE
        self._resize(file_path,3072,3072) # Resizes the image (saved in same location)
        return genai.upload_file(file_path)

    def _grayscale(self,file_path):
        super()._grayscale(file_path)

    def _resize(self,file_path,width,height):
        super()._resize(file_path,width,height)
    #Look into resizing image too much
