# Movie Theme-eter
___

### Business Understanding
Movie recommendations from friends are tricky. Netflix recommends movies with succinct little topics or themes. But when you friend tells you about a movie they really liked, and they think you should watch it, what do you really know about it? You could look at Wikipedia or IMDB, but that would tell you too much, and might spoil the movie. With the Theme-eter you can enter a plot summary, and it will give you a few keywords to describe the plot.  

### Data Understanding
This project will require plot summaries. Sites like IMDB have ready collections of summaries, which could be useful, but wikipedia will have more verbose entries. Wikipedia also has a list of english language movies as a Category, which makes it easy to navigate. With this in mind, I will begin by using the Wikipedia API to gather a collection of movie plot summaries.

### Data Preparation
By going over the movies by year in wikipedia, I should be able to gather 800+ movies per year, and even more from recent years. I will store the entries using MongoDB. I will then process each summary by tokenizing and vectorizing it, to extract features. It will be difficult to find appropriate labels for each summary, so I propose to use clustering to find common themes among movies, and use those for labels. I will also use Name Entity Recognition to identify and remove names from the text. 

### Modeling
With the number of entries I should be able to collect, I will be able to set aside ~20% for testing, and use the rest for training. I’m going to try using LDA to extract topics from summaries. Then I will be able to use the LDA model to predict probabilities on the topics the model has created.

### Evaluation
I will use coherency scores to examine the different topic models, and to help find meaningful lists of words. The point is to find meaningful topics to summarize a plot, so will be necessary to find topic lists with reasonable themes.

### Deployment
The model will be deployed as a Flask app that will allow the user to select a movie. If selecting a movie it will return a list of themes.

Use-case:
A user, John, likes movies. John gets a recommendation for a movie from a friend, but he doesn’t know anything about it. He doesn’t want to read a full summary, but he wants to have some basic ideas about what the movie is about before he commits 2 hours, plus however long it takes him to track down a means to watch the movie. Now John can look up the movie using the Theme-eter, and see topics/themes that the movie involves. This provides a means to get an idea of the movie, without spoilers.   
