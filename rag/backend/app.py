import flask
import flask_cors
import time
from langchain_openai import OpenAI
from llm import generate_response
from flask import request
from constants import Constants
import os

os.environ["OPENAI_API_KEY"] = Constants.OPENAI_API_KEY
app = flask.Flask(__name__)
flask_cors.CORS(app)


@app.get("/stream-response")
def stream():
    query = request.args.get('query')
    return flask.Response(generate_response(query), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(port=8800)
