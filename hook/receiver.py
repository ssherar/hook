from flask import Flask
from .parser import get_rules
import logging

app = Flask(__name__)
rules = get_rules()

@app.route("/")
def home():
    return "Hello world"

@app.route("/hook/<name>/<method>")
def trigger_hook(name, method):
    ret = None
    try:
        hook = rules[name]
        ret = hook.execute_hook(method)
    except KeyError:
        return "Hook not found", 404

    return ret, 200

if __name__ == "__main__":
    app.run(debug=True)
