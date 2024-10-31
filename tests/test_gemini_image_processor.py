import unittest
from gemini_image_processor  import GeminiImageProcessor
from PIL import Image

class TestGeminiImageProcessor(unittest.TestCase):

    def setUp(self):
        """Set up test resources (runs before each test case)"""
        self.file_path = "Test_Images/M214_1015935974_0046_0015_Verso.tif"
        self.processor = GeminiImageProcessor(self.file_path)

    def test_grayscale(self):
        """Test that the image is converted to grayscale"""
        self.processor._grayscale()

        with Image.open(self.file_path) as img:
            self.assertEqual(img.mode, "L", "Image is not in grayscale mode after processing.")

    def test_resize_small_JPEG(self):
        """Test if the resize function does not resize images smaller than 3072x3072"""
        file_path = "Test_Images/Test_Small_JPEG.jpg"
        processor = GeminiImageProcessor(file_path)
        #Actual Size of the image: 500 × 408 pixels

        processor._resize()

        with Image.open(file_path) as img:
            width, height = img.size
            self.assertEqual(width,500,"width was not accurate")
            self.assertEqual(height,408,"height was not accurate")

    def test_resize_large_TIF(self):
        """Test if the resize function does resize TIF images larger than 3072x3072"""
        #Actual Size of the image:

        self.processor._resize()

        with Image.open(self.file_path) as img:
            width, height = img.size
            self.assertEqual(width,3072,"width was not accurate")
            self.assertEqual(height,3072,"height was not accurate")

    def test_is_JPEG(self):
        "Test if a TIF image properly converted into a JPEG after it was processed"
        with Image.open(self.file_path) as img:
            self.assertEqual(img.format,"TIFF","Image does not start as a TIFF")

        self.processor.process_image()

        with Image.open(self.file_path) as img:
            self.assertEqual(img.format,"JPEG","Image is not a JPEG")

    def test_process_image(self):
        """Test to make sure the image was properly saved"""
        img_file = self.processor.process_image()
        self.assertEqual(img_file.display_name,"M214_1015935974_0046_0015_Verso.tif","file_name does not match up")


if __name__ == '__main__':
    unittest.main()