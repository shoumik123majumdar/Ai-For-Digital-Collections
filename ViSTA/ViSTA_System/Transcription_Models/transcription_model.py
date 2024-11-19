from abc import ABC, abstractmethod


class TranscriptionModel(ABC):
    """
    Interface for classes that handle transcribing text from the back of the image
    """
    def __init__(self,raw_transcription_prompt_file,detail_extraction_prompt_file,token_tracker):
        self.token_tracker = token_tracker
        with open(raw_transcription_prompt_file, "r") as file:
            self.raw_transcription_prompt = file.read()
        with open(detail_extraction_prompt_file, "r") as file:
            self.detail_extraction_prompt = file.read()
        #self.model <- model should be instantiated in constructor


    @abstractmethod
    def generate_transcription(self,image_file):
        """
        Generates transcription from image at self.file_path
        Also extracts details from transcription like photographer names and dates
        Inputs:
            - image_file: image object you want to generate transcription for
        Outputs:
            - self.transcription is initialized as a Transcription object
            - self.token_tracker is updated to reflect new total, input, and output token counts
        """
        pass