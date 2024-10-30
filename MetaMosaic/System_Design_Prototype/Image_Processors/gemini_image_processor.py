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
        self._grayscale() # Turns the image grayscale (saved in same location)
        self._resize() # Resizes the image (saved in same location)
        return genai.upload_file(self.file_path)

    def _grayscale(self):
        with Image.open(self.file_path) as img:
            grayscale_img = img.convert("L")
            grayscale_img.save(self.file_path)

    def _resize(self):
        with Image.open(self.file_path) as img:
            img = img.convert('RGB') #Makes sure it is possible to convert this image object into a JPEG later in the code

            image_size = img.size
            if image_size[0] < 3072 or image_size[1] < 3072:
                image_size = image_size  # Keep the original size if it's smaller
            else:
                image_size = (3072, 3072)  # Resize to 3072x3072

            #Resize the image
            resized_img = img.resize(image_size, Image.ANTIALIAS)
            resized_img.save(self.file_path)
