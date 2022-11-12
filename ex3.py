#!/usr/bin/env python
# coding: utf-8

# Libraries
# -------------------------------------------------------------------------------------------------------------------------

# In[ ]:


import sys
import json
from pprint import pprint
from datetime import datetime
import csv
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans


# Read the csv files 
# -------------------------------------------------------------------------------------------------------------------------

# In[ ]:


ratings = pd.read_csv( '/Users/AngelosRgs/Desktop/ratings.csv' ) 
movies = pd.read_csv( '/Users/AngelosRgs/Desktop/movies.csv' )


# Create a dataframe where each row is a user and each column has the average rating of this user for a movie genre 
# ------------------------------------------------------------------------------------------------------------------

# In[ ]:


all_unique_userIds = ( ratings["userId"].unique() )
all_unique_genres = ( movies["genres"].unique() )
df = np.transpose( [ np.tile(all_unique_userIds, len(all_unique_genres)), np.repeat(all_unique_genres, len(all_unique_userIds))])
all_genres_per_userId = pd.DataFrame( df, columns = ["userId","genres"] )


# In[ ]:


merged_csv = pd.merge( ratings, movies, on = "movieId" )
avg_ratings_per_uId_genres = merged_csv.groupby( ['userId', 'genres'] )["rating"].mean().reset_index()
all_avg_ratings_per_uId_genres = pd.merge( all_genres_per_userId, avg_ratings_per_uId_genres, on= ['userId', 'genres'], how="left" )
all_avg_ratings_per_uId_genres["rating"] = all_avg_ratings_per_uId_genres.rating.fillna(0)


# In[ ]:


kmeans_input = pd.pivot_table( all_avg_ratings_per_uId_genres, index='userId', columns='genres', values='rating' )


# KMeans clustering with 6 clusters
# ------------------------------------------------------------------------------------------------------------------

# In[ ]:


kmeans=KMeans( n_clusters=6, init='k-means++',random_state=0 )
y=kmeans.fit_predict( kmeans_input )
centers = pd.DataFrame( kmeans.cluster_centers_ )
centers.columns = kmeans_input.columns.values


# Create a final dataframe where each row is a user and each column has the rating of the user for a movie
# ------------------------------------------------------------------------------------------------------------------

# In[ ]:


all_movieId = (movies["movieId"])
df2 = np.transpose([np.tile(all_unique_userIds, len(all_movieId)), np.repeat(all_movieId, len(all_unique_userIds))])
all_userIds_movieIds = pd.DataFrame( df2, columns = ["userId","movieId"] )
final_table = pd.merge( all_userIds_movieIds, ratings, on=["userId","movieId"], how="left" )
final_table = final_table.drop( "timestamp", axis = 'columns' )
final_table = final_table.sort_values( by = 'movieId', ascending= False )
final_table = pd.pivot_table( final_table, index='userId', columns='movieId', values='rating', dropna=False )


# For each user, fill the missing ratings for every movie with its average rating given by the other users of the same cluster 
# ------------------------------------------------------------------------------------------------------------------

# In[ ]:


#del final_table3
final_table3 = pd.DataFrame(columns=final_table.columns)
final_table['Clusters'] = y

for i in range (6):
    k1 = final_table.loc[final_table['Clusters'] == i]
    k2 = k1.apply(lambda x: x.fillna(x.mean()),axis=0)
    final_table3 = final_table3.append(k2)

final_table = final_table3.sort_index()

# fill the movies with no rating with an average rating of 2.5/5.0
final_table = final_table3.fillna(2.5)
final_table = final_table3.drop('Clusters', axis=1)


# Load the results from the query of the previous exercise
# ------------------------------------------------------------------------------------------------------------------

# In[ ]:


from numpy import load

# load array
data = load('erotima2_result.npy', allow_pickle = True)
id_list = data[0]
average_rating = data[1]
score_list = data[2]
full_info = data[3]
userId = data[4]
print(data)


# Save the new ratings of ex.3 for the given user in ex.2 and for the given movie titles in ex.2
# ------------------------------------------------------------------------------------------------------------------

# In[ ]:


rated_by_user=np.zeros(len(id_list))

for i in range(len(id_list)):
    k1 = final_table.iloc[int(userId)]
    index = int(id_list[i])
    rated_by_user[i] = k1[index]
print(rated_by_user)


# Combine the new scores with the existing metrics
# -------------------------------------------------------------------------------------------------------------------------

# In[ ]:


#new metric
new_scores=[]

for i in range(len(id_list)):
    new_score=0.30*rated_by_user[i]+0.10*average_rating[i]+0.60*score_list[i]
    new_scores.append(new_score)
    
print("The new scores are:") 
print(new_scores)

#enwnetai olh h pliroforia me thn stili twn newn score ths neas metrikis
result = np.vstack((full_info,new_scores)).T
print(result)


# In[ ]:




