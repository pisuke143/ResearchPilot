import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from researchpilot.pipeline import process_pdf


class TestPipeline(unittest.TestCase):

    def test_process_pdf_keeps_page_numbers(self):
        with TemporaryDirectory() as temp_dir:
            pdf_path = Path(temp_dir) / "sample.pdf"

            with pymupdf.open() as document:
                page = document.new_page()
                page.insert_text(
                    (72, 72),
                    "Research papers contain useful evidence."
                )

                page = document.new_page()
                page.insert_text(
                    (72, 72),
                    "Experiments help test scientific ideas."
                )

                document.save(pdf_path)

            chunks = process_pdf(str(pdf_path), chunk_size=500)

            self.assertEqual(len(chunks), 2)
            self.assertEqual(chunks[0]["page_number"], 1)
            self.assertEqual(chunks[1]["page_number"], 2)
            self.assertIn("Research papers", chunks[0]["text"])
            self.assertIn("Experiments", chunks[1]["text"])

    def test_missing_pdf_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            process_pdf("file_that_does_not_exist.pdf")


if __name__ == "__main__":
    unittest.main()
