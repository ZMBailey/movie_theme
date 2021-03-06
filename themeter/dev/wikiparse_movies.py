import string
import wikipedia
import requests
import pandas as pd


class WikiParser():
    
    def __init__(self):
        self.S = requests.Session()
        self.pageerrors = []
        self.ambiguation = []
        self.attribute = []
        self.filter = self.setup_filter()
    
    def get_plot(self,raw_text):
        '''accepts a WikipediaPage object, and extracts the plot text(if there is any)
            and returns it in plain text, with no punctuation. If no plot text exists, return -1.
            
            Args:
                raw_text: WikipediaPage
                    the artiticle in a WikipediaPage format.
                
            Return:
                plottext: string
                    The plot section of the article in plain text format.'''
        fulltext = raw_text.content
        ind1 = fulltext.find('== Plot ==') + 10
        ind2 = fulltext.find('==',ind1)
        plottext = fulltext[ind1:ind2]
        plottext = plottext.replace('\n',' ').translate(str.maketrans('','',string.punctuation))
        if len(plottext) > 5:
            return plottext
        else:
            return -1


    def get_category(self,cat):
        '''searches for a wikipedia category, and returns the first 100 members
        of the category.
            
            Args:
                cat: string
                The category to be searched. 
                
            Return:
                titles: list
                    the titles of the 100 category members in the search.'''
        
        URL = "https://en.wikipedia.org/w/api.php"

        TITLE = cat

        PARAMS = {
            'action': "query",
            'list': 'categorymembers',
            'cmtitle': TITLE,
            'cmlimit': '100',
            'format': "json",
        }

        R = self.S.get(url=URL, params=PARAMS)
        data = R.json()
        ids =  [item['pageid'] for ind,item in enumerate(data['query']['categorymembers']) if ind>1]
        if 'continue' in data.keys():
            self.cmc = data['continue']['cmcontinue']
        else:
            self.cmc = -1
        return ids


    def continue_category(self,cat):
        '''searches for a wikipedia category previously searched, and returns the 
        next 100 memebers of the category. Requires that the category have been
        previously searched. 
            
            Args:
                cat: string
                    The category to be searched. 
                
            Return:
                titles: list
                    the titles of the next 100 category members in the search.'''
        
        
        URL = "https://en.wikipedia.org/w/api.php"

        PARAMS = {
            'action': "query",
            'list': 'categorymembers',
            'cmtitle': cat,
            'cmcontinue': self.cmc,
            'cmlimit': '100',
            'format': "json",
        }

        R = self.S.get(url=URL, params=PARAMS)
        data = R.json()
        ids =  [item['pageid'] for ind,item in enumerate(data['query']['categorymembers']) if ind>1]
        if 'continue' in data.keys():
            self.cmc = data['continue']['cmcontinue']
        else:
            self.cmc = -1
        return ids
    
    
    def setup_filter(self):
        p_titles = []
        old_titles = []
        
        for year in range(1960,2011,10):
            cat = "Category:" + str(year) + "s pornographic films"
            titles = self.get_category(cat)

            for _ in range(32):
                p_titles += titles
                if self.cmc != -1:
                    titles = self.continue_category(cat)
                if titles == old_titles:
                    break
                old_titles = titles
        return titles
    

    def get_all_plots(self,pages):
        '''accepts a list of wikipedia page titles, and searchs for each one.
            The plot is then extracted from the page in a plaintext format, 
            and attached to a list.
            
            Args:
                pages: list
                    list of page titles to be searched. 
                
            Return:
                plots: list
                    list of dictionaries, each containing a plot summary for a movie and the title'''
        
        
        plots = []

        for i,page in enumerate(pages):
            try:
                if page in self.filter:
                    continue
                movie = wikipedia.page(pageid=page)
                if movie.title.startswith('List'):
                    continue
                plot = self.get_plot(movie)
                if plot != -1:
                    plots.append({'title': movie.title, 'summary': plot})
            except wikipedia.exceptions.DisambiguationError:
                self.ambiguation.append(page)
            except wikipedia.exceptions.PageError:
                self.pageerrors.append(page)
            except AttributeError:
                self.attribute.append(page)
            if ((i+1) % 10 == 0):
                print('.',end=" ")

        print(" ")
        return plots
    
    def get_plots_from_year(self,year,end=602,start=0,skip=False):
        '''accepts a year and returns all plot summaries from that year.
            
            Args:
                year: int
                    the year to be searched.
                start: int (optional) 
                    page of category to start search at.
                skip: boolean (optional)
                    If set to true, search will attempt to start from a later page.
                
            Return:
                movies: list
                    list of dictionaries, each containing a plot summary for a movie and the title'''
        
        cat = "Category:" + str(year) + " films"
        titles = self.get_category(cat)
        
        if skip:
            for _ in range(start+1):
                titles = self.continue_category(cat)

        movies = []
        old_movies = []

        for _ in range(start,end):
            print('page: ' + str(_) + ' parsing...', end=" ")
            new_movies = self.get_all_plots(titles)
            if new_movies == old_movies:
                break
            movies += new_movies
            if self.cmc != -1:
                titles = self.continue_category(cat)
            old_movies = new_movies
            
        return movies
    
    def get_years(self,start,end):
        '''accepts a start year and end year and returns all plot summaries from that year range.
            
            Args:
                start: int
                    starting year.
                end:
                    ending year.
                
            Return:
                movies: list
                    list of dictionaries, each containing a plot summary for a movie and the title'''
        
        movies = []
        for year in range(start,end):
            print("Getting plots from " + str(year) + ":")
            movies += self.get_plots_from_year(year)
        
        return movies
        