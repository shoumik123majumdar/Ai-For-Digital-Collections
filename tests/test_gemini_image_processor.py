import unittest
from gemini_image_processor  import GeminiImageProcessor


class TestGeminiImageProcessor(unittest.TestCase):

    def setUp(self):
        """Set up test resources (runs before each test case)"""
        self.file_path = "Test_Images/Test.jpeg"
        self.processor = GeminiImageProcessor(self.file_path)

    def test_process_image(self):
        """Test the image processing functionality."""
        processed_image = self.processor.process_image()


    def test_process_image_fails(self):
        """Test that image processing functionality fails"""


if __name__ == '__main__':
    unittest.main()