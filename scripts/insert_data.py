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
json_data = open('samir.json')
data = json.load(json_data)
id = 1
for data in data:

# Preparing SQL queries to INSERT a record into the database.
    file_path = Path(data['filepath'])
    with open(file_path, 'rb') as f:
        file_contents = f.read()
    paper_id = data['internal_id']
    title = data['title']
    abstract = data['abstract']
    authors = data['authors']
    authors_json = json.dumps(authors)

    conference = data['conference']
    paper_published_at = data['created_time']

    # Construct the SQL query with placeholders
    query = '''INSERT INTO research_papers(id, created_at, updated_at, paper_id,
        active, version, title, abstract, authors, conference, paper_published_at,paper) VALUES (%s, NOW(), NOW(), %s, true, 1, %s, %s, %s::jsonb, %s, %s, %s)'''

    # Pass the values as parameters to the execute method
    cursor.execute(query, (id, paper_id, title, abstract, authors_json, conference, paper_published_at, file_contents))
    id+=1
    print(id)


# Commit your changes in the database
conn.commit()
print("Records inserted........")

# Closing the connection
conn.close()