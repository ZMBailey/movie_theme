import gensim
from gensim.models import CoherenceModel

def get_coherence_vals(start,end,step,corpus,id2word,bigram,rand_state):
    '''runs a series of models with increasing numpers of topics, 
        and returns the list of models along with their coherence scores.
            
            Args:
                start: int
                    the starting number of topics.
                end: int
                    the ceiling number of topics.
                step: int
                    the number to increment between lda models.
                corpus: int
                    the corpus to train the lda model on.
                id2word: int
                    the id2word dictionary to use in the lda model.
                bigram: int
                    the set of bigrams to use in the coherence model.
                rand_state: int
                    the random state to use in the lda model.
                
            Return:
                first: tuple
                    tuple with the score and the corresponding topic and set of keywords
                    for the highest ranking topic.
                scnd: tuple
                    same as first, but for the second highest ranking topic.'''
    
    coherence_values = []
    model_list = []
    for num_topics in range(start,end,step):
        model = gensim.models.LdaMulticore(corpus=corpus,
                                           num_topics=num_topics,
                                           id2word=id2word,
                                           chunksize=100,
                                           eval_every=1,
                                           per_word_topics=True,
                                           passes=20,
                                           workers=3,
                                           random_state=rand_state)
        model_list.append(model)

        coherencemodel = CoherenceModel(model=model, 
                                        texts=bigram,
                                        dictionary=id2word,
                                       coherence='c_v')
        print('model with ' + str(num_topics) + ' topics')
        coherence_values.append(coherencemodel.get_coherence())
    
    return model_list,coherence_values