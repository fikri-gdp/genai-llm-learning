from gdplabs_gen_ai.document_processing_orchestrator.loader.pipeline_loader import PipelineLoader
from gdplabs_gen_ai.document_processing_orchestrator.loader.pdf_loader import PDFMinerLoader, PDFPlumberLoader
from gdplabs_gen_ai.document_processing_orchestrator.parser.document_parser import PDFParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json
from typing import Dict, Tuple
from constants import StructureConstants, ChunkParameter, Constants
from utils import get_append_logic_separator
from transformers import AutoTokenizer
from unidecode import unidecode
import os
from hashlib import md5
from tqdm import tqdm


tokenizer = AutoTokenizer.from_pretrained(Constants.TOKENIZER_REPOSITORY)
unique_keys = {}

def load_documents(source: str):
    pipeline = PipelineLoader()
    pipeline.add_loader(PDFMinerLoader())
    pipeline.add_loader(PDFPlumberLoader())

    loaded_elements = pipeline.load(source)
    
    return loaded_elements


def parse_document(loaded_elements: list) -> list:
    parser = PDFParser()
    return parser.parse(loaded_elements)


def get_title(parse_result: list) -> str:
    """Retrieve the title from a document content dictionary.

    This function extracts the title from a dictionary containing document contents.
    It iterates through the content list, searching for the structure identified as the title
    (using `StructureConstants.TITLE`). Once found, it returns the text associated with the title structure.

    Args:
        res (Dict): A dictionary containing document contents.

    Returns:
        str: The extracted title text, if found; otherwise, an empty string.

    Example:
        Given a dictionary `res` representing document contents:
        title_text = get_title(res)
    """

    for content in parse_result:
        if content["structure"] == StructureConstants.TITLE:
            return content["text"]

    return ""


def post_process_parse_result(parse_result: list):
    content_list = parse_result

    result = ""
    tables = []

    for idx, content in enumerate(content_list):
        if content["text"]:
            if content["structure"] == StructureConstants.TABLE:
                prev_content = content_list[idx - 1]
                prev_prev_content = content_list[idx - 2] if idx - 2 >= 0 else {"text": ""}
                tables.append(f"{prev_prev_content['text']}{prev_content['text']}\n{content['text']}")
            elif content["structure"] == StructureConstants.FOOTER:
                continue
            else:
                separator = (
                    get_append_logic_separator(prev_content=content_list[idx - 1], current_content=content)
                    if idx > 0
                    else "\n"
                )
                result += f'{separator}{content["text"]}'

    return result, tables


def count_token(string: str) -> int:
    encoded_string = tokenizer.encode(string)
    return len(encoded_string)


def chunk_text(text: str, max_token: int = ChunkParameter.MAX_TOKEN, overlap_ratio=ChunkParameter.OVERLAP_RATIO):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=max_token,
        chunk_overlap=max_token*overlap_ratio
    )

    return splitter.split_text(text)


def remove_unicode(string: str) -> str:
    return unidecode(string)


def get_source(parse_result: list) -> str:
    for idx, elem in enumerate(parse_result):
        if elem['metadata']['source']:
            return elem['metadata']['source']
        
    return ""


def save_dict_as_json(dictionary, file_name):
    """Save a dictionary as a JSON file.

    This function writes a dictionary into a JSON file with the specified file name.
    It opens the file in write mode and uses the `json.dump()` method to serialize the dictionary and
    save it as JSON.

    Args:
        dictionary (Dict): The dictionary to be saved as JSON.
        file_name (str): The name of the JSON file to be created or overwritten.

    Example:
        To save a dictionary `my_dict` into a file named "data.json":
        save_dict_as_json(my_dict, "data.json")
    """
    with open(file_name, "w+", encoding="UTF-8") as json_file:
        json.dump(dictionary, json_file)

def generate_chunk_id(key: str) -> Tuple[Dict[str, int], str]:
    """Generate a unique chunk ID using the MD5 hashing algorithm.

    This function generates a unique chunk ID by hashing the provided key using the MD5 hashing algorithm.
    If multiple chunks have the same key, it auto-increments the ID to ensure uniqueness.

    Args:
        unique_keys (Dict[str, int]): A dictionary of unique keys and their counts.
        key (str): The key used for generating the chunk's ID.

    Returns:
        Tuple[Dict[str, int], str]: A tuple containing the updated unique keys dictionary and the generated
        chunk ID.

    Note:
        Example ID (<MD5 Hashed Key>-<Index>):
        - e52a1bc6de13ae3f1e36f2fbcf126752-1
        - e52a1bc6de13ae3f1e36f2fbcf126752-2

    """
    hashed_key = md5(key.encode()).hexdigest()
    if hashed_key not in unique_keys:
        unique_keys[hashed_key] = 1
    else:
        unique_keys[hashed_key] += 1

    result_id = f"{hashed_key}-{unique_keys[hashed_key]}"
    return result_id


def process_documents():
    DOCUMENT_LIST = os.listdir(Constants.DOCUMENT_PATH)
    for document in tqdm(DOCUMENT_LIST):
        loaded_elements = load_documents(f"{Constants.DOCUMENT_PATH}/{document}")
        parsed_elements = parse_document(loaded_elements)

        title = get_title(parsed_elements)
        # source = get_source(parsed_elements)
        text_result, table_result = post_process_parse_result(parsed_elements)
        chunked_text = chunk_text(text_result)

        merged_result = chunked_text + table_result

        for idx, text in enumerate(merged_result):
            result_dict = {
                "title": title,
                "content": remove_unicode(text),
                "source": document,
                "chunk_id": generate_chunk_id(document)
            }
            destination_path = f"{Constants.CHUNK_RESULT_FILE_PATH}/{document.replace('.pdf', '')}-{idx}.json"
            save_dict_as_json(result_dict, destination_path)



def main():
    process_documents()


if __name__ == "__main__":
    main()