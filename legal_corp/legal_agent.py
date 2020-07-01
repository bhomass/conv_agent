from allennlp.predictors.predictor import Predictor as AllenNLPPredictor
import os

class Legal_agent:
    def __init__(self):
        self.predictor = AllenNLPPredictor.from_path(
            "https://storage.googleapis.com/allennlp-public-models/bidaf-elmo-model-2020.03.19.tar.gz"
        )
        print('cwd={}'.format(os.getcwd()))
        with open('legal_corp/data/1000453_1997-11-14_CREDIT AGREEMENT.txt', 'r') as credit_doc:
            content = credit_doc.read()
            
        lines = content.split('\n')
        
        line_array = []
        max_lines = 200
        i = 0
        for line in lines:
            if len(line) > 0:
                line_array.append(line)
                i += 1
                if i > max_lines:
                    break
                    
        self.corpus = '\n'.join(line_array)
                

    def predict(self, question):
        prediction = self.predictor.predict(
            passage = self.corpus, question= question
        )
        return prediction["best_span_str"]  