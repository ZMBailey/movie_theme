from text_processing import (tag_words,remove_stopwords,
                             remove_sw,process_doc,
                            bigrams,refactor_corpus,get_corpus)
from gensim.models import LdaMulticore
import pickle


class Themeter():
    
    def __init__(self):
        
        with open('model1.pkl', 'rb') as f:
            self.model1 = pickel.load(f)
        with open('model2.pkl', 'rb') as e:
            self.model2 = pickel.load(e)
            
        self.topics1 = ['Crime Drama','On the Run','Thriller involving Planes','Murder Mystery','Relationship Drama',
               'Heist','Jail','Highschool','Romance','Action',
               'Tough Decisions','Hospitals']
        self.topics2 = ['On the Run','Drama','Performance','Medieval','Action','Romance','Psychological','Mystery']
            
            
    def run_model(self,text,model_no):
        if model_no == 1:
            model = self.model1
            topics = self.topics1
        else:
            model = self.model2
            topics=self.topics2
            
        topic = model.get_document_topics(corp, minimum_probability=0.0)
        idx, scores = zip(*topic)
        return topics1scores.index(max(scores))]
        
    def find_topics(self,text):
        topic1 = run_model(text,1)
        topic2 = run_model(text,2)
        return topic1, topic2
