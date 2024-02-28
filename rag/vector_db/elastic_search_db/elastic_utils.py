from elastic_connection import ElasticSearchConnection
from typing import Dict, List
from elasticsearch import Elasticsearch
from tqdm import tqdm


class ElasticUtils():
    def __init__(self, elastic_connection: ElasticSearchConnection):
        self.es = elastic_connection.get_instance()
    
    def create_index(self, index_name: str, mappings: Dict):
        self.es.indices.create(index=index_name, mappings=mappings)
    
    def insert_data(self, list_data: List[Dict], index_name: str):
        for data in tqdm(list_data, desc="Inserting data to the index"):
            try:
                self.es.index(index=index_name, document=data, id=data['chunk_id'])
            except Exception as e:
                print(f"Error when inserting {data['chunk_id']}", e)
    
    def search_data(self, query: Dict, index_name: str, source: List[str]):
        res = self.es.knn_search(index=index_name, knn=query, source=source)

        return res['hits']["hits"]

