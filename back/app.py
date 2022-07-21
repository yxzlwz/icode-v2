import json
import os
import time

from flask import Flask, jsonify, request
from flask_cors import CORS

from hunxiao import hunxiao

app = Flask(__name__)
CORS(app)
thisDir = os.path.dirname(os.path.abspath(__file__))

questions = {}


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


@app.route('/question/<question_id>/', methods=['DELETE'])
def del_question(question_id):
    ts = request.json['ts']
    for i in range(len(questions[question_id])):
        if questions[question_id][i]['time'] == ts:
            del questions[question_id][i]
            return jsonify({'status': 'ok'})
    return jsonify({'status': 'not_found'})


if __name__ == '__main__':
    with open(f'{thisDir}/data.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    app.run(debug=True)
