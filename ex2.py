#erotima2

from elasticsearch import Elasticsearch
import pandas as pd
import numpy as np

es=Elasticsearch([{'host':'localhost','port':9200}])
x=input("Give a title: ")
res= es.search(index="index_name",body={'query':{'match':{'title':x}}})
all_results = res['hits']['hits']

id_list=[]
score_list=[]
full_info=[]

for i in all_results:
    id_list.append(i['_source']['movieId'])   #krataei ta movieid pou epistrafikan
    score_list.append(i['_score'])            #krataei mono ta scores
    full_info.append(i['_source'])            #krataei olh th pliroforia

ratings_data = pd.read_csv("ratings.csv")

#ola ta user id twn users pou vathmologisan
user_id_from_ratings = ratings_data['userId']
user_id_from_ratings = user_id_from_ratings.to_numpy()

#ola ta movies id twn users pou vathmologisan
movie_id_from_ratings = ratings_data['movieId']
movie_id_from_ratings = movie_id_from_ratings.to_numpy()

#oles oi vathmologies twn users pou vathmologisan
rating_from_ratings = ratings_data['rating']
rating_from_ratings = rating_from_ratings.to_numpy()

#oi mesoi oroi twn tainiwn pou epistrafikan apo tis vathmologies twn users
average_rating=[]

for i in range(len(id_list)):
    count =0
    sum_rating=0
    
    for j in range(len(movie_id_from_ratings)):
        if (int(id_list[i])== int(movie_id_from_ratings[j])):
            sum_rating = sum_rating + rating_from_ratings[j]
            count=count+1
    average_rating.append(sum_rating/count)
    
# print("\nThe average ratings are:")
# print(average_rating)


input_id = input("Give a user id: " )
ratings_from_user=[]
movies_from_user=[]

for i in range(len(user_id_from_ratings)):
    if(int(input_id)== int(user_id_from_ratings[i])):
        ratings_from_user.append(rating_from_ratings[i])
        movies_from_user.append(movie_id_from_ratings[i])

# oi vathmologies tou user(pou dwsame san input) gia tis tainies pou gurise h elastic search
        
rated_by_user=np.zeros(len(id_list))

#update
for i in range(len(id_list)):
    for j in range(len(movies_from_user)):
        if(int(id_list[i])==int(movies_from_user[j])):
            rated_by_user[i]=ratings_from_user[j]

#new metric
new_scores=[]

for i in range(len(id_list)):
    new_score=0.30*rated_by_user[i]+0.10*average_rating[i]+0.60*score_list[i]
    new_scores.append(new_score)
        
#enwnetai olh h pliroforia me thn stili twn newn score ths neas metrikis
result = np.vstack((full_info,new_scores)).T
print("\n",result)



