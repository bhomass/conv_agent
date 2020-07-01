from allennlp.predictors.predictor import Predictor as AllenNLPPredictor


class Legal_agent:
    def __init__(self):
        self.predictor = AllenNLPPredictor.from_path(
            "https://storage.googleapis.com/allennlp-public-models/bidaf-elmo-model-2020.03.19.tar.gz"
        )
        with open('legal_corp/data/1000453_1997-11-14_CREDIT AGREEMENT.txt', 'r') as credit_doc:
            self.corpus = credit_doc.read()

    def predict(self, question):
        prediction = self.predictor.predict(
            passage = self.corpus, question= question
        )
        return prediction["best_span_str"]  