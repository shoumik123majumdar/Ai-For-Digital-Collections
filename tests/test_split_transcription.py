import unittest
from gemini_transcription_model_v2 import GeminiTranscriptionModel
from transcription import Transcription
from gemini_image_processor  import GeminiImageProcessor
from token_tracker import TokenTracker

class TestGeminiTranscriptionModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test resources once for the entire test suite."""
        file_path = "Test_Images/portrait_back_clone.tif"
        processor = GeminiImageProcessor()
        cls.img = processor.process_image(file_path)
        self.token_tracker = TokenTracker()
        cls.model = GeminiTranscriptionModel("Prompts/Transcription_Prompts/transcription_step_one.txt",self.token_tracker)

    def test_generate_initial_transcription(self):
        """Test that the transcription is generated and is of the correct type."""
        transcription = self.model.generate_transcription(self.img)

        print(transcription
        #self.assertIsInstance(self.transcription, Transcription, "The response should be a Transcription object")


if __name__ == "__main__":
    unittest.main()
