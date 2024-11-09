

class Metadata:
    """
    Abstract Class for storing metadata information as a single object
    Representative of the metadata that would be generated from one run through of the VISTA model once.

    Attributes:
        image_title (str): Title of the actual image file.
        title (str): Title that was generated for the image.
        abstract (str): Abstract that was generated for the image.
        total_tokens (int): Total number of tokens used to generate metadata.
        total_input_tokens (int): Total number of input tokens used to generate metadata.
        total_output_tokens (int): Total number of output tokens used to generate metadata.
    """
    def __init__(self, image_title, title, abstract, total_tokens, total_input_tokens, total_output_tokens):
        self._image_title = image_title
        self._title = title
        self._abstract = abstract
        self._total_tokens = total_tokens
        self._total_input_tokens = total_input_tokens
        self._total_output_tokens = total_output_tokens

    def get_image_title(self):
        """
        Gets the title of the actual image file.
        :return: The title of the actual image file.
        """
        return self._image_title

    def get_title(self):
        """
        Gets the title that was generated for the image.
        :return: The generated title for the image.
        """
        return self._title

    def get_abstract(self):
        """
        Gets the abstract that was generated for the image.
        :return: The generated abstract for the image.
        """
        return self._abstract


    def get_total_tokens(self):
        """
        Gets the total number of tokens used to generate metadata.
        :return: The total number of tokens used for metadata generation.
        """
        return self._total_tokens

    def get_total_input_tokens(self):
        """
        Gets the total number of input tokens used to generate metadata.
        :return: The total number of input tokens used for metadata generation
        """
        return self._total_input_tokens

    def get_total_output_tokens(self):
        """
        Gets the total number of output tokens used to generate metadata.
        :return: The total number of output tokens used for metadata generation
        """
        return self._total_output_tokens

    def get_metadata_as_list(self):
        """
        Formats the metadata contained in this object into a list
        :return: metadata contained in the object
        """
        metadata_list = [self.get_image_title(),
                         self.get_title(),
                         self.get_abstract(),
                         self.get_total_tokens(),
                         self.get_total_input_tokens(),
                         self.get_total_output_tokens()]
        return metadata_list