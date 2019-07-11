#Theme-eter

---
Instructions for use:

Replicating the experiment:
    - In 'dev', you can open 'wiki_api.ipynb' to view the steps used for data collection,
    but the dataset takes a long time to collect, so it is recommended to use the included
    dataset in the data folder.
    
    - To run the experiment, open 'model.ipynb'. 
    - Instructions are included for importing data from the included json files.
    - The data is then processed using functions from text_processing,
    and then used to create a series of models to find the best number of topics.
    
    
    
Running the App:
    -to run the app, from this directory run:
    `FLASK_APP=themeter/webapp/app.py flask run`
    



