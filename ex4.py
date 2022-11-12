#!/usr/bin/env python
# coding: utf-8

# Libraries and CSV files
# -------------------------------------------------------------------------------------------------------------------------

# In[11]:


import csv
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import one_hot
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.embeddings import Embedding


# In[12]:


ratings = pd.read_csv('/Users/AngelosRgs/Desktop/ratings.csv') 
movies = pd.read_csv('/Users/AngelosRgs/Desktop/movies.csv')
merged_csv = pd.merge(ratings, movies, on = "movieId")
merged_csv = merged_csv.sort_values(by = "userId")


# Create the Word Embeddings
# ------------------------------------------------------------------------------------------------------------------

# In[13]:


titles = movies["title"]
titles_list = [title for title in titles]

# vocabulary size was estimated around 9000 distinct words
vocab_size = 9000
titles_onehot = [one_hot(d, vocab_size) for d in titles_list]

# We set the maximum title length to 30 words and the embeddings dimensions to 100
sentence_length = 30
dim = 100
embedded_titles = pad_sequences(titles_onehot, padding='pre', maxlen = sentence_length)

#create an embedded layer with keras to find the word embeddings
model=Sequential()
model.add(Embedding(vocab_size, dim, input_length=sentence_length))
model.add(Flatten())
model.compile('adam', 'mse')
word_embeddings = model.predict(embedded_titles)

word_embeddings=pd.DataFrame(word_embeddings)
word_embeddings=pd.concat([movies[["movieId"]], word_embeddings], axis=1)


# Use one-hot encoding for the movie genres and merge them with the embeddings
# ------------------------------------------------------------------------------------------------------------------

# In[14]:


one_hot = movies['genres'].str.get_dummies()
movies_onehot= movies.merge(one_hot, left_index=True, right_index=True)
movies_onehot.drop(['title','genres'],axis=1,inplace=True)

final_df = pd.merge(word_embeddings, movies_onehot, left_on="movieId", right_on="movieId")


# Use one-hot encoding for the ratings (10 labels, from 0 to 5.0)
# ------------------------------------------------------------------------------------------------------------------

# In[15]:


ratings_one_hot=pd.get_dummies(ratings.loc[:, "rating"])
ratings_one_hot=pd.concat([ratings, ratings_one_hot], axis=1)


# Create a function to train a neural network for a given user
# ------------------------------------------------------------------------------------------------------------------

# In[38]:


def trainNeuralNet(ratings_one_hot, user, final_df):
    
    movies_rated = ratings[ratings["userId"] == user][["movieId", "rating"]]
    df_x = pd.merge(final_df, movies_rated[["movieId"]], left_on="movieId", right_on="movieId").drop(['movieId'], axis=1).values
    df_y = ratings_one_hot[(ratings_one_hot["userId"]==user)].iloc[:, 4:]

    X_train,X_test,y_train,y_test = train_test_split(df_x,df_y,test_size=0.1, random_state=2)

    model = Sequential()
    model.add(Dense(178, input_dim = df_x.shape[1], activation = 'relu')) 
    model.add(Dense(16, activation = 'relu'))
    model.add(Dense(10, activation = 'softmax')) # Softmax for multi-class classification

    model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
    model.fit(X_train, y_train, epochs=25, verbose=0)
    
    loss, accuracy = model.evaluate(X_test,y_test)
    print("User % d, Test accuracy  % .5f " %(user, accuracy))
    return model, movies_rated


# Main program
# ------------------------------------------------------------------------------------------------------------------

# In[39]:


from random import randrange

all_unique_userIds = ( ratings["userId"].unique() )

#because of peformance time, test the program for 10 random users
for i in range(10):
    user = randrange( len(all_unique_userIds) )
    model, movies_rated = trainNeuralNet(ratings_one_hot,user,final_df) 
    


# In[ ]:




