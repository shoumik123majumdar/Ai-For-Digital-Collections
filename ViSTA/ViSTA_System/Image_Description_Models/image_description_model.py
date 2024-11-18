from abc import ABC, abstractmethod


class ImageDescriptionModel(ABC):
    """
    Interface for classes that generate image description informatino
    Ie: Titles, Abstracts, Subjects
    """
    def __init__(self,title_prompt_file,abstract_prompt_file):
        self.total_tokens = 0
        self.input_tokens = 0
        self.output_tokens = 0
        self.abstract_token_data = None
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
            - self.title - String representing the title of the image object
            - self.title_token_data is initialized with the number of tokens in this API request
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
        return self.total_tokens

    def reset_token_counts(self):
        """
        Resets token counts to zero.
        """
        self.total_tokens = 0
        self.input_tokens = 0
        self.output_tokens = 0
