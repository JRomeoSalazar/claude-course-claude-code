from io import BytesIO
from pathlib import Path

from markitdown import MarkItDown, StreamInfo
from pydantic import Field

SUPPORTED_EXTENSIONS = ("pdf", "docx")


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_markdown(
    path: str = Field(
        description="Path to a PDF (.pdf) or Word (.docx) file on the machine "
        "running this server. Absolute paths are recommended; '~' is expanded."
    ),
) -> str:
    """Convert a PDF or DOCX file on disk to markdown.

    Reads the file at the given path and returns its full contents as
    markdown-formatted text, preserving structure such as headings, lists
    and tables where the source document exposes it. The file type is
    determined from the file extension (case-insensitive).

    When to use:
    - When you need to read or analyse the contents of a local PDF or DOCX file
    - When you have a file path rather than the document contents

    When not to use:
    - For other formats (e.g. .txt, .md, .xlsx); only .pdf and .docx are supported
    - For remote documents; the path must be on the server's filesystem

    Raises:
    - ValueError if the file extension is not .pdf or .docx
    - FileNotFoundError if the path does not exist or is not a file

    Examples:
    >>> document_path_markdown("/home/user/reports/q3.pdf")
    "# Q3 Report\n\nRevenue grew ..."
    >>> document_path_markdown("~/notes/meeting.docx")
    "## Agenda\n\n- Budget\n- Hiring"
    """
    file_path = Path(path).expanduser()
    extension = file_path.suffix.lower().lstrip(".")
    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type '{file_path.suffix}'. "
            f"Supported types: {', '.join(SUPPORTED_EXTENSIONS)}"
        )
    if not file_path.is_file():
        raise FileNotFoundError(f"No file found at {file_path}")
    return binary_document_to_markdown(file_path.read_bytes(), extension)
