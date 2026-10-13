import os
import pytest
from tools.document import binary_document_to_markdown, document_path_markdown


class TestBinaryDocumentToMarkdown:
    # Define fixture paths
    FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
    DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")
    PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")

    def test_fixture_files_exist(self):
        """Verify test fixtures exist."""
        assert os.path.exists(self.DOCX_FIXTURE), (
            f"DOCX fixture not found at {self.DOCX_FIXTURE}"
        )
        assert os.path.exists(self.PDF_FIXTURE), (
            f"PDF fixture not found at {self.PDF_FIXTURE}"
        )

    def test_binary_document_to_markdown_with_docx(self):
        """Test converting a DOCX document to markdown."""
        # Read binary content from the fixture
        with open(self.DOCX_FIXTURE, "rb") as f:
            docx_data = f.read()

        # Call function
        result = binary_document_to_markdown(docx_data, "docx")

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result

    def test_binary_document_to_markdown_with_pdf(self):
        """Test converting a PDF document to markdown."""
        # Read binary content from the fixture
        with open(self.PDF_FIXTURE, "rb") as f:
            pdf_data = f.read()

        # Call function
        result = binary_document_to_markdown(pdf_data, "pdf")

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result


class TestDocumentPathMarkdown:
    PDF_FIXTURE = TestBinaryDocumentToMarkdown.PDF_FIXTURE
    DOCX_FIXTURE = TestBinaryDocumentToMarkdown.DOCX_FIXTURE

    def test_document_path_markdown_with_pdf(self):
        """Test converting a PDF file path to markdown."""
        result = document_path_markdown(self.PDF_FIXTURE)

        assert isinstance(result, str)
        assert len(result) > 0

    def test_document_path_markdown_with_docx(self):
        """Test converting a DOCX file path to markdown."""
        result = document_path_markdown(self.DOCX_FIXTURE)

        assert isinstance(result, str)
        assert len(result) > 0

    def test_document_path_markdown_matches_binary_conversion(self):
        """The path tool must return the same markdown as converting the bytes."""
        with open(self.PDF_FIXTURE, "rb") as f:
            expected = binary_document_to_markdown(f.read(), "pdf")

        assert document_path_markdown(self.PDF_FIXTURE) == expected

    def test_document_path_markdown_rejects_unsupported_extension(self, tmp_path):
        """Test that a non PDF/DOCX file is rejected."""
        text_file = tmp_path / "notes.txt"
        text_file.write_text("hello")

        with pytest.raises(ValueError, match="Unsupported file type"):
            document_path_markdown(str(text_file))

    def test_document_path_markdown_with_missing_file(self, tmp_path):
        """Test that a nonexistent path raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            document_path_markdown(str(tmp_path / "missing.pdf"))
