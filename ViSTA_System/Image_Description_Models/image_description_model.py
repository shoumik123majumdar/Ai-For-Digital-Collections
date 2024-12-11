from abc import ABC, abstractmethod


class ImageDescriptionModel(ABC):
    """
    Interface for classes that generate image description informatino
    Ie: Titles, Abstracts, Subjects
    """
    def __init__(self,title_prompt_file,abstract_prompt_file,token_tracker):
        self.token_tracker = token_tracker
        with open(title_prompt_file, "r") as file:
            self.title_generation_prompt = file.read()
        with open(abstract_prompt_file, "r") as file:
            self.abstract_generation_prompt = file.read()


    @abstractmethod
    def generate_title(self,image_file,context=""):
        """
        Generates title for the given image object (self.image_file)
        Inputs:
            - image_file: image object you want to generate an title for
            - context: additional context you want to add to generation request
        Outputs:
            - title: String representing the title of the image object
            - self.token_tracker is updated to reflect new token counts
        """
        pass

    @abstractmethod
    def generate_abstract(self,image_file,context=""):
        """
        Generates abstract for the given image object (self.image_file)
        Inputs:
            - image object you want to generate an abstract for
            - context: additional context you want to add to generation request
        Outputs:
            - abstract: String representing the title of the image object
            - self.token_tracker is updated to reflect new token counts        """
        pass