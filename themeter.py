from text_processing import (tag_words,remove_stopwords,
                             remove_sw,process_doc,
                            bigrams,refactor_corpus,get_corpus)
from gensim.models import LdaMulticore
import pickle


class Themeter():
    
    def __init__(self):
        
        with open('jar/model1.pkl', 'rb') as f1:
            model1 = pickle.load(f1)
        with open('jar/model2.pkl', 'rb') as f2:
            model2 = pickle.load(f2)
        with open('jar/id2word.pkl', 'rb') as f3:
            self.id2 = pickle.load(f3) 
        with open('jar/stopwords.pkl', 'rb') as f4:
            self.stopwords = pickle.load(f4) 
        topics1 = ['Crime Drama','On the Run','Thriller involving Planes','Murder Mystery','Relationship Drama',
               'Heist','Jail','Highschool','Romance','Action',
               'Tough Decisions','Hospitals']
        topics2 = ['On the Run','Drama','Performance','Medieval','Action','Romance','Psychological','Mystery']
         
        keywords1 = [['tape', 'killed', 'cop', 'thugs', 'involved', 'arrest', 'dealer'],
                        ['tries', 'begins', 'runs', 'leave', 'attempts', 'turns', 'starts', 'causing'],
                        ['plane', 'flight', 'pilot', 'passengers', 'infected', 'aired', 'bombing', 'engine', 'airplane', 'climbing'],
                        ['killed', 'reveals', 'discovers', 'murdered', 'died', 'claims', 'apartment', 'evidence', 'begins', 'investigate'],
                        ['played', 'includes', 'concerns', 'received', 'romantic', 'shown'],
                        ['plan', 'plans', 'scheme', 'fake', 'pay', 'minister', 'thief', 'hired', 'turns'],
                        ['trial', 'sent', 'prisoners', 'execution', 'sentenced', 'taken', 'lawyer', 'guilty', 'sentence'],
                        ['contract', 'script', 'paying', 'prom', 'championship', 'teams', 'composer', 'involves', 'debate', 'current'],
                        ['relationship', 'become', 'begins', 'decides', 'would', 'married', 'career'],
                        ['killed', 'ship', 'reveals', 'captured', 'attempt', 'bomb', 'plan'],
                        ['leave', 'meets', 'decides', 'gives', 'agrees', 'tries', 'apartment', 'offers', 'reveals'],
                        ['debut', 'shown', 'patients', 'called', 'narrator', 'appeared', 'available', 'patient']]    
        keywords2 = [['tries', 'runs', 'begins', 'leave', 'starts', 'turns',
                           'makes', 'attempts', 'gives', 'seen'],
                        ['romantic', 'concerns', 'whose', 'sexual', 'played', 
                         'relationship', 'experiences', 'struggles', 'leading', 'childhood'],
                        ['shown', 'played', 'debut', 'includes', 'received',
                         'final', 'september', 'december', 'created'],
                        ['painting', 'must', 'wish', 'villagers', 'minister', 'servant', 
                         'attraction', 'scheme', 'coat', 'spell'],
                        ['ship', 'plane', 'pilot', 'flight', 'passengers', 'aliens', 
                         'ships', 'launch', 'engine', 'surface'],
                        ['meets', 'decides', 'relationship', 'would', 'become', 'agrees',
                         'married', 'leave', 'begins', 'gives'],
                        ['trial', 'patient', 'committed', 'evidence', 'patients', 'roles',
                         'psychiatrist', 'precode', 'executed', 'innocent'],
                        ['killed', 'reveals', 'named', 'discovers', 'attempts',
                         'attempt', 'discover', 'attacked', 'manages', 'plan']]
        
        self.model1 = {'model':model1, 'topics':topics1, 'keywords':keywords1}
        self.model2 = {'model':model2, 'topics':topics2, 'keywords':keywords2}
            
            
    def get_topic(self,model,probs,p):
        idx, scores = zip(*probs)
        if p == 1:
            s = max(scores)
        else:
            s = sorted(scores)[-2]
        i = scores.index(s)
        return probs[i] + (model['topics'][i],) + (model['keywords'][i],) 
            
        
    def run_model(self,text,model_no):
        if model_no == 1:
            model = self.model1
        else:
            model = self.model2
            
        text_vec = process_doc(text,self.id2,self.stopwords)    
        probs = model['model'].get_document_topics(text_vec, minimum_probability=0.0)
        first = self.get_topic(model,probs,1)
        scnd = self.get_topic(model,probs,2)
        return first,scnd
    
    
    def get_max_tuple(self,tup1,tup2):
        if tup1[1] > tup2[1]:
            return tup1, tup2
        else:
            return tup2, tup1
        
        
    def find_topics(self,text):
        topic1_f,topic1_s = self.run_model(text,1)
        topic2_f,topic2_s = self.run_model(text,2)
        t1, t2 = self.get_max_tuple(topic1_f,topic2_f)
        t2, t3 = self.get_max_tuple(t2, topic1_s)
        t3, t4 = self.get_max_tuple(t3, topic2_s)
        
        movie_topics = [t1[2],t2[2],t3[2],t4[2]]
        keywords = [t1[3],t2[3],t3[3],t4[3]]
        return movie_topics, keywords