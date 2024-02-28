import gradio as gr
from backend.llm import generate_response
from backend.constants import Constants
import os

os.environ["OPENAI_API_KEY"] = Constants.OPENAI_API_KEY

def stream_response(message):
    response_generator = generate_response(message)
    response = ""
    for chunk in response_generator:
        if "data: [DONE]" not in chunk:
            response += chunk
            yield response

gr.ChatInterface(stream_response).launch()
