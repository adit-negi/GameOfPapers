import json
def calculate_metrics():
    with open("bert/sample.json", "r") as f:


        d1 = json.load(f)

    with open("jaccard/sample.json", "r") as f:


        d2 = json.load(f)

    with open("tf-idf/sample.json", "r") as f:


        d3 = json.load(f)

    with open("use/use_sample_output.json", "r") as f:


        d4 = json.load(f)


    with open("scibert/sample.json", "r") as f:
        d5 = json.load(f) 
    with open("finetuned-scibert/sample.json", "r") as f:
        d6 = json.load(f)

    with open("longformer/sample.json", "r") as f:
        d7 = json.load(f)

    with open("sample1.json", "r") as f:
        ground_dataset = json.load(f)

    journal_name = ""
    tags = ""
    base_doc_id = "0704.0001"
    journal_name = 'Phys.Rev.D76'
    tag = ground_dataset[base_doc_id]['categories']
    cnt = 1
    m = []
    for i in [d1,d2,d3,d4, d5,d6, d7]:

        c =0
        matches = 0
        for j in i:
            f =False
            id_ = i[j][1]
            if id_ == base_doc_id:
                continue
            tags = i[j][2]
            if tag in tags:
                matches += 1
                f = True

            if ground_dataset[id_]['journal-ref'] and journal_name in ground_dataset[id_]['journal-ref'] and not f:
                matches += 1
            c += 1
            if c == 300:
                break
        m.append(matches)
        print("Matches", matches)
        cnt += 1
    return m

def process_file():
    f = open('sample.json')
  

    d = json.load(f)
    d1 = {}
    for i in d:
        d1[i['id']] = i
    with open("sample1.json", "w") as f:
        f.write(json.dumps(d1)) 

def calculate_score(m):
    
    
    total_relevant_docs = 0
    with open("sample1.json", "r") as f:
        d5 = json.load(f)
    base_doc_id = "0704.0001"
    journal_name = 'Phys.Rev.D76'
    tag = d5[base_doc_id]['categories']
    for i in d5:
        f = False
        if i== base_doc_id: continue
        tags = d5[i]['categories']
        if tag in tags:
            total_relevant_docs += 1
            f = True

        if d5[i]['journal-ref'] and journal_name in d5[i]['journal-ref'] and not f:
            total_relevant_docs += 1
    cnt = 0
    cnt_model = {0:"bert", 1:'jaccard', 2:'tf-idf', 3:'use', 4:"scibert", 5:'our-finetune-scibert', 6:"cross-doc-longformer"}
    print(total_relevant_docs)
    for i in m:
        print(cnt_model[cnt])
        print(i)
        cnt+=1
        print('PRECISION',i/300)
        print('RECALL', i/total_relevant_docs)
        print()
    
M =calculate_metrics()
calculate_score(M)