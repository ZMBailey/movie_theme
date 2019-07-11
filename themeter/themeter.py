from themeter.dev.text_processing import (tag_words,remove_stopwords,
                             remove_sw,process_doc,
                            bigrams,refactor_corpus,get_corpus)
from gensim.models import LdaMulticore
from themeter.dev.wikiparse_movies import WikiParser
import wikipedia
import pickle


class Themeter():
    
    def __init__(self):
        
        with open('themeter/dev/jar/model1_1.pkl', 'rb') as f1:
            model1 = pickle.load(f1)
        with open('themeter/dev/jar/model2_1.pkl', 'rb') as f2:
            model2 = pickle.load(f2)
        with open('themeter/dev/jar/id2word.pkl', 'rb') as f3:
            self.id2 = pickle.load(f3) 
        with open('themeter/dev/jar/stopwords.pkl', 'rb') as f4:
            self.stopwords = pickle.load(f4) 
#         topics1 = ['Creation','Drama','Action','Art','Beginning','Tension',
#                 'Espionage','Romance','Mystery','Crime','Thriller','Adventure']
#         topics2 = ['Action','Small Town','Sports','Performance','On the Run','Competition',
#                 'Relationship Drama','Suspense','Mystery','Thriller']
         
#         keywords1 = [['different', 'final', 'shown', 
#                       'focuses', 'include', 'script', 'explores', 'writer'],
#                     ['maid', 'narrator', 'questioning', 'draws', 'effort',
#                      'earned', 'affection', 'portrayed', 'townsfolk'],
#                     ['plane', 'bomb', 'flight', 'pilot', 'scientist', 
#                      'infected', 'passengers', 'helicopter'],
#                     ['played', 'romantic', 'includes', 'screened', 
#                      'inspired', 'period', 'inmates', 'painting'],
#                     ['tries', 'runs', 'begins', 'starts',
#                      'makes', 'getting', 'playing'],
#                     ['leave', 'reveals', 'killed', 'named', 
#                          'begins', 'discovers', 'attempts', 'apartment', 'runs'],
#                     ['aliens', 'thugs', 'minister', 'defeats', 
#                      'humans', 'residents', 'execution', 'plans'],
#                     ['decides', 'meets', 'relationship', 'become', 'married',
#                      'leave', 'agrees', 'apartment'],
#                     ['killed', 'ship', 'attempt', 'plan',
#                      'captured', 'discover', 'led', 'manages'],
#                     ['trial', 'evidence', 'confession', 'heroin', 'spell', 
#                      'lawyer', 'guilty', 'accused', 'sentence', 'arrest'],
#                     ['murdered', 'victims', 'died', 'thriller', 'victim',
#                      'discovers', 'couple', 'evidence'],
#                     ['roles', 'creatures',  'airplane', 'theory', 
#                      'cases', 'existence', 'transforms', 'loyalty']]    
#         keywords2 = [['ship', 'plane', 'flight', 'pilot', 'bomb', 
#                       'scientist', 'passengers', 'ships', 'aliens', 'destroyed'],
#                     ['tape', 'deals', 'presented', 'fog', 'prominent', 
#                      'firm', 'residents','fishing'],
#                     ['concerns', 'played', 'precode', 'narrator',
#                      'edited', 'teams', 'player', 'airplane'],
#                     ['shown', 'romantic', 'received',
#                      'played', 'bands', 'screened', 'musician'],
#                     ['tries', 'runs', 'begins', 'leave', 
#                      'starts', 'turns', 'attempts'],
#                     ['wins', 'turns', 'decides', 'attempt', 'final', 'become', 'loses'],
#                     ['meets', 'decides', 'relationship', 'apartment',
#                      'leave', 'agrees', 'become', 'married'],
#                     ['killed', 'reveals', 'discovers', 
#                      'attempts', 'plan', 'taken', 'manages'],
#                     ['named', 'begins', 'died', 'murdered', 
#                      'victims', 'curse', 'discovers', 'victim'],
#                     ['thriller', 'writer', 'played', 'final', 'leading','described', 'different']]
        topics1 = ['Action','Crime','Performance','On the Run','Drama','Espionage','Suspense','Romance']
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
        '''Queries the wikipedia api for a movie title, and then 
            returns the plot of the movie.
            
            Args:
                title: string
                    movie title to be searched.
                
            Return:
                string
                    the text of the plot summary from wikipedia.
                string
                    the title of the movie.'''
        
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
        '''takes a list of probabilities and finds either the highest or second highest
            probability, and looks up the corresponding topic and set of keywords. 
            
            Args:
                model: dictionary
                    a dictionary containing topics and keywords.
                probs: list of tuples
                    list of tuples containing the scores for each topic.
                
            Return:
                tuple
                    tuple with the score and the corresponding topic and set of keywords'''
        
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
        '''processes the input text and runs it through a model to get the topic scores.
            
            Args:
                text: string
                    the input text to be processed.
                model_no:
                    the number of model to run on the text.
                
            Return:
                first: tuple
                    tuple with the score and the corresponding topic and set of keywords
                    for the highest ranking topic.
                scnd: tuple
                    same as first, but for the second highest ranking topic.'''
        
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
        '''finds the numerical order of two tuples based on the score contained
        at index 1.
            
            Args:
                tup1: tuple
                    the first tuple.
                tup2:
                    the second tuple.
                
            Return:
                tuple
                    tuple with higher score.
                tuple
                    tuple with lower score.'''
        if tup1[1] > tup2[1]:
            return tup1, tup2
        else:
            return tup2, tup1
        
        
    def find_topics(self,name):
        '''takes a title, searches wikipedia for the plot summary, and then runs the plot 
            summary through both models, and returns the resulting topics. 
            
            Args:
                text: string
                    the title of a movie.
                
            Return:
                movie_topics: list
                    a list of the movie topics
                keywords: list
                    a list of lists of keywords, corresponding the topics.
                w_title: string
                    the title of the movie as it appears on wikipedia.'''
        
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