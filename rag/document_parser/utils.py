from typing import Dict
from constants import StructureConstants


def get_append_logic_separator(prev_content: Dict, current_content: Dict) -> str:
    """Determine the logic for appending separators between content structures.

    This function decides the separator to be appended between different content structures based on their types.
    It evaluates the previous and current content structures and returns an appropriate separator.

    Args:
        prev_content (Dict): Dictionary containing information about the previous content structure.
        current_content (Dict): Dictionary containing information about the current content structure.

    Returns:
        str: The separator determined based on the comparison of content structures.

    Example:
        Given dictionaries representing the previous and current content structures:
        separator = get_append_logic_separator(previous_content, current_content)
    """
    if (
        prev_content["structure"] == StructureConstants.PARAGRAPH
        and current_content["structure"] == StructureConstants.PARAGRAPH
    ):
        return "\n"
    elif (
        prev_content["structure"] in StructureConstants.HEADING
        and current_content["structure"] == StructureConstants.PARAGRAPH
    ):
        return "\n"
    elif (
        prev_content["structure"] == StructureConstants.PARAGRAPH
        and current_content["structure"] in StructureConstants.HEADING
    ):
        return "\n\n"
    elif (
        prev_content["structure"] in StructureConstants.HEADING
        and current_content["structure"] in StructureConstants.HEADING
    ):
        if prev_content["structure"] == current_content["structure"]:
            return " "
        else:
            return "\n"
    elif (
        prev_content["structure"] == StructureConstants.TITLE
        and current_content["structure"] == StructureConstants.PARAGRAPH
    ):
        return "\n"

    return "\n\n"