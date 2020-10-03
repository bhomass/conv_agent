
from sentence_transformers import SentenceTransformer

from sklearn.metrics.pairwise import cosine_similarity

class Intent_classifier:
    
    def __init__(self):
        self.model = SentenceTransformer('bert-base-nli-mean-tokens')
        
    def train(self, intents, sentences):
        self.intent0 = intents[0]
        self.intent1 = intents[1]
        self.intent2 = intents[2]
#         sentences = ["Is my bill delayed", "Can you email me my statement", 'what is the billing status of john doe']
        sentence_embeddings = self.model.encode(sentences)
        self.intent0_embedding = list(sentence_embeddings[0])
        self.intent1_embedding = list(sentence_embeddings[1])
        self.intent2_embedding = list(sentence_embeddings[2])
    

    def classify(self, input):
        input_embedding = self.model.encode([input])[0]
        intent0_score = cosine_similarity([list(input_embedding)], [self.intent0_embedding])
        intent1_score = cosine_similarity([list(input_embedding)], [self.intent1_embedding])
        intent2_score = cosine_similarity([list(input_embedding)], [self.intent2_embedding])

        score_list = [intent0_score, intent1_score, intent2_score]
        max_index = score_list.index(max(score_list))

        return [self.intent0, self.intent1, self.intent2][max_index]

