import fitz # PyMuPDF :: using pip install PyMuPDF
import re
from datetime import datetime
import json
import ftfy
import os

# Load the PDF file
#with open('..\pdf\GaugeEquivariantMeshCNNsAnisotropicconvolutionsongeometricgraphs.pdf', 'rb') as file:
#    pdf_data = file.read()




def clean_abstract_title(text):
    #abstract = abstract.encode().decode("utf-8")
    text = ftfy.fix_text(text)
    text = text.replace('\n', ' ')
    text = text.strip()
    return text


def get_title(text_blocks):
    try:
        
        # ICMR PDF Modifications
        title = ''
        #print(text_blocks)
        for index, block in enumerate(text_blocks):
            if not title and block[4]:
                title_index = index
                title += block[4]
        
        #for ICLR conferences
        if "ICLR" in title:
            text_blocks.pop(0)
            title,title_index = get_title(text_blocks)
            title_index = 1
        
        return clean_abstract_title(title),title_index

    except Exception as e:
        raise e

def get_abstract(text_blocks):
    try:
        abstract = ''
        abstract_index = -1
        abstract_found = False
        for index, block in enumerate(text_blocks):
            if 'abstract' in block[4].lower():
                abstract_found = True
                abstract_index = index
                continue
            if abstract_found:
                abstract += block[4] + ' '
                break
        
        return clean_abstract_title(abstract), abstract_index

    except Exception as e:
        raise e
   

def check_list(author):
    unwanted_list = ['university','research','lab','college','school','institute','technology','abstract','team','inc','china','india','UK','Electronics',
                     'Tianjin','USA', 'Angeles','Department','Computer','Science','Universidade','Brazil','Australia','Block','South','Associates' 
                     'County','Republic','KAIST','and','Academy','Switzerland','Delhi','IIIT','Machine','Oceanic','Engineering','Amazon','United','Korea'
                     'Nanjing','Melbourne','San Diego','Stanford','Facebook','Shenzhen','Beijing','Electric','Industry','Technologies','Singapore','Berkeley','width','height','image',
                     'Germany','Zurich'
                     
                     ]

    for word in unwanted_list:
        if word.lower() in author.lower():
            return ''
    author.strip()
    if " " not in author or author.count(' ') >= 3:
        return ''
    
    return author

def clean_email(author_block):
    # define a regular expression pattern to match email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # use a list comprehension to filter out non-matching items
    final_authors = [item for item in author_block if not '@' in item]
    
    return final_authors
 
def split_authors(author_block,split_string):
    #Splitting the author names by \n and getting the sub lists 
    sublists = []
    for string in author_block:
        sublist = string.split(split_string)
        sublists.append(sublist)
    
    author_block = sublists
    
    #Merging all the sub lists within the list into one big list to fix
    sublists = []
    for sublist in author_block:
        for item in sublist:
            sublists.append(str(item))
    
    author_block = sublists
    return author_block

def get_authors(text_blocks,title_index,abstract_index):
    author_block = []
    for i in range(int(title_index)+1,int(abstract_index)+1):
       author_block.append(text_blocks[i][4])

    author_block = split_authors(author_block,'\n')
    author_block = clean_email(author_block)
    author_block = split_authors(author_block,',')    
    
    #Cleaning any string that have email in them
    author_block = clean_email(author_block)
    
    clean_authors = []
    #Now final clean up of the authors
    for author in author_block:
        author = re.sub('[^A-Za-z0-9]+', ' ', author)
        author = author.lstrip()
        author = author.rstrip()
        pattern = r'[0-9]'
        # Match all digits in the string and replace them with an empty string
        author = re.sub(pattern, '', author)
        #Removing all those items where it is a university name or something similar 
        author = check_list(author)
        
        if(author != ''):
            clean_authors.append(author)
        
    author_block = clean_authors
    

    
    return author_block[:10]
    
    
def get_created_time(pdf):
    # Get the metadata
    metadata = doc.metadata
    
    created_time = metadata.get('creationDate')[2:10]
    
    try:
        #Extracting only the date
        created_time = datetime.strptime(created_time, '%Y%m%d').date()
        # Convert the date object to a formatted string
        created_time = created_time.strftime('%d %B %Y')
    except:
        print('Some issue with created_time format')
    
    return created_time


for root, dirs, files in os.walk("/Users/adit/papers/"):
    print(dirs)
    break


for dir in dirs:
    print('../papers/' + dir)

output = []
cnt = 0
for cur_dir in dirs:
    my_dir = '/Users/adit/papers/' + cur_dir
    for filename in os.listdir(my_dir):
        # check if the file is a PDF
        if filename.endswith(".pdf"):
            # open the PDF file using PyMuPDF
            try:
                with fitz.open(os.path.join(my_dir, filename)) as doc:        
                    # Select the first page
                    page = doc[0]
                    text_blocks = page.get_text_blocks()

                    title,title_index = get_title(text_blocks)
                    # Get abstract of the document
                    abstract, abstract_index = get_abstract(text_blocks)
                    text_blocks = page.get_text_blocks()
                    authors = get_authors(text_blocks,title_index,abstract_index)
                    created_time = get_created_time(doc)
                    conference = cur_dir
                    cnt+=1
                    if abstract.count(" ") <20:
                        continue
                    
                    if title=='' or abstract=='':
                        continue
                    
                    output.append({"internal_id":cnt,"title": title, "abstract": abstract, "authors":authors,"created_time":created_time,"conference":conference, 'filepath':my_dir+"/"+filename})

            except:
                print('issue with: ' + str(filename))
                continue
print(cnt)
print(len(output))
with open('./samir.json', 'w') as f:
    json.dump(output, f, indent=4)
            

#with fitz.open('./test/NeuroMLRRobustReliableRouteRecommendationonRoadNetworks.pdf') as doc:  
#    page = doc[0]
#    text_blocks = page.get_text_blocks()
    #(x0, y0, x1, y1, "word", block_no, line_no, word_no)
    
    
#    title,title_index = get_title(text_blocks)
   
    # Get abstract of the document
  #  abstract, abstract_index = get_abstract(text_blocks)
 #   text_blocks = page.get_text_blocks()
   # authors = get_authors(text_blocks,title_index,abstract_index)
    #created_time = get_created_time(doc)
    

    
   # output = []
   # output.append({"title": title, "abstract": abstract, "authors":authors,"created_time":created_time})
   # print(output)
    
    
    # Save the output data to a JSON file
    #with open('./samir.json', 'w') as f:
     #   json.dump(output, f, indent=4)
    #print(text_blocks)
    #print(title)
    #print(abstract)
    #print(abstract_index)
    #print(title_index)
    #print(authors)
    #for item in authors:
    #    print(type(item))



