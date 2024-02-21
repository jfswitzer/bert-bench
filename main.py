import time
import socketio
import json
from tflite_support.task import text
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, send, emit
import csv
import sys
import numpy as np 
class BertQA():
    def __init__(self):
        self.answerer = text.BertQuestionAnswerer.create_from_file('mobilebert.tflite')
        self.answerer._options.num_threads=2
        self.answerer._options.accelerator_name="google-edgetpu"
    def get_answer(self,question,text):
        bert_qa_result = self.answerer.answer(text,question)
        return bert_qa_result


classifier = BertQA()
with open('qa.json') as json_file:
    data = json.load(json_file)
    TITLES = data['titles']
    CONTENTS = data['contents']


def job_submit(title,question):
    if title in TITLES:
        text=CONTENTS[TITLES.index(title)]
    start_time = time.time_ns()
    result = classifier.get_answer(question,text[0])
    end_time = time.time_ns()
    text = result.answers[0].text
    logit = result.answers[0].pos.logit
    start = result.answers[0].pos.start
    end = result.answers[0].pos.end
    latency=end_time-start_time
    return latency


if __name__ == "__main__":
    import json
    with open('qa.json') as json_file:
        data = json.load(json_file)
        titles=data['titles']
        questions=data['questions']
    latencies=[]
    #for i in range(10):
    for title in titles:
        for question in questions[titles.index(title)]:
            latency=job_submit(title,question)
            latencies.append(latency)
    with open(f'{sys.argv[1]}.csv', 'w', newline='') as csvfile:
        writer=csv.writer(csvfile)
        writer.writerow(["latency"])
        for l in latencies:
            writer.writerow([l])

