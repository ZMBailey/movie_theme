# Movie Theme-eter

### Business Understanding
We all like movies, but we all like certain kinds of movies. Maybe you feel like a movie with a certain theme, but you only know a few like that. I propose to create a model that will analyze a movie for themes, and then accept a theme and return movies closely matching that theme.

### Data Understanding
This project will require plot summaries. Sites like IMDB have ready collections of summaries, which could be useful, but wikipedia will have more verbose entries. Wikipedia also has decent lists of movies by year, which are relatively easy to navigate. With this in mind, I will begin by using the Wikipedia API to gather a collection of movie plot summaries.

### Data Preparation
By going over the movies by year in wikipedia, I should be able to gather 800+ movies per year, and even more from recent years. I will store the entries using MongoDB. I will then process each summary by tokenizing and vectorizing it, to extract features. It will be difficult to find appropriate labels for each summary, so I propose to use clustering to find common themes among movies, and use those for labels. 

### Modeling
With the number of entries I should be able to collect, I will be able to set aside ~20% for testing, and use the rest for training. I’m going to try using LDA to extract topics from summaries. For classification I will use a RandomForest, XGBoost, or Logisitic Regression. Once I can predict themes from a summary, I plan to use clustering data to take a single theme and show the top x number of movies matching that theme.

### Evaluation
I will report both the accuracy score and cross entropy loss, on training and test data. Movie goers only have so much time for movies, and we want to respect that by selecting thresholds that will help us avoid wasting time on the wrong movie. I plan to use k-fold cross validation to do any needed parameter tuning.

### Deployment
The model will be deployed as a Flask app that will allow the user to select a movie or a theme. If selecting a movie it will return a list of themes, if selecting a theme it will return a list of movies matching that theme.

A user, John, likes movies. John gets a recommendation for a movie from a friend, but he doesn’t know anything about it. He doesn’t want to read a full summary, but he wants to have some basic ideas about what the movie is about before he commits 2 hours, plus however long it takes him to track down a means to watch the movie. Now John can look up the movie using the Theme-eter, and see a list of topics/themes that the movie involves. This provides a means to get an idea of the movie, without spoilers.

Now John has decided he’ll like the movie, and watched it last night. He ended up liking it so much, he wants to find similar movies. By selecting one of the themes involved in the movie, John can see a list of movies also involving that theme. 
