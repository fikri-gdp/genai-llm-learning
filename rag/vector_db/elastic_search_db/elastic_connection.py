from elasticsearch import Elasticsearch
from constants import Constants
from typing import Tuple

class ElasticSearchConnection:
    def __init__(self, es_address: str = Constants.ES_ADDRESS, basic_auth: Tuple[str, str] = Constants.ES_AUTH, ca_certs: str = Constants.ES_CA_CERTS) -> Elasticsearch:
        self.es = Elasticsearch(
            es_address,
            basic_auth=basic_auth,
            ca_certs=ca_certs
        )

    def get_instance(self) -> Elasticsearch:
        return self.es
