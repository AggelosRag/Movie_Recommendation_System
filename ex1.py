#erotima 1

from elasticsearch import Elasticsearch

es=Elasticsearch([{'host':'localhost','port':9200}])

x=input("Give a title: ")

res= es.search(index="index_name",body={'query':{'match':{'title':x}}})
all_results = res['hits']['hits']

for  i in range(len(all_results)):
    print(all_results[i]['_source'])
    
    print("Score: "+str(all_results[i]['_score']))
    









