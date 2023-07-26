from flask import Flask
# from flask_cors import CORS

app = Flask(__name__)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/members")
def members():
    return {"members": ["1", "2", "3"]}


if __name__ == "__main__":
    app.run(debug=True)
