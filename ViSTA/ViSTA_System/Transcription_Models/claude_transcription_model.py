from transcription_model import TranscriptionModel
from transcription import Transcription
import anthropic
import os

class ClaudeTranscriptionModel(TranscriptionModel):
    """
    Generates transcriptions from images using Claude API
    """

    def __init__(self, image_file):
        super().__init__(image_file)
        api_key = os.environ.get('API_KEY')
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def generate_transcription(self):
        """
        Generates transcription from image
        """
        # prepare prompt for Claude API
        content = [
            {"type": "text", "text": "Image:"},
            {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": self.image_file}},
            {"type": "text", "text": f"Generate a transcription based on the following transcription guidelines: {self.prompt}"}
        ]

        # claude API request
        response = self.client.messages.create(
            model='claude-3-5-sonnet-20241022',
            messages=[{"role": "user", "content": content}]
        )

        # extract transcription text and token usage data
        transcription_text = response.content
        self.token_data = response.usage

        # create and return transcription object
        transcription = Transcription(transcription_text)
        return transcription

    def get_total_tokens(self):
        """
        Gets total number of tokens used from the latest transcription request
        :return:
        """
        if self.token_data is None:
            return "No transcription requests have been made"
        else:
            return self.token_data['total_tokens']

    def get_total_input_tokens(self):
        """
        Gets total number of input tokens used from the latest transcription request
        :return:
        """
        if self.token_data is None:
            return "No transcription requests have been made"
        else:
            return self.token_data['prompt_tokens']

    def get_total_output_tokens(self):
        """
        Gets total number of input tokens used from the latest transcription request
        :return:
        """
        if self.token_data is None:
            return "No transcription requests have been made"
        else:
            return self.token_data['completion_tokens']




