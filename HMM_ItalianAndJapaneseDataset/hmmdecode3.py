import sys
import json
import os



hmmhmmmodel_dict = open('hmmmodel.txt', 'r', encoding='UTF-8')
hmmmodel = json.loads(hmmhmmmodel_dict.read())
hmmhmmmodel_dict.close()

transition_prob_dict = hmmmodel['transition']
emission_prob_dict = hmmmodel['emission']
count_tags_dict = hmmmodel['tags']
freq_count_tags = hmmmodel['freq_word_tag_dict']

testdata = sys.argv[1]

f = open(testdata, 'r', encoding='UTF-8')
corpus = f.read()
corpus_sentences = corpus.splitlines()
sentence_tagger= []



for sentence in corpus_sentences:
    wordList = sentence.split()
    firstWord = wordList[0]
    hmmmodel_args = []
    hmmmodel_args.append({})
    
    hmm_states = {}
    if firstWord in emission_prob_dict.keys():
        hmm_states = emission_prob_dict[firstWord]
    else:
        hmm_states = freq_count_tags
    for tag in hmm_states:
        if tag == 'beg' or tag=='end':
            continue
        elif firstWord in emission_prob_dict:
            e_values = emission_prob_dict[firstWord][tag]
        
        else:
            e_values = 1  
        hmmmodel_args[0][tag] = {}
        hmmmodel_args[0][tag]['prob'] = e_values * transition_prob_dict[tag]['beg']
        hmmmodel_args[0][tag]['bp'] = 'beg'
        
    for i in range(1,len(wordList)+1):
        if i==len(wordList):
            lastword = hmmmodel_args[-1]
            hmm_states = lastword.keys()
            maxProb ={'prob':0,'bp':''}
            hmmmodel_args.append({})
            for tag in hmm_states:
                if tag=='end':
                    continue
                else:
                    prevProb = hmmmodel_args[-2][tag]['prob'] * transition_prob_dict['end'][tag]

                    if (prevProb>maxProb['prob']):
                        maxProb['prob'] = prevProb
                        maxProb['bp'] = tag

            hmmmodel_args[-1]['end'] = {}
            hmmmodel_args[-1]['end']['prob'] = maxProb['prob']
            hmmmodel_args[-1]['end']['bp'] = maxProb['bp']
        else:    
            currentWord = wordList[i]
            hmmmodel_args.append({})
            if currentWord in emission_prob_dict:
                hmm_states = emission_prob_dict[currentWord]
            else:
                hmm_states = freq_count_tags
            for tag in hmm_states:
                if tag=='start' or tag=='end':
                    continue
                elif currentWord in emission_prob_dict:
                    e_values = emission_prob_dict[currentWord][tag]
               
                else:
                    e_values = 1  
                maxProb ={'prob':0,'bp':''}
                for lastTag in hmmmodel_args[i-1]:
                    if lastTag=='beg' or lastTag=='end':
                        continue
                    else:
                        prevProb = hmmmodel_args[i-1][lastTag]['prob'] * e_values * transition_prob_dict[tag][lastTag]

                        if(prevProb>maxProb['prob']):
                            maxProb['prob'] = prevProb
                            maxProb['bp'] = lastTag

                hmmmodel_args[i][tag] = {}
                hmmmodel_args[i][tag]['prob'] = maxProb['prob']
                hmmmodel_args[i][tag]['bp'] = maxProb['bp']
    
    curState = len(wordList)
    curTag = 'end'
    res = ""
    i = len(wordList)-1
    while i>=0:
        res = wordList[i]+"/"+hmmmodel_args[curState][curTag]['bp']+" " + res
        curTag = hmmmodel_args[curState][curTag]['bp']
        curState = curState-1
        i-=1
    
    
    sentence_tagger.append(res)
                
fwrite = open('hmmoutput.txt', 'w', encoding = 'UTF-8')
for s in sentence_tagger:
    fwrite.write(s+'\n')