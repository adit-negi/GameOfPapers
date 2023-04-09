import psycopg2
import json
from pathlib import Path

#Establishing the connection
conn = psycopg2.connect(
   database="hello_flask_dev", user='hello_flask', password='hello_flask', host='127.0.0.1', port= '5432'
)
#Setting auto commit false
conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

json_data = open('/Users/adit/GameOfPapers/baseline_model_experiments/finetuned-scibert/results.json')
data = json.load(json_data)

for paper_id in data:
    recommendations = []
    pid = paper_id
    for recs in data[paper_id]:
        similartiy = recs[0]
        summary = recs[1]
        paper_id = str(recs[2])
        query = "select id from research_papers where paper_id = %s;"
        cursor.execute(query, (paper_id,))
        result = cursor.fetchone()
        postgres_id = result[0]
        recommendations.append({"paper_id":paper_id,"similarity":similartiy,"summary":summary, "id":postgres_id})
    recommendations_json = json.dumps(recommendations)
    query = "update research_papers set recommendations = %s where paper_id = %s;"
    cursor.execute(query, (recommendations_json, pid))
        

print(result[0])
conn.commit()
print("Records inserted........")

# Closing the connection
conn.close()