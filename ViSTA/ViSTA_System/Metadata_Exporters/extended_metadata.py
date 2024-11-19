from httplib2.auth import token

from .metadata import Metadata

class ExtendedMetadata(Metadata):
    """
    Class for storing metadata information as a single object
    Representative of the metadata that would be generated from one run through of the VISTA model with both a front and back image.

    Attributes:
        image_title (str): Title of the actual image file.
        title (str): Title that was generated for the image.
        abstract (str): Abstract that was generated for the image.
        transcription: Transcription object that was generated for the image.
        token_tracker = TokenTracker object that was used to track the token usage when generating the metadata
    """
    def __init__(self, image_title, title, abstract, transcription,token_tracker):
        super().__init__(image_title,title,abstract,token_tracker)
        self._transcription = transcription

    def get_transcription(self):
        """
        Gets the full transcription (including photographer name and dates) that was generated for the image.
        :return: The generated transcription for the image.
        """
        return self._transcription.transcription

    def get_photographer_name(self):
        """
        Gets the photographer name scanned from the back image by the transcription model
        :return: photographer name
        """
        return self._transcription.extract_names()

    def get_primary_date(self):
        """
        Gets the earliest date scanned from the back image by the transcription model
        :return: The earliest date
        """
        dates = self._transcription.extract_dates()
        if dates == "":
            return ""
        else:
            return dates[0]


    def get_secondary_date(self):
        """
        Gets the second-earliest date scanned from the back image by the transcription model
        :return: second-earliest date
        """
        dates = self._transcription.extract_dates()
        if dates == "":
            return ""
        if len(dates)>1:
            return dates[1]
        else:
            return ""

    def get_metadata_as_list(self):
        """
        Formats the metadata contained in this object into a list
        :return: metadata contained in the object
        """
        metadata_list = [self.get_image_title(),
                         self.get_title(),
                         self.get_abstract(),
                         self.get_photographer_name(),
                         self.get_primary_date(),
                         self.get_secondary_date(),
                         self.get_transcription(),
                         self.get_total_tokens(),
                         self.get_total_input_tokens(),
                         self.get_total_output_tokens()]
        return metadata_list