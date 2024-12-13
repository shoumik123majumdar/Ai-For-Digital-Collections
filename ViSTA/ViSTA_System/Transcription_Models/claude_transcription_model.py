from .transcription_model import TranscriptionModel
from .transcription import Transcription
import anthropic
import os

class ClaudeTranscriptionModel(TranscriptionModel):
    """
    Generates transcriptions from images using Claude API
    """

    def __init__(self, raw_transcription_prompt_file,detail_extraction_prompt_file,token_tracker):
        super().__init__(raw_transcription_prompt_file,detail_extraction_prompt_file,token_tracker)
        api_key = os.environ.get('CLAUDE_KEY')
        self.client = anthropic.Anthropic(api_key=api_key)

    def generate_transcription(self, image_file):
        """
        Generates transcription from image
        """
        # generate raw transcription
        content = [
            {"type": "text", "text": "Image:"},
            {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": image_file}},
            {"type": "text", "text": f"Generate a transcription based on the following transcription guidelines: {self.raw_transcription_prompt}"}
        ]

        # claude API request
        response = self.client.messages.create(
            max_tokens=1500,
            messages=[{"role": "user", "content": content}],
            model='claude-3-5-sonnet-20241022',
        )

        # extract raw transcription text update token usage data
        raw_transcription = response.content
        token_data = response.usage
        self.token_tracker.update_token_traker(token_data)

        # extract details (photographer name and date) from raw transcriptions
        detailed_extraction_prompt = f"{self.detail_extraction_prompt}{raw_transcription}"
        detail_response = self.client.messages.create(
            max_tokens=1500,
            messages=[{"role": "user", "content": [{"type": "text", "text": detailed_extraction_prompt}]}],
            model='claude-3-5-sonnet-20241022',
        )

        # extract detail extraction text and update token tracker
        detailed_extraction = detail_response.content
        token_data = response.usage
        self.token_tracker.update_token_traker(token_data)

        # create transcription object
        transcription = Transcription(raw_transcription, detailed_extraction)
        return transcription






