index_map = {
    "properties": {
        "title": {
            "type": "text"
        },
        "source": {
            "type": "text"
        },
        "content": {
            "type": "text"
        },
        "content_vector": {
            "type": "dense_vector",
            "dims": 768,
            "index": True,
            "similarity": "l2_norm"
        }

    }
}
