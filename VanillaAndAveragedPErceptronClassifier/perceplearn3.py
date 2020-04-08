import sys
import os
import re
import json
import random
import string


def get_freq_review(review):
    token_freq = {}
    #print(review)
    for word in review:
        
        if word in token_freq:
            token_freq[word] += 1
        else:
            token_freq[word] = 1
    return token_freq


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

inputPath = sys.argv[1]#"op_spam_training_data/" #
all_files = []
for root, dirc, files in os.walk(inputPath):
    for file in files:
        file_path = os.path.join(root,file)
        if '.txt' in file and file_path.find("README") ==-1:
            if "negative" in os.path.join(root, file).lower() and "deceptive" in os.path.join(root, file).lower():
                all_files.append((os.path.join(root, file),"negative","deceptive"))
            if "negative" in os.path.join(root, file).lower() and "truthful" in os.path.join(root, file).lower():
                all_files.append((os.path.join(root, file),"negative","truthful"))
            if "positive" in os.path.join(root, file).lower() and "deceptive" in os.path.join(root, file).lower():
                all_files.append((os.path.join(root, file),"positive","deceptive"))
            if "positive" in os.path.join(root, file).lower() and "truthful" in os.path.join(root, file).lower():
                all_files.append((os.path.join(root, file),"positive","truthful"))           
                
                
labels = {'positive':1, 'negative':-1, 'truthful':1, 'deceptive':-1} # to identify class 
weight_td = {"Vanilla":{'bias' : 0},"Averaged":{'bias' : 0}}
weight_pn = {"Vanilla":{'bias' : 0},"Averaged":{'bias' : 0}}
cache_weight_td = {'bias' : 0}
cache_weight_pn = {'bias' : 0}
maxIter = 110
averageIndex = 1
for i in range(maxIter):
    random.shuffle(all_files) # for each iteration shuffle the file for epochs 
    for file in all_files:
        #print(file[0])
        file_open = open(file[0],"r")
        review = file_open.read()
        review = re.sub('[^ a-zA-Z0-9]', '', review)
        review = review.lower().strip()
        review =review.split(" ")
        #review = remove_stopwords(review)
        if len(review)>0:
            word_freq_feat = get_freq_review(review)
            for word,val in word_freq_feat.items(): #initliase weights
                if word not in weight_td['Vanilla']:
                    weight_td['Vanilla'][word]=0
                    weight_td['Averaged'][word] = 0
                    cache_weight_td[word] = 0 
                if word not in weight_pn['Vanilla']:
                    weight_pn['Vanilla'][word]=0
                    weight_pn['Averaged'][word] = 0
                    cache_weight_pn[word] = 0 

            vanilla_activation_pn = weight_pn['Vanilla']['bias']
            vanilla_activation_td = weight_td['Vanilla']['bias']
            averaged_activation_pn = weight_pn['Averaged']['bias']
            averaged_activation_td = weight_td['Averaged']['bias']


            for word in word_freq_feat:
                vanilla_activation_pn += word_freq_feat[word] * weight_pn['Vanilla'][word]
                vanilla_activation_td += word_freq_feat[word] * weight_td['Vanilla'][word]

                averaged_activation_pn += word_freq_feat[word] * weight_pn['Averaged'][word]
                averaged_activation_td += word_freq_feat[word] * weight_td['Averaged'][word]


            if vanilla_activation_pn*labels[file[1]] <=0:
                for word in word_freq_feat:
                    weight_pn['Vanilla'][word] += labels[file[1]] * word_freq_feat[word]
                    weight_pn['Vanilla']['bias'] += labels[file[1]]

            if vanilla_activation_td*labels[file[2]] <= 0:
                    for word in word_freq_feat:
                        weight_td['Vanilla'][word] += labels[file[2]] * word_freq_feat[word]
                        weight_td['Vanilla']['bias'] += labels[file[2]]

            if averaged_activation_pn*labels[file[1]] <= 0:
                for word in word_freq_feat:
                    weight_pn['Averaged'][word] += labels[file[1]] * word_freq_feat[word]
                    weight_pn['Averaged']['bias'] += labels[file[1]]
                    cache_weight_pn[word] += labels[file[1]] * averageIndex  * word_freq_feat[word]
                    #print(word)
                    cache_weight_pn['bias'] += labels[file[1]] * averageIndex

            if averaged_activation_td*labels[file[2]] <= 0:
                for word in word_freq_feat:
                    weight_td['Averaged'][word] += labels[file[2]] * word_freq_feat[word]
                    weight_td['Averaged']['bias'] += labels[file[2]]
                    cache_weight_td[word] += labels[file[2]] * averageIndex  * word_freq_feat[word]
                    cache_weight_td['bias'] += labels[file[2]] * averageIndex

            averageIndex  = averageIndex  + 1
            
          
for keys in weight_pn['Averaged']:
        if keys in cache_weight_pn:
            weight_pn['Averaged'][keys] -= cache_weight_pn[keys]/(averageIndex*1.0)
            
for keys in weight_td['Averaged']:
        if keys in cache_weight_td:
            weight_td['Averaged'][keys] -= cache_weight_td[keys]/(averageIndex*1.0)
            
            
            
vanilla = {'pn': weight_pn['Vanilla'], 'td': weight_td['Vanilla']}
averaged = {'pn': weight_pn['Averaged'], 'td': weight_td['Averaged']}
model_output_file = open('vanillamodel.txt','w')
model_output_file.write(json.dumps(vanilla, indent=2))
model_output_file.close()
model_output_file1 = open('averagedmodel.txt','w')
model_output_file1.write(json.dumps(averaged, indent=2))
model_output_file1.close()
