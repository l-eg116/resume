import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import src.convert as cv


class TestConverter(unittest.TestCase):
    def test_convert_happy_path_to_jpg(self):
        # Arrange
        path_pdf = "src/resume-en/resume.pdf"
        path_jpg = "src/resume-en/resume"

        # Act
        cv.pdf_to_jpg(path_pdf, path_jpg)

        # Assert
        # Check if the JPEG images are saved with numbered file names
        assert os.path.exists(path_jpg + ".jpg")

    def test_convert_nonexistent_pdf(self):
        # Arrange
        path_pdf = "nonexistent.pdf"
        path_jpg = "src/resume-en/resume"

        # Act and Assert
        with self.assertRaises(FileNotFoundError):
            cv.pdf_to_jpg(path_pdf, path_jpg)

    def test_convert_non_pdf_to_jpg(self):
        # Arrange
        path_pdf = "src/resume-en/resume.docx"
        path_jpg = "src/resume-en/resume"

        # Act and Assert
        with self.assertRaises(ValueError):
            cv.pdf_to_jpg(path_pdf, path_jpg)

    def test_valid_yaml_file(self):
        # Arrange
        yaml_path = "testing/resources/options-valid.yml"

        # Act
        result = cv.load_options(yaml_path)

        # Assert
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_empty_yaml_file(self):
        # Arrange
        yaml_path = "testing/resources/options-empty.yml"

        # Act and Assert
        with self.assertRaises(ValueError):
            cv.load_options(yaml_path)

    def test_invalid_yaml_file_path(self):
        # Arrange
        yaml_path = "invalid_path.yml"

        # Act and Assert
        with self.assertRaises(FileNotFoundError):
            cv.load_options(yaml_path)

    def test_input_file_not_yaml_error(self):
        # Arrange
        yaml_path = "invalid.txt"

        # Act and Assert
        with self.assertRaises(ValueError):
            cv.load_options(yaml_path)


if __name__ == "__main__":
    unittest.main()
