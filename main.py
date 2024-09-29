from flask import Flask, abort

app = Flask(__name__)

@app.route("/")
def index():
    abort(404)

if __name__ == "__main__":
    pass