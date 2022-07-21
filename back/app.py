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
questions_stars = {}


@app.route('/question/')
def question_stars():
    length = int(request.args.get('length'))
    res = {}
    for i in range(1, length + 1):
        i = str(i)
        res[i] = questions_stars[i]
    return jsonify(res)


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
    questions[question_id].append(data)
    questions_stars[question_id] = max(questions_stars[question_id],
                                       data['stars'])
    with open(f'{thisDir}/data.json', 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False)
    return jsonify({'status': 'ok'})


@app.route('/question/<question_id>/del/', methods=['POST'])
def del_question(question_id):
    ts = str(request.json['ts'])
    for i in range(len(questions[question_id])):
        if questions[question_id][i]['time'] == ts:
            del questions[question_id][i]
            with open(f'{thisDir}/data.json', 'w', encoding='utf-8') as f:
                json.dump(questions, f, ensure_ascii=False)
            questions_stars[question_id] = 0
            for j in questions[question_id]:
                questions_stars[question_id] = max(
                    questions_stars[question_id], j['stars'])
            return jsonify({'status': 'ok'})
    return jsonify({'status': 'not_found'})


if __name__ == '__main__':
    with open(f'{thisDir}/data.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    for i in range(1, 1000):
        questions_stars[str(i)] = 0
    for i, j in questions.items():
        for k in j:
            questions_stars[i] = max(questions_stars[i], k['stars'])
    app.run(debug=False, port=5555)
