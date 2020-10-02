import sys
sys.path.insert(0,'..')

import pandas as pd

import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import row
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput, TextAreaInput, HTMLTemplateFormatter
from bokeh.plotting import figure

from bokeh.io import show, output_notebook#, output_file


from datetime import date
from random import randint

from bokeh.io import show
from bokeh.models import ColumnDataSource, DataTable, DateFormatter, TableColumn
from bokeh.models import Button, Column

from bokeh.models.widgets import Div
from bokeh.layouts import column

from pdf_files.pdf_agent import PDF_agent

print('instantiating agent')
covid_agent = PDF_agent()
print('agent initiated')

file = 'EBC External 06.10.20 FAQs.pdf'
covid_agent.read_file(file)
corpus = covid_agent.get_corpus()

# print(corpus)

corpus_text = TextAreaInput(title="Source Corpus", value=corpus, rows=20, cols=20, max_length=10000)

question_field = TextInput(title='Enter question here')
button = Button(label="Ask", button_type="success")
inputs = Column(corpus_text, question_field, button, width=550)



lines = [{'Question': 'question text', 'Answer': 'answer text'}]
summary_df = pd.DataFrame(lines)

Columns = [TableColumn(field=Ci, title=Ci, width=296, formatter=HTMLTemplateFormatter(template='<div style="width: 340px;word-break: break-all;white-space: normal;"><%= value %></div>')) for Ci in summary_df.columns] # bokeh columns
# columns = [
#     TableColumn(field='atomic number', title='Atomic Number'),
#     TableColumn(field='symbol', title='Symbol'),
#     TableColumn(field='name', title='Name', 
#                 formatter=HTMLTemplateFormatter(template='<font color="<%= CPK %>"><%= value %></font>'))
# ]
columnDataSource = ColumnDataSource(summary_df)
data_table = DataTable(columns=Columns, source=columnDataSource, row_height=100, width=640) # bokeh table

# show(data_table)
div = Div(text="""The Answer to your question is given below.""",
width=800, height=20)

# show(data_table)

column = column(div, data_table)
def update_table():
    global summary_df
    print('button clicked')
    question = question_field.value
#     div.text = source
    print('calling answer_question')
    answer = answer_question(question)
    print('update columnDataSource')
    print('before df shape={}'.format(summary_df.shape))
    summary_df = summary_df.append({'Question': question, 'Answer': answer}, ignore_index=True)
    print('after df shape={}'.format(summary_df.shape))

    columnDataSource.data = summary_df
    

button.on_click(update_table)

# show(row(inputs, column, width=800))
curdoc().add_root(row(inputs, column, width=800))
curdoc().title = "QA-Agent"

# In[ ]:

def answer_question(question):
    print('calling agent to answer')
    answer = covid_agent.answer(question)
    print('got answer: {}'.format(answer))
    return answer