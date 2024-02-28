from pinecone import Pinecone
from constants import Constants
from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np
import json

MODEL = SentenceTransformer('all-mpnet-base-v2')


def transform_to_vector(text: str) -> List:
    return MODEL.encode(text)


def main():
    pc = Pinecone(api_key=Constants.PINECONE_API_KEY)

    index = pc.Index(Constants.INDEX_NAME)

    query = "Neymar is a super dribbler"
    query_vector = np.array(transform_to_vector(query))
    query_vector = query_vector.tolist()

    response = index.query(
        vector=query_vector,
        top_k=10,
        # include_values=True,
        include_metadata=True
    )

    print(json.dumps((response.to_dict())))


if __name__ == "__main__":
    main()