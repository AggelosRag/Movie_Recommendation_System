## AI-based Movie Recommendation System

The project was developed for the "Information Retrieval" course. Given a dataset of movies and a dataset of user ratings for each movie, the objective was to:
* Load the datasets on Elasticsearch and Kibana, and perform indicative queries on user ratings and movies.
* Use the BM25 information retrieval metric to sort resembling movie titles, given a specific movie name as input. The movie titles that resemble the most to the given input are shown first.
* Develop a custom information retrieval metric that also takes into account the average rating of each movie.
* Perform K-means clustering on users’ ratings to predict all missing ratings per movie and per user. Each movie that does not have a specific user rating acquires the mean rating of all similar users.
* Create word embeddings and used one-hot encoding on movies’ titles to predict missing ratings with a Neural Network classifier
