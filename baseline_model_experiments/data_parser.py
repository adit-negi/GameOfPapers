import json
import time

def get_thousand_papers():
    li = []
    cnt = 0
    with open("/Users/adit/GameOfPapers/arxivDataset.json", "r") as f:
            for l in f:
                if cnt>1000:
                    break
                d = json.loads(l)
                li.append(d)
                cnt += 1

    return li

l = get_thousand_papers()
cat_set =set()
for i in l:
    cats = i['categories'].split(" ")
    for cat in cats:
        cat_set.add(cat)
with open("sample.json", "w") as outfile:
    outfile.write(json.dumps(l))


def get_docs():
    data = get_thousand_papers()
    i = 0
    documents = []
    doc_ids = []
    for doc_id in data:
        if i==0:
            base_document = doc_id['title'] +" " + doc_id['abstract']
            i = i+1
        else:
            documents.append(doc_id['title'] +" " + doc_id['abstract'])
            doc_ids.append((doc_id['id'], doc_id['categories']))

    return base_document, documents, doc_ids

def output_data(scores, documents, doc_ids):
    output = []
    for i in range(len(scores)):
        output.append((scores[i], documents[i], doc_ids[i][0],doc_ids[i][1] ))
    output.sort(reverse=True)

    d= {}
    for i, j,l,k in output:
        
        d[str(i)] = [j,l,k]
    json_object = json.dumps(d, indent=4)
    return json_object
