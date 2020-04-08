import os 
import re
import math
import sys

stop_words = {'i', 'me', 'my', 'myself', 'we', 'our', 'ours',
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
              "won't", 'wouldn', "wouldn't"}




negative_fake_words = {}
positive_fake_words = {}
positive_true_words = {}
negative_true_words = {}


label_word_dict = {"negative fake" : negative_fake_words, "negative true" : negative_true_words,
                             "positive fake" : positive_fake_words, "positive true" : positive_true_words}

label_wcount_dict = {"negative fake":0, "positive true":0,"negative true":0,"positive fake":0}
unique_words = set()

inputPath =  sys.argv[1]
negative_true_files = []
negative_fake_files = []
positive_true_files = []
positive_fake_files = []

import string

translator = str.maketrans('', '', string.punctuation)

def remove_stopwords(review):
    changed_review = []
    for word in review.split():
        if word not in stop_words:
            changed_review.append(word)

    return " ".join(changed_review)

for root, dirc, files in os.walk(inputPath):
    for file in files:
        file_path = os.path.join(root,file)
        if '.txt' in file and file_path.find("README") ==-1:
            if "negative" in os.path.join(root, file).lower() and "deceptive" in os.path.join(root, file).lower():
                negative_fake_files.append(os.path.join(root, file))
            if "negative" in os.path.join(root, file).lower() and "truthful" in os.path.join(root, file).lower():
                negative_true_files.append(os.path.join(root, file))
            if "positive" in os.path.join(root, file).lower() and "deceptive" in os.path.join(root, file).lower():
                positive_fake_files.append(os.path.join(root, file))
            if "positive" in os.path.join(root, file).lower() and "truthful" in os.path.join(root, file).lower():
                positive_true_files.append(os.path.join(root, file))
                
                
allFiles = []
allFiles.append(negative_fake_files)
allFiles.append(negative_true_files)
allFiles.append(positive_fake_files)
allFiles.append(positive_true_files)


labels = ["negative fake","negative true","positive fake", "positive true"]
i = 0 
totalFiles = 0 
for i in range(len(allFiles)):
    class_files = allFiles[i]
    totalFiles = totalFiles + len(class_files)
    label  = labels[i]
    for file in class_files:
        file_open = open(file,"r")
        review = file_open.read()
        review = review.lower()
        review = re.sub('[^ a-zA-Z0-9]', '', review)
        review =review.split(" ")
        #review = review.translate(translator) 
        #review = remove_stopwords(review)
        for word in review:
            #print(word)
            #word = word.lower()
            label_word_dict[label][word] = label_word_dict[label].get(word, 0) + 1
            unique_words.add(word)


#print("hello")
#print(len(unique_words))
with open("nbmodel.txt", "w") as model_file :
    model_file.write(str(unique_words))
    model_file.write("\n")
    model_file.write(str(totalFiles))
    model_file.write("\n")
    model_file.write(str(label_word_dict['negative fake']))
    model_file.write("\n")
    model_file.write(str(len(negative_fake_files)))
    model_file.write("\n")
    model_file.write(str(label_word_dict['negative true']))
    model_file.write("\n")
    model_file.write(str(len(negative_true_files)))
    model_file.write("\n")
    model_file.write(str(label_word_dict['positive fake']))
    model_file.write("\n")
    model_file.write(str(len(positive_fake_files)))
    model_file.write("\n")
    model_file.write(str(label_word_dict['positive true']))
    model_file.write("\n")
    model_file.write(str(len(positive_true_files)))






    
