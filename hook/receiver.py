from flask import Flask, request
from .parser import get_rules

app = Flask(__name__)
rules = get_rules()


@app.route("/")
def home():
    return "Hello world"


@app.route("/hook/<name>", methods=["POST"])
def trigger_hook(name):
    headers = request.headers

    try:
        method = headers["X-Github-Event"]
    except KeyError:
        return "Method not in payload", 404

    try:
        hook = rules[name]
        return hook.execute_hook(method), 200
    except KeyError:
        return "Hook not found", 404


if __name__ == "__main__":
    app.run(debug=True)
