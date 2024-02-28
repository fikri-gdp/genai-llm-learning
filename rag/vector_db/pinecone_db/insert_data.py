from pinecone import Pinecone
import os
from typing import List
from sentence_transformers import SentenceTransformer
import json
from tqdm import tqdm
import time
from constants import Constants

CHUNK_PATH = "../../chunk_data"
MODEL = SentenceTransformer('all-mpnet-base-v2')


def transform_to_vector(text: str) -> List:
    return MODEL.encode(text)


def main():
    files = os.listdir(CHUNK_PATH)
    pc = Pinecone(api_key=Constants.PINECONE_API_KEY)
    index = pc.Index(Constants.INDEX_NAME)

    chunks = []
    print("Processing chunk")
    for file in tqdm(files):
        json_file = open(f"{CHUNK_PATH}/{file}")
        dict_data = json.load(json_file)
        json_file.close()

        # dict_data['content_vector'] = transform_to_vector(dict_data['content'])
        new_dict = {
            "id": dict_data["chunk_id"],
            "metadata": {
                "title": dict_data["title"],
                "source": dict_data["source"],
                "content": dict_data["content"],
            },
            "values": transform_to_vector(dict_data["content"])
        }

        chunks.append(new_dict)

    for i in range(0, len(chunks), 30):
        chunk_to_insert = chunks[i:i+30]
        print("Inserting", i)
        index.upsert(chunk_to_insert)
        time.sleep(1)
        print("Finished inserting")


if __name__ == "__main__":
    main()