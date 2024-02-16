import os


class Constants:
    TOKENIZER_REPOSITORY = os.path.abspath(os.path.join(os.path.dirname(__file__), "./tokenizer"))
    DOCUMENT_PATH = "../../data/raw/pdf"
    CHUNK_RESULT_FILE_PATH = "../chunk_data"


class ChunkParameter:
    """Represents the chunk parameter of the content."""
    MAX_TOKEN = 1800
    OVERLAP_RATIO = 0.2
    SEPARATORS = ["\n\n", "\n", " ", ""]


class StructureConstants:
    """Represents the structure of the content."""

    HEADER = "header"
    TITLE = "title"
    HEADING = ("heading 1", "heading 2", "heading 3", "heading 4", "heading 5", "heading 6")
    PARAGRAPH = "paragraph"
    TABLE = "table"
    FOOTNOTE = "footnote"
    FOOTER = "footer"
    UNCATEGORIZED_TEXT = "UncategorizedText"