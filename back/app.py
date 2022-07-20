import json
import os
import time

from flask import Flask, jsonify, redirect, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
thisDir = os.path.dirname(os.path.abspath(__file__))

questions = {}


def hunxiao(code):
    # TODO
    return code


@app.route('/question/<question_id>/')
def question(question_id):
    data = questions.get(question_id, [])
    for i in range(len(data)):
        data[i]['code_hx'] = hunxiao(data[i]['code'])
    return jsonify(data)


@app.route('/question/<question_id>/', methods=['POST'])
def add_answer(question_id):
    if question_id not in questions:
        questions[question_id] = []
    data = request.json
    data['time'] = time.time()
    questions[question_id].append(data)
    with open(f'{thisDir}/data.json', 'w', encoding='utf-8') as f:
        json.dump(questions, f)
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    with open(f'{thisDir}/data.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    app.run(debug=True)
