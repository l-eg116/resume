import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import src.convert as cv  # noqa: E402


class TestConverter(unittest.TestCase):
    """Test the functions in the convert.py module."""

    def test_convert_happy_path_to_jpg(self: unittest) -> None:
        """Test the pdf_to_jpg function with a valid PDF file."""
        # Arrange
        path_pdf = "src/resume-en/resume.pdf"
        path_jpg = "src/resume-en/resume"

        # Act
        cv.pdf_to_jpg(path_pdf, path_jpg)

        # Assert
        # Check if the JPEG images are saved with numbered file names
        assert Path(path_jpg + ".jpg").exists()

    def test_convert_nonexistent_pdf(self: unittest) -> None:
        """Test the pdf_to_jpg function with a nonexistent PDF file."""
        # Arrange
        path_pdf = "nonexistent.pdf"
        path_jpg = "src/resume-en/resume"

        # Act and Assert
        with self.assertRaises(FileNotFoundError):
            cv.pdf_to_jpg(path_pdf, path_jpg)

    def test_convert_non_pdf_to_jpg(self: unittest) -> None:
        """Test the pdf_to_jpg function with a non-PDF file."""
        # Arrange
        path_pdf = "src/resume-en/resume.docx"
        path_jpg = "src/resume-en/resume"

        # Act and Assert
        with self.assertRaises(ValueError):
            cv.pdf_to_jpg(path_pdf, path_jpg)

    def test_valid_yaml_file(self: unittest) -> None:
        """Test the load_options function with a valid YAML file."""
        # Arrange
        yaml_path = "testing/resources/options-valid.yml"

        # Act
        result = cv.load_options(yaml_path)

        # Assert
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_empty_yaml_file(self: unittest) -> None:
        """Test the load_options function with an empty YAML file."""
        # Arrange
        yaml_path = "testing/resources/options-empty.yml"

        # Act and Assert
        with self.assertRaises(ValueError):
            cv.load_options(yaml_path)

    def test_invalid_yaml_file_path(self: unittest) -> None:
        """Test the load_options function with a nonexistent YAML file."""
        # Arrange
        yaml_path = "invalid_path.yml"

        # Act and Assert
        with self.assertRaises(FileNotFoundError):
            cv.load_options(yaml_path)

    def test_input_file_not_yaml_error(self: unittest) -> None:
        """Test the load_options function with a non-YAML file."""
        # Arrange
        yaml_path = "invalid.txt"

        # Act and Assert
        with self.assertRaises(ValueError):
            cv.load_options(yaml_path)


if __name__ == "__main__":
    unittest.main()
