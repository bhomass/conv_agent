from allennlp.predictors.predictor import Predictor as AllenNLPPredictor
import os
import torch
from allennlp.models.archival import load_archive

from os import listdir
from os.path import isfile, join

from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.converter import TextConverter
from io import StringIO
import io

class PDF_agent:
    def __init__(self):
        self.predictor = AllenNLPPredictor.from_path(
            "https://storage.googleapis.com/allennlp-public-models/bidaf-elmo-model-2020.03.19.tar.gz", \
                cuda_device=torch.cuda.current_device()
        ) 
        
#         print('file location={}'.format((os.path.dirname(os.path.abspath(__file__)))))
        file_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'data')
        print('file_dir={}'.format(file_dir))
        
        self.onlyfiles = [f for f in listdir(file_dir) if isfile(join(file_dir, f))]
        
    def list_files(self):
        return self.onlyfiles
    
    def read_nth_file(self, index):
        file = self.onlyfiles[index]
        self.read_file(file)
        
    def read_file(self, file):
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'data', file)
#         print('cwd={}'.format(filepath))
        
        content = convert_pdf_to_txt(filepath)
#         with open(filepath, 'r') as credit_doc:
#             content = credit_doc.read()
            
        lines = content.split('\n')
        print('total lines = {}'.format(len(lines)))
        
        line_array = ['\n\n']
        max_lines = 500
        i = 0
        for line in lines:
            if len(line) > 0:
                line_array.append(line)
                i += 1
                if i > max_lines:
                    break
                    
        self.corpus = '\n'.join(line_array)
#         self.corpus = content
                

    def answer(self, question):
        prediction = self.predictor.predict(
            passage = self.corpus, question= question
        )
#         [start, end] = prediction['best_span']
#         print('start end = {},{}'.format(start, end))
#         line = find_beginning_end(start, end, self.corpus)
        
        return prediction["best_span_str"]  #, line
    
    def get_corpus(self):
        return self.corpus
    
    
def convert_pdf_to_txt(path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(path, 'rb') as fh:

        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()

#     print(text)
    return text

def find_new_line_backward(start, end, text):
    if end == 0:
        end = start + 1
    start -= 1     # start backing up the document
    partial_str = text[start: end]
    print('partial_str={}'.format(partial_str))
    start_index = -1
    try:
        start_index = re.search("\n\n", partial_str).start()
    except:
        pass
#     print('start_index= {}'.format(start_index))
    while start_index != 0:
        start -= 1
        partial_str = text[start: end]
        print('partial_str={}'.format(partial_str))
        try:
            start_index = re.search("\n\n", partial_str).start()
        except:
            pass
#         print('start_index= {}'.format(start_index))
    
#     print('final start_index= {}'.format(start))
    return start

def find_new_line_forward(start, end, text):
    end += 1     # start backing up the document
    partial_str = text[start: end]
#     print('partial_str={}'.format(partial_str))
    end_index = -1
    try:
        end_index = re.search("\n\n", partial_str).start()
    except:
        pass
#     print('start_index= {}'.format(start_index))
    while end_index == -1:
        end += 1
        partial_str = text[start: end]
#         print('partial_str={}'.format(partial_str))
        try:
            end_index = re.search("\n\n", partial_str).start()
        except:
            pass
#         print('end_index= {}'.format(end_index))
    
#     print('final end_index= {}'.format(start))
    return end

def find_beginning_end(start, end, text):
    line_start = find_new_line_backward(start, end, text)
    line_end = find_new_line_forward(start, end, text)
    line = text[line_start + 2: line_end - 2]
#     print('before sub line={}'.format(line))
    line = re.sub('[*]+', '', line)
    line = line.strip()
#     print('after sub line={}'.format(line))
    return line

