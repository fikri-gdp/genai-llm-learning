import time
import numpy as np
from typing import List
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from .constants import Constants, PROMPT_TEMPLATE
from langchain_openai import OpenAI

MODEL = SentenceTransformer('all-mpnet-base-v2')


def transform_query_to_vector(text: str) -> List:
    return MODEL.encode(text)


def get_context(query: str) -> dict:
    query_vector = transform_query_to_vector(query)
    query_vector = np.array(query_vector).tolist()
    pc = Pinecone(api_key=Constants.PINECONE_API_KEY)
    index = pc.Index(Constants.INDEX_NAME)

    response = index.query(
        vector=query_vector,
        top_k=4,
        # include_values=True,
        include_metadata=True
    )

    return response.to_dict()


def build_prompt(question: str) -> str:

    query_response = get_context(query=question)
    context_string = "Title: {title}\nSource:{source}\nContent:{content}"
    contexts = [context_string.format(title=elem['metadata']['title'], source=elem['metadata']['source'], content=elem['metadata']['content']) for elem in query_response['matches']]

    return PROMPT_TEMPLATE.format(context="\n\n".join(contexts), question=question)


def query_llm(prompt: str):
    llm = OpenAI(model="gpt-3.5-turbo-instruct")

    for chunk in llm.stream(prompt):
        yield f"data: {chunk}"

    yield "data: [DONE]\n\n"


def generate_response(question: str):
    prompt = build_prompt(question)
    llm = OpenAI(model="gpt-3.5-turbo-instruct")

    for chunk in llm.stream(prompt):
        yield chunk
    yield "data: [DONE]\n\n"
