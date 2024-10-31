from abc import ABC, abstractmethod


class ImageDescriptionModel(ABC):
    """
    Interface for classes that generate image description informatino
    Ie: Titles, Abstracts, Subjects
    """
    def __init__(self, image_file):
        self.image_file = image_file
        self.title_token_data = None
        self.abstract_token_data = None
        self.raw_context = ""
        with open("../../title_prompt.txt", "r") as file:
            self.title_generation_prompt = file.read()
        with open("../../abstract_prompt.txt", "r") as file:
            self.abstract_generation_prompt = file.read()


    @abstractmethod
    def generate_title(self):
        """
        Generates title for the given image object (self.image_file)
        Inputs:
            - None
        Outputs:
            - self.title - String representing the title of the image object
            - self.title_token_data is initialized with the number of tokens in this API request
        """
        pass

    @abstractmethod
    def generate_abstract(self):
        """
        Generates abstract for the given image object (self.image_file)
        Inputs:
            - None
        Outputs:
            - self.abstract - String representing the title of the image object
            - self.abstract_token_data is initialized with the number of tokens in this API request
        """
        pass

    @abstractmethod
    def get_total_tokens(self):
        """
        Gets the total number of tokens used in both the abstract and title requests
        Inputs:
            - None
        Outputs:
            - Returns total number of tokens used
            OR
            - Returns message indicating that no abstract requests have been made yet
            OR
            - Returns message indicating that no title requests have been made yet
        """
        pass

