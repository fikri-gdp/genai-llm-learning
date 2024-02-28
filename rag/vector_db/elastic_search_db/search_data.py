from insert_data import transform_to_vector


def query_builder(field: str, keyword: str, k: int, num_candidates: int):
    return {
        "field": field,
        "query_vector": transform_to_vector(keyword),
        "k": k,
        "num_candidates": num_candidates,
    }
