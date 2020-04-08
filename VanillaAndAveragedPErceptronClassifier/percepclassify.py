import os
import json
import re
import sys

test_path = sys.argv[2] #"op_spam_training_data/negative_polarity/deceptive_from_MTurk/fold1"

test_files = []
for root, dir, files in os.walk(test_path):
    for file in files:
        file_path = os.path.join(root,file)
        if '.txt' in file and file_path.find("README") ==-1:
            test_files.append(os.path.join(root, file))
            
            
def remove_stopwords(review):
    stop_words = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours',
              'ourselves', 'you', "you're", "you've", "you'll",
              "you'd", 'your', 'yours', 'yourself', 'yourselves',
              'he', 'him', 'his', 'himself', 'she', "she's", 'her',
              'hers', 'herself', 'it', "it's", 'its', 'itself',
              'they', 'them', 'their', 'theirs', 'themselves', 'what',
              'which', 'who', 'whom', 'this', 'that', "that'll", 'these',
              'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
              'being', 'have', 'has', 'had', 'having', 'do', 'does',
              'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
              'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by',
              'for', 'with', 'about', 'against', 'between', 'into', 'through',
              'during', 'before', 'after', 'above', 'below', 'to', 'from',
              'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under',
              'again', 'further', 'then', 'once', 'here', 'there', 'when',
              'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few',
              'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
              'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't',
              'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now',
              'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn',
              "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't",
              'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn',
              "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't",
              'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won',
              "won't", 'wouldn', "wouldn't"])
    new_review = []
    #print(review)
    for word in review:
        if word not in stop_words:
            #print(word)
            new_review.append(word)
    return new_review

def get_freq_review(review):
    token_freq = {}
    #print(review)
    for word in review:
        
        if word in token_freq:
            token_freq[word] += 1
        else:
            token_freq[word] = 1
    return token_freq



labels = {'positive':1, 'negative':-1, 'truthful':1, 'deceptive':-1}
output_file = "percepoutput.txt"
output_file = open(output_file, "w")

model_file = open(sys.argv[1]) #open("vanillamodel.txt")
model_param = model_file.read()
model_dict = json.loads(model_param)

for file in test_files:
    file_open = open(file,"r")
    review = file_open.read()
    review = re.sub('[^ a-zA-Z0-9]', '', review)
    review = review.lower().strip()
    review =review.split(" ")
    #review = remove_stopwords(review)
    word_freq_feat = get_freq_review(review)
    activation_pn = model_dict['pn']['bias']
    activation_td = model_dict['td']['bias']
    for word in word_freq_feat:
        if word in model_dict['pn']:
            activation_pn += model_dict['pn'][word]*word_freq_feat[word]
        if word in model_dict['td']:
            activation_td += model_dict['td'][word]*word_freq_feat[word]
            
    if activation_pn>=0:
        label1 = "positive"
    else:
        label1 = "negative"
        
    if activation_td>=0:
        label2 = "truthful"
    else:
        label2 = "deceptive"
    output_file.write(label2+" "+label1+" "+file+"\n")
    #print(label2+" "+label1+" "+file+"\n")
            
            
