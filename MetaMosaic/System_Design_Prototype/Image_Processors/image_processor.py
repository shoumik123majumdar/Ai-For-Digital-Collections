from abc import ABC, abstractmethod


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
    #Current downloaded zip file image size:
    @abstractmethod
    def resize(self):
        """
        Helper Function to takes image file and resize it for optimal VLM processing
        Scale up for maximum output effectiveness
        Ie: For Gemini model, scale to 3072x3072
        Inputs:
            - None
        Outputs:
            - resized image file
        """
        pass

    @abstractmethod
    def grayscale(self):
        """
        Helper function that takes image file and converts it to grayscale
        Inputs:
            - None
        Outputs:
            - grayscaled image file
        """
        pass
