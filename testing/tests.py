import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.convert import pdf_to_jpg


class TestConverter(unittest.TestCase):
    def test_convert_happy_path_to_jpg(self):
        # Arrange
        path_pdf = "../resume-en/resume.pdf"
        path_jpg = "../resume-en/resume"

        # Act
        pdf_to_jpg(path_pdf, path_jpg)

        # Assert
        # Check if the JPEG images are saved with numbered file names
        assert os.path.exists(path_jpg + ".jpg")

    def test_convert_nonexistent_pdf(self):
        # Arrange
        path_pdf = "../nonexistent.pdf"
        path_jpg = "../resume-en/resume"

        # Act and Assert
        with self.assertRaises(FileNotFoundError):
            pdf_to_jpg(path_pdf, path_jpg)

    def test_convert_non_pdf_to_jpg(self):
        # Arrange
        path_pdf = "../resume-en/resume.docx"
        path_jpg = "../resume-en/resume"

        # Act and Assert
        with self.assertRaises(ValueError):
            pdf_to_jpg(path_pdf, path_jpg)
    


if __name__ == "__main__":
    unittest.main()
    