from themeter.dev.text_processing import (tag_words,remove_stopwords,
                             remove_sw,process_doc,
                            bigrams,refactor_corpus,get_corpus)
from gensim.models import LdaMulticore
from themeter.dev.wikiparse_movies import WikiParser
import wikipedia
import pickle


class Themeter():
    
    def __init__(self):
        
        with open('themeter/dev/jar/model1.pkl', 'rb') as f1:
            model1 = pickle.load(f1)
        with open('themeter/dev/jar/model2.pkl', 'rb') as f2:
            model2 = pickle.load(f2)
        with open('themeter/dev/jar/id2word.pkl', 'rb') as f3:
            self.id2 = pickle.load(f3) 
        with open('themeter/dev/jar/stopwords.pkl', 'rb') as f4:
            self.stopwords = pickle.load(f4) 
        topics1 = ['Action','Crime','Performance','On the Run','Relationship_Drama','Espionage','Suspense','Romance']
        topics2 = ['Fighting','Romance','Drama','On the Run','Psychological',
               'Heist','Thriller','Crime','Courtroom','Tough Decisions',
               'Mystery','Action']
         
        keywords1 = [['ship', 'plane', 'pilot', 'flight', 
                      'bomb', 'passengers', 'ships', 'engine'],
                    ['trial', 'evidence', 'murdered', 'committed', 'patient',
                         'guilty', 'patients', 'innocent', 'victim'],
                    ['played', 'shown', 'includes', 'final', 'received',
                         'focuses', 'called', 'romantic'],
                    ['tries', 'begins', 'leave', 'runs', 
                         'turns', 'starts', 'attempts'],
                    ['debut', 'painting', 'wrote', 'unexpected',
                         'published', 'millionaire', 'reputation'],
                    ['decides', 'agrees', 'gives', 'leave', 
                         'offers', 'reveals', 'plans', ],
                    ['killed', 'named', 'attempt', 'reveals', 
                         'discover', 'attacked', 'attempts', 'captured'],
                    ['relationship', 'begins', 'meets', 'married', 
                         'career', 'couple', 'pregnant', 'boyfriend']]    
        keywords2 = [['final', 'powerful', 
                     'terrorists', 'teams', 'involves', 'championship', 'theaters'],
                    ['relationship', 'meets', 'leave', 'begins', 'apartment', 
                         'married', 'reveals', 'decides', 'discovers', 'visits'],
                    ['shown', 'played', 'includes', 'debut', 'concerns', 
                         'received', 'romantic'],
                    ['tries', 'starts', 'runs', 'decides', 
                         'gives', 'doesnt', 'leave', 'turns'],
                    ['experiences', 'patient', 'patients', 
                         'psychiatrist', 'visions', 'tape'],
                    ['pay', 'hired', 'scheme', 'offers', 
                         'gambling', 'player', 'plans'],
                    ['killed', 'reveals', 'plane', 'flight',
                         'pilot', 'evidence'],
                    ['killed', 'named', 'plan', 'arrest', 'criminals', 
                         'thugs', 'captured', 'plans'],
                    ['trial', 'evidence', 'murdered', 'lawyer', 'accused', 
                         'guilty', 'cop', 'victim'],
                    ['become', 'decides', 'must', 
                         'agrees', 'contract', 'named', 'wish', 'plans'],
                    ['killed', 'attempts', 'tries', 'leave', 'begins', 
                         'discovers', 'named', 'runs', 'turns', 'manages'],
                    ['ship', 'bomb', 'helicopter', 'captured', 'others', 
                         'attacked', 'scientist', 'ships']]
        
        self.model1 = {'model':model1, 'topics':topics1, 'keywords':keywords1}
        self.model2 = {'model':model2, 'topics':topics2, 'keywords':keywords2}
            
    def get_from_wikipedia(self,title):
        wp = WikiParser()
        try:
            movie = wikipedia.page(title)
            return wp.get_plot(movie),movie.title
        except wikipedia.exceptions.DisambiguationError:
            return -2,-2
        except wikipedia.exceptions.PageError:
            return -2,-2
        except AttributeError:
            return -2,-2
        
    
    def get_topic(self,model,probs,p):
        idx, scores = zip(*probs)
        if p == 1:
            i = scores.index(max(scores))
        else:
            i = scores.index(sorted(scores)[-2])
                             
        if scores[i] < 0.15:
            topic = ("",)
            keywords = ([""],)
        else:
            topic = (model['topics'][i],)
            keywords = (model['keywords'][i],) 
        return probs[i] + topic + keywords 
            
        
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
        
        
    def find_topics(self,name):
        title = name.title()
        text,w_title = self.get_from_wikipedia(title)
        if text == -2:
            text,w_title = self.get_from_wikipedia(title + " (film)")
            if text == -2:
                return text,text,text
        if text == -1:
            return text,text,text
        
        topic1_f,topic1_s = self.run_model(text,1)
        topic2_f,topic2_s = self.run_model(text,2)
        t1, t2 = self.get_max_tuple(topic1_f,topic2_f)
        t2, t3 = self.get_max_tuple(t2, topic1_s)
        t3, t4 = self.get_max_tuple(t3, topic2_s)
        
        movie_topics = [t1[2],t2[2],t3[2],t4[2]]
        keywords = [t1[3],t2[3],t3[3],t4[3]]
        return movie_topics, keywords, w_title