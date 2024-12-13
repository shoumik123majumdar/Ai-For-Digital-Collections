from .image_processor import ImageProcessor
import base64
import anthropic
import os
from PIL import Image


class ClaudeImageProcessor(ImageProcessor):
    """
    Class Implementation of ImageProcessor interface for use with Claude Models
    """
    def __init__(self):
        API_KEY = os.environ.get('CLAUDE_KEY')
        self.client = anthropic.Anthropic(api_key=API_KEY)

    def process_image(self, file_path):
        """
            Processes given image at self.file_path and converts it to base_64 encoding for use with Anthropic's Claude API
            Inputs:
                - None
            Outputs:
                - base_64 encoding of given image
        """
        self._greyscale_image()
        self._resize_image()
        with open(file_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def _greyscale_image(self, file_path):
        super()._grayscale(file_path)

    def _resize_image(self, file_path, width, height):
        super()._resize(file_path, width, height)
