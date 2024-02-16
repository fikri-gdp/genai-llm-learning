from elastic_utils import ElasticUtils
from elastic_connection import ElasticSearchConnection
import os
from typing import List
from sentence_transformers import SentenceTransformer
import json
from index_map import index_map
from tqdm import tqdm

INDEX_NAME = "learn_rag"
CHUNK_PATH = "../chunk_data"
MODEL = SentenceTransformer('all-mpnet-base-v2')


def transform_to_vector(text: str) -> List:
    return MODEL.encode(text)


def main():
    files = os.listdir(CHUNK_PATH)

    chunks = []
    print("Processing chunk")
    for file in tqdm(files):
        print(f"Processing file {file}")
        json_file = open(f"{CHUNK_PATH}/{file}")
        dict_data = json.load(json_file)
        json_file.close()

        dict_data['content_vector'] = transform_to_vector(dict_data['content'])

        chunks.append(dict_data)
    
    connection = ElasticSearchConnection()
    es = ElasticUtils(connection)
    
    print("Creating index")
    es.create_index(INDEX_NAME, index_map)
    print("Success create index")

    es.insert_data(chunks, INDEX_NAME)
    print("Success insert data")


if __name__ == "__main__":
    main()