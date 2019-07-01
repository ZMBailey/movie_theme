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
         
        self.keywords1 = [['tape', 'killed', 'cop', 'thugs', 'involved', 'arrest', 'dealer']
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
        self.keywords2 = [['tries', 'runs', 'begins', 'leave', 'starts', 'turns',
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
            
    def run_model(self,text,model_no):
        if model_no == 1:
            model = self.model1
            topics = self.topics1
            keywords = self.keywords1
        else:
            model = self.model2
            topics = self.topics2
            keywords = self.keywords2
            
        probs = model.get_document_topics(corp, minimum_probability=0.0)
        idx, scores = zip(*probs)
        f = scores.index(max(scores))
        s = scores.index(sorted(scores)[-2])
        first = probs[f] + (topics[f]) + (keywords[f])
        scnd = probs[s] + (topics[s]) + (keywords[s])
        return first,scnd
    
    def get_max_tuple(tup1,tup2):
        if tup1[1] > tup2[1]:
            return tup1, tup2
        else:
            return tup2, tup1
        
    def find_topics(self,text):
        topic1_f,topic1_s = run_model(text,1)
        topic2_f,topic2_s = run_model(text,2)
        t1, t2 = get_max_tuple(topic1_f,topic2_f)
        t2, t3 = get_max_tuple(t2, topic1_s)
        t3, t4 = get_max_tuple(t3, topic2_s)
        
        movie_topics = [t1[2],t2[2],t3[2],t4[2]]
        keywords = [t1[3],t2[3],t3[3],t4[3]]
        return movie_topics, keywords