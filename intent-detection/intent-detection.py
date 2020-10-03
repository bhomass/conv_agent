import sys
sys.path.insert(0,'..')

import pandas as pd

import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import row
from bokeh.models import CustomJS, ColumnDataSource
from bokeh.models.widgets import Slider, TextInput, TextAreaInput, HTMLTemplateFormatter
from bokeh.plotting import figure

from bokeh.io import show, output_notebook#, output_file


from datetime import date
from random import randint

from bokeh.io import show, output_notebook
from bokeh.models import ColumnDataSource, DataTable, DateFormatter, TableColumn
from bokeh.models import Button, Column

from bokeh.models.widgets import Div
from bokeh.layouts import column

from intent_classifier import Intent_classifier

intent_classifier = Intent_classifier()

intent_0 = TextInput(title="Intent 0", name='intent_0', value='delayed')
sentence_0 = TextAreaInput(value="Is my bill delayed", title="Prototype Sentence:", rows=5, cols=1000, max_length=1400)
row_0 = row(intent_0, sentence_0, width=800)

intent_1 = TextInput(title="Intent 1", name='intent_1', value='send')
sentence_1 = TextAreaInput(value="Can you email me my statement", title="Prototype Sentence:", rows=5, cols=1000, max_length=1400)
row_1 = row(intent_1, sentence_1, width=800)

intent_2 = TextInput(title="Intent 2", name='intent_2', value='status')
sentence_2 = TextAreaInput(value="what is the billing status of john doe", title="Prototype Sentence:", rows=5, cols=1000, max_length=1400)
row_2 = row(intent_2, sentence_2, width=800)

def train_intents():
#     out_div.text = 'training begins'
    intents = [intent_0.value, intent_1.value, intent_2.value]
    sentences = [sentence_0.value, sentence_1.value, sentence_2.value]
    intent_classifier.train(intents, sentences)
#     out_div.text = 'training done'
    button1.disabled = False
    
button0 = Button(label="Train Intent", button_type="success", width=400)
button0.on_click(train_intents)

new_sentence_text = TextAreaInput(title="New Sentence", rows=3, cols=1000, value='')

div = Div(text="""The sentence you just entered has ______ intent.""",
width=800, height=20)

def display_intent():
    new_sentence = new_sentence_text.value
#     out_div.text = 'classify {}'.format(new_sentence)
    detected_intent = intent_classifier.classify(new_sentence)
    div.text = 'The sentence you just entered has "{}" intent.'.format(detected_intent)
#     out_div.text = 'classification done'
        
button1 = Button(label="Classify Sentence", button_type="success", width=400, disabled=True)
button1.on_click(display_intent)

out_div = Div(text="", width=800, height=20)
# out_div.text = 'not yet clicked'

vertical_column = column(row_0, row_1, row_2, button0, new_sentence_text, div, button1, out_div)

curdoc().add_root(vertical_column)
curdoc().title = "Intent Detection"
