import flask
from flask import request, jsonify
from intent_classifier import Intent_classifier

app = flask.Flask(__name__)
app.config["DEBUG"] = True

intent_classifier = Intent_classifier()

@app.route('/', methods=['GET'])
def home():
    return "<h1>Intent Detection using NLP</h1><p>This site is a prototype API for training and classifying intents.</p>"



@app.route('/api/v1/intent_detection/train', methods=['PUT'])
def train_model():
    query_parameters = request.args
    
    intent0 = query_parameters['intent0']
    sentence0 = query_parameters['sentence0']

    intent1 = query_parameters['intent1']
    sentence1 = query_parameters['sentence1']

    intent2 = query_parameters['intent2']
    sentence2 = query_parameters['sentence2']

    intents = [intent0, intent1, intent2]
    sentences = [sentence0, sentence1, sentence2]
    intent_classifier.train(intents, sentences)
    
    params = [
        {'intent0': intent0,
         'sentence0': sentence0},
        {'intent1': intent1,
         'sentence1': sentence1},
        {'intent2': intent2,
         'sentence2': sentence2},

    ]
    
    return jsonify({'response':'model ready'})

@app.route('/api/v1/intent_detection/classify', methods=['PUT'])
def classify():
    query_parameters = request.args
    sentence = query_parameters['sentence']
    detected_intent = intent_classifier.classify(sentence)
    
    return jsonify({'intent':detected_intent})
    
app.run(host='0.0.0.0')
