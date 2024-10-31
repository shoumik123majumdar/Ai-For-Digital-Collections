import unittest
from gemini_transcription_model import GeminiTranscriptionModel
from transcription import Transcription
from gemini_image_processor  import GeminiImageProcessor


class TestGeminiTranscriptionModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test resources once for the entire test suite."""
        file_path = "Test_Images/M214_1015935974_0046_0015_Verso.tif"
        processor = GeminiImageProcessor(file_path)
        img = processor.process_image()
        cls.model = GeminiTranscriptionModel(img)

        # Perform a single API request and save the response
        cls.transcription = cls.model.generate_transcription()
        cls.token_data = cls.model.tokens

    def test_generate_transcription(self):
        """Test that the transcription is generated and is of the correct type."""
        print(self.token_data)
        print(self.transcription)
        self.assertIsInstance(self.transcription, Transcription, "The response should be a Transcription object")

    def test_total_tokens(self):
        """Test that the total tokens are returned correctly."""
        total_tokens = self.model.get_total_tokens()
        self.assertEqual(total_tokens, self.token_data["total_tokens"], "Total tokens do not match expected value")

    def test_total_input_tokens(self):
        """Test that the input tokens are returned correctly."""
        input_tokens = self.model.get_total_input_tokens()
        self.assertEqual(input_tokens, self.token_data["prompt_tokens"], "Input tokens do not match expected value")

    def test_completion_tokens(self):
        """Test that the completion tokens are returned correctly."""
        completion_tokens = self.model.get_completion_tokens()
        self.assertEqual(completion_tokens, self.token_data["completion_tokens"],
                         "Completion tokens do not match expected value")


if __name__ == "__main__":
    unittest.main()
