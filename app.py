from flask import Flask, render_template, request, jsonify
import os
import json

app = Flask(__name__)

DB_FILE = "answer.json"

def get_answer():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            data = json.load(f)
            return data.get("answer")
    return None

def save_answer(answer):
    with open(DB_FILE, "w") as f:
        json.dump({"answer": answer}, f)

@app.route("/")
def home():
    return render_template("index.html", saved_answer=get_answer())

@app.route("/submit", methods=["POST"])
def submit():
    if get_answer():
        return jsonify({"status": "locked"})
    data = request.get_json()
    answer = data.get("answer")
    save_answer(answer)
    return jsonify({"status": "saved", "answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)