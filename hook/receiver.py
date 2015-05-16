from flask import Flask, request, jsonify
import json
from .parser import get_rules
from .model import DottedDict

app = Flask(__name__)
rules = get_rules()


@app.route("/")
def home():
    return "Hello world"


@app.route("/hook/<name>", methods=["POST"])
def trigger_hook(name):
    headers = request.headers
    payload = request.data

    decoder = json.JSONDecoder(object_hook=DottedDict)
    dd = decoder.decode(payload)

    try:
        method = headers["X-Github-Event"]
    except KeyError:
        return "Method not in payload", 404

    try:
        hook = rules[name]
        status = hook.execute_hook(method)
    except KeyError:
        return "Hook not found", 404
    try:
        return jsonify(message=status.format(**dd)), 200
    except AttributeError as e:
        return e.message, 500


if __name__ == "__main__":
    app.run(debug=True)
