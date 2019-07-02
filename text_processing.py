from gensim.utils import simple_preprocess
from gensim.models import Phrases
from gensim.models.phrases import Phraser
import gensim


def get_tag(idx,doc,st):
    '''modified function to print a number every time 1000 items
    have been processed.
    
    Args:
        idx: int
            index of item being processed.
        doc: string
            the document to process.
        st: StandfordNERTagger
            the tagger object being used to run NER of the doc.
                
    Return:
        output from NER.
        '''
    if idx % 1000:
        print(idx)
        return st.tag(doc.split())

    
def tag_words(texts, st):
    '''Takes a list of documents and runs NER on each one. Then it creates
    a list of all the words that have been classified as names.
    
    Args:
        texts: list of strings
            List of the documents to be processed
        st: StandfordNERTagger
            the tagger object being used to run NER of the doc.
                
    Return:
        List of names contained in the documents.
        '''
    tags = [get_tag(idx,doc,st) for idx,doc in enumerate(texts)]
    names = [set([word for word,tag in doc if tag != 'O']) for doc in tags]
    return set.union(*names)


def remove_sw(doc,stop_words):
    '''Takes a document and removes the stopwords from each one.
    
    Args:
        doc: string
            document to be processed
        stop_words: list
            List of stopwords to be removed
                
    Return:
        Document with all the stopwords removed.
        '''
    return [word for word in simple_preprocess(str(doc)) if word not in stop_words]


def remove_stopwords(texts,stop_words):
    '''Takes a list of documents and removes the stopwords from each one.
    
    Args:
        texts: list of strings
            List of the documents to be processed
        stop_words: list
            List of stopwords to be removed
                
    Return:
        Document list with all the stopwords removed.
        '''
    return [remove_sw(doc,stop_words) for doc in texts]


def process_doc(doc,id2word,stop_words):
    '''Generates the processed form of a single document.
    
    Args:
        doc: string
            document to be processed
        id2word: gensim.corpora.dictionary.Dictionary
            dictionary used to process the document.
        stop_words: list
            List of stopwords to be removed
                
    Return: list of tuples
        Processed version of the document.
        '''
    words = remove_sw(doc,stop_words)
    bigram_mod = bigrams(words)
    bigram = bigram_mod[words]
    corpus = id2word.doc2bow(bigram)
    return corpus


def bigrams(words, bi_min=15):
    '''Creates a Phraser for converting words into bigrams. 
    
    Args:
        words: list
            documents to be conveted to bigrams.
        bi_min: int
            minimum count threshold for detecting bigrams.
                
    Return: Phraser
        gensim Phraser model for converting words to bigrams.
        '''
    
    bigram = Phrases(words, min_count = bi_min)
    bigram_mod = Phraser(bigram)
    return bigram_mod


def refactor_corpus(bigram,below=15,above=0.35):
    '''Re-generates corpus using custom filter parameters.
    
    Args:
        doc: string
            document to be processed
        id2word: gensim.corpora.dictionary.Dictionary
            dictionary used to process the document.
                
    Return: list of tuples
        Processed version of the document.
        '''
    
    id2word = gensim.corpora.Dictionary(bigram)
    id2word.filter_extremes(no_below=below, no_above=above)
    id2word.compactify()
    corpus = [id2word.doc2bow(text) for text in bigram]
    return corpus, id2word


def get_corpus(texts,stop_words):
    '''Generates a corpus of processed documents:
    Removes stopwords, generates bigrams, and creates a dictionary.
    The dictionary is then used to process the text.
    
    Args:
        texts: string
            document to be processed
        stop_words: list
            List of stopwords to be removed
                
    Return:
        corpus: list
            List of processed documents.
            
        id2word: gensim.corpora.dictionary.Dictionary
            dictionary used in processing the documents.
            
        bigram: list of documents broken into bigrams.
        '''
    
    words = remove_stopwords(texts,stop_words)
    bigram_mod = bigrams(words)
    bigram = [bigram_mod[plot] for plot in words]
    id2word = gensim.corpora.Dictionary(bigram)
    id2word.filter_extremes(no_below=15, no_above=0.35)
    id2word.compactify()
    corpus = [id2word.doc2bow(text) for text in bigram]
    return corpus, id2word, bigram