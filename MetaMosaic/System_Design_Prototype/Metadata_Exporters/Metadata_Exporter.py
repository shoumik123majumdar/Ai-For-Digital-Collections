from abc import ABC, abstractmethod


class MetadataExporter(ABC):
    """
    Interface for classes that package and export metadata information
    """
    def __init__(self,file_name,title,abstract,transcription_information,token_information):




    @abstractmethod
    def generate_title(self):

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
