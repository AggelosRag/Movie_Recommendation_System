

import csv
from elasticsearch import helpers, Elasticsearch


es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

with open('movies.csv',encoding="utf8") as outfile:
    reader = csv.DictReader(outfile)
    helpers.bulk(es, reader, index="index_name", doc_type="type")
    
