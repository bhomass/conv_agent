from allennlp.predictors.predictor import Predictor as AllenNLPPredictor
import os
import torch
from allennlp.models.archival import load_archive

class Legal_agent:
    def __init__(self):
        self.predictor = AllenNLPPredictor.from_path(
            "https://storage.googleapis.com/allennlp-public-models/bidaf-elmo-model-2020.03.19.tar.gz", \
                cuda_device=torch.cuda.current_device()
        ) 
        
#         print('file location={}'.format((os.path.dirname(os.path.abspath(__file__)))))
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'data', '1000453_1997-11-14_CREDIT AGREEMENT.txt')
#         print('cwd={}'.format(filepath))
        with open(filepath, 'r') as credit_doc:
            content = credit_doc.read()
            
        lines = content.split('\n')
        
        line_array = []
        max_lines = 1000
        i = 0
        for line in lines:
            if len(line) > 0:
                line_array.append(line)
                i += 1
#                 if i > max_lines:
#                     break
                    
        self.corpus = '\n'.join(line_array)
                

    def predict(self, question):
        prediction = self.predictor.predict(
            passage = self.corpus, question= question
        )
        return prediction["best_span_str"]  
    
    def get_corpus(self):
        return self.corpus