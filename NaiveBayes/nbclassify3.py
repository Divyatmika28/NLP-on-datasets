import os 
import re
import math
import sys
from ast import literal_eval

model_params = open("nbmodel.txt", "r")

unique_words_set = literal_eval(model_params.readline().strip())

total_vocab_len = int(model_params.readline().strip())

negative_deceptive_model = literal_eval(model_params.readline().strip())
negative_deceptive_count = int(model_params.readline().strip())

negative_truthful_model = literal_eval(model_params.readline().strip())
negative_truthful_count = int(model_params.readline().strip())

positive_deceptive_model = literal_eval(model_params.readline().strip())
positive_deceptive_count = int(model_params.readline().strip())

positive_truthful_model = literal_eval(model_params.readline().strip())
positive_truthful_count = int(model_params.readline().strip())

each_class_word_count = {}
each_class_word_count['negative deceptive'] = sum(negative_deceptive_model.values())
each_class_word_count['negative truthful'] = sum(negative_truthful_model.values())
each_class_word_count['positive deceptive'] = sum(positive_deceptive_model.values())
each_class_word_count['positive truthful'] = sum(positive_truthful_model.values())

test_files = []
test_path = sys.argv[1]
for root, dir, files in os.walk(test_path):
    for file in files:
        file_path = os.path.join(root,file)
        if '.txt' in file and file_path.find("README") ==-1:
            test_files.append(os.path.join(root, file))



prior_probability = {}
prior_probability["negative deceptive"] = negative_deceptive_count/total_vocab_len
prior_probability["negative truthful"] = negative_truthful_count/total_vocab_len
prior_probability["positive deceptive"] = positive_deceptive_count/total_vocab_len
prior_probability["positive truthful"] = positive_truthful_count/total_vocab_len

output_file = 'nboutput.txt'
output_file = open(output_file, "w")

alpha = 0.45 #SMOOTHING 
for file_path in test_files:
    negative_deceptive_probablity = prior_probability["negative deceptive"]
    negative_truthful_probablity = prior_probability["negative truthful"]
    positive_deceptive_probablity = prior_probability["positive deceptive"]
    positive_truthful_probablity = prior_probability["positive truthful"]
    review = open(file_path,"r")
    review = review.read()
    review = review.lower()
    review = re.sub('[^ a-zA-Z0-9]', '', review)
    review =review.split(" ")
    for word in review:
        word = word.strip()
        negative_deceptive_probablity *= (negative_deceptive_model.get(word,0)+alpha)/(each_class_word_count['negative deceptive']+alpha*len(unique_words_set))
        positive_deceptive_probablity *= (positive_deceptive_model.get(word,0)+alpha)/(each_class_word_count["positive deceptive"]+alpha*len(unique_words_set))
        negative_truthful_probablity *= (negative_truthful_model.get(word,0)+alpha)/(each_class_word_count["negative truthful"]+alpha*len(unique_words_set))
        positive_truthful_probablity *= (positive_truthful_model.get(word,0)+alpha)/(each_class_word_count["positive truthful"]+alpha*len(unique_words_set))
        
        max_probability_class = max(negative_deceptive_probablity,
                 negative_truthful_probablity,
                 positive_deceptive_probablity,
                 positive_truthful_probablity)
        
        negative_deceptive_probablity/= max_probability_class
        negative_truthful_probablity /= max_probability_class
        positive_deceptive_probablity /= max_probability_class
        positive_truthful_probablity /= max_probability_class

    if negative_deceptive_probablity == 1:
        output_file.write("deceptive negative "+file_path+"\n")
        #print("hello")
    elif negative_truthful_probablity == 1:
        output_file.write("truthful negative "+file_path+"\n")
        #print("divya")
    elif positive_deceptive_probablity == 1:
        output_file.write("deceptive positive "+file_path+"\n")
        #print("jj")
    else: 
        output_file.write("truthful positive "+file_path+"\n")
        #print("what")

