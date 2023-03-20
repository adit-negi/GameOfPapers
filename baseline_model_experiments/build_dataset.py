import json
def get_thousand_papers():
    li = []
    cnt = 0
    with open("/Users/adit/GameOfPapers/baseline_model_experiments/30k.json", "r") as f:
        li = json.load(f)
  

    seen = set()
    triplets_list = []
    cnt = 0
    for paper in li:

        print(cnt)
        if cnt%10 ==0:
            print(cnt)
        cnt += 1
        paper_authors = ['{} {}'.format(author[0], author[1]) for author in paper['authors_parsed']]
        paper_categories = paper['categories'].split(" ")
        pos, neg = False, False
        for triplet in li:
            if pos and neg:
                break
            if paper['id'] == triplet['id'] or triplet['id'] in seen:
                continue
            
            triplet_authors = ['{} {}'.format(author[0], author[1]) for author in triplet['authors_parsed']]
            triplet_categories = triplet['categories'].split(" ")
            if len(Intersection(paper_authors, triplet_authors))>0:
                if pos:
                    pass
                else:
                    pos = True
                    if triplet['id'] not in seen:
                        pos_paper = triplet
                        seen.add(triplet['id'])
            else:
                if neg:
                    pass
                else:
                    neg = True
                    if triplet['id'] not in seen:
                        neg_paper = triplet
                        seen.add(triplet['id'])

            if len(Intersection(paper_categories, triplet_categories))>0:
                if pos:
                    pass
                else:
                    pos = True
                    if triplet['id'] not in seen:
                        pos_paper = triplet
                        seen.add(triplet['id'])
            else:
                if neg:
                    pass
                else:
                    neg = True
                    if triplet['id'] not in seen:
                        neg_paper = triplet
                        seen.add(triplet['id'])

        triplets_list.append((paper, pos_paper, neg_paper))
    return triplets_list
            
def Intersection(lst1, lst2):
    return set(lst1).intersection(lst2)

trips = get_thousand_papers()
ids =[]
for i in trips:
    id1, id2, id3 = i[0]['id'], i[1]['id'], i[2]['id']
    ids.append(id1)
    ids.append(id2)
    ids.append(id3)

import csv
with open('paper_triplet_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["", "anchor", "positive", "negative"])
    cnt = 0
    for anchor, pos, neg in trips:
        writer.writerow([cnt, anchor['title'] +" " + anchor['abstract'], pos['title'] +" " + pos['abstract'], neg['title'] +" " + neg['abstract']])


print(len(ids))