from flask import Flask, abort, render_template

app = Flask(__name__)

@app.route("/")
def index():
    abort(404)

@app.route("/prescriber/dashboard")
def prescriberDash():
    return render_template("prescriber.html")

if __name__ == "__main__":
    pass