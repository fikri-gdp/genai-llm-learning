from pinecone import Pinecone, PodSpec
import os
from constants import Constants
import time


def main():
    pc = Pinecone(api_key=Constants.PINECONE_API_KEY)
    spec = PodSpec(
        environment="us-central-1",
        pod_type='p1.x1'
    )

    existing_indexes = [
        index_info["name"] for index_info in pc.list_indexes()
    ]

    if Constants.INDEX_NAME not in existing_indexes:
        pc.create_index(
            Constants.INDEX_NAME,
            dimension=768,
            metric="cosine",
            spec=spec
        )

    while not pc.describe_index(Constants.INDEX_NAME).status["ready"]:
        time.sleep(1)
    
    index = pc.Index(Constants.INDEX_NAME)
    time.sleep(1)
    print(index.describe_index_stats())


if __name__ == "__main__":
    main()
