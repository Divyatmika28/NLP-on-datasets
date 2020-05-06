import sys
import json
import os
import glob

def get_emission_prob(tag_word_dict):       
    emission_prob_dict= {}
    for tag in tag_word_dict:
        for word in tag_word_dict[tag]:
            if word not in emission_prob_dict:
                emission_prob_dict[word] = {}
            if tag not in emission_prob_dict[word]:
                emission_prob_dict[word][tag] = tag_word_dict[tag][word]/tag_count_dict[tag]
            
    return emission_prob_dict


def get_transition_prob(transition_prob_dict):
    for cur_tag in transition_prob_dict:
        for prev_tag in tag_count_dict:
            if prev_tag == 'end':
                continue
            #adding add one smoothing
            elif prev_tag not in transition_prob_dict[cur_tag]:
                transition_prob_dict[cur_tag][prev_tag] = 1/(tag_count_dict[prev_tag]+(4*len(tag_count_dict))-1)
            else:
                transition_prob_dict[cur_tag][prev_tag] = (transition_prob_dict[cur_tag][prev_tag]+1)/(tag_count_dict[prev_tag]+(4*len(tag_count_dict))-1)
    return transition_prob_dict


def get_tag_dict(tag_count_dict):
    tags_dict_ini = dict([(key, {}) for key in tag_count_dict])
    return tags_dict_ini
    

input_training_data = sys.argv[1]

input_file = open(input_training_data, encoding = 'UTF-8')

corpus_words = [line.rstrip('\n').split() for line in input_file]
#print(corpus_words)
tag_count_dict = {}
tag_word_dict = {}
freq_wordtag_dict = {}

tag_count_dict['beg'] = len(corpus_words)
tag_count_dict['end'] = len(corpus_words)

for wordList in corpus_words:
    for label in wordList:
        labels = label.split('/')
        tag = labels[-1]
        word = labels[:-1]
        if tag not in freq_wordtag_dict:
            freq_wordtag_dict[tag] = []
        if word[0] not in freq_wordtag_dict[tag]:
            freq_wordtag_dict[tag].append(word[0])
        word = word[0]
        if tag not in tag_count_dict:
            tag_count_dict[tag] = 1
        else:
            tag_count_dict[tag]+=1
        if tag not in tag_word_dict:
            tag_word_dict[tag] = {}
        if word not in tag_word_dict[tag]:
            tag_word_dict[tag][word] = 1
        else:
            tag_word_dict[tag][word]+=1
            

tags_dict_ini = get_tag_dict(tag_count_dict)
    
for line in corpus_words:
    for i in range(len(line)+1):
        if i==0:
            if 'beg' not in tags_dict_ini[line[i].split('/')[-1]]: 
                tags_dict_ini[line[i].split('/')[-1]]['beg'] = 1
            else:
                tags_dict_ini[line[i].split('/')[-1]]['beg'] += 1
        elif i==len(line):
            if line[i-1].split('/')[-1] not in tags_dict_ini['end']:
                tags_dict_ini['end'][line[i-1].split('/')[-1]] = 1
            else:
                tags_dict_ini['end'][line[i-1].split('/')[-1]] += 1                
        else:
            if line[i-1].split('/')[-1] not in tags_dict_ini[line[i].split('/')[-1]]:
                tags_dict_ini[line[i].split('/')[-1]][line[i-1].split('/')[-1]] = 1
            else:
                tags_dict_ini[line[i].split('/')[-1]][line[i-1].split('/')[-1]] += 1
        

transition_prob_dict = tags_dict_ini
transition_prob_dict = get_transition_prob(transition_prob_dict)
emission_prob_dict = get_emission_prob(tag_word_dict)
freq_wordtag_dict = sorted(freq_wordtag_dict, key=lambda k: len(freq_wordtag_dict[k]), reverse=True)

model = {'tags': tag_count_dict, 'transition': transition_prob_dict, 'emission': emission_prob_dict, 'freq_word_tag_dict': freq_wordtag_dict[0:5]}            


hmmmodel_file = open('hmmmodel.txt', 'w')
hmmmodel_file.write(json.dumps(model, indent=2))


