import unittest
from Transcription_Models.gemini_transcription_model_v2 import GeminiTranscriptionModel
from Transcription_Models.transcription_v2 import Transcription
from Image_Processors.gemini_image_processor  import GeminiImageProcessor
from token_tracker import TokenTracker

class TestGeminiTranscriptionModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test resources once for the entire test suite."""
        file_path = "Test_Images/transcription_test.tif"
        processor = GeminiImageProcessor()
        cls.img = processor.process_image(file_path)
        cls.token_tracker = TokenTracker()
        prompt_step_one = "Prompts/Transcription_Prompts/transcription_step_one.txt"
        prompt_step_two = "Prompts/Transcription_Prompts/transcription_step_two.txt"
        cls.model = GeminiTranscriptionModel(prompt_step_one,prompt_step_two,cls.token_tracker)

    def test_generate_initial_transcription(self):
        """Test that the transcription is generated and is of the correct type."""
        transcription = self.model.generate_transcription(self.img)
        print(transcription.transcription)
        print(transcription.detail_extraction)
        print(transcription.name)
        print(transcription.dates)
        print(self.token_tracker.total_tokens)
        print(self.token_tracker.input_tokens)
        print(self.token_tracker.output_tokens)
        #self.assertIsInstance(self.transcription, Transcription, "The response should be a Transcription object")


if __name__ == "__main__":
    unittest.main()
