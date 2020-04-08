### This program is a very simple lemmatizer, which learns a
### lemmatization function from an annotated corpus. The function is
### so basic I wouldn't even consider it machine learning: it's
### basically just a big lookup table, which maps every word form
### attested in the training data to the most common lemma associated
### with that form. At test time, the program checks if a form is in
### the lookup table, and if so, it gives the associated lemma; if the
### form is not in the lookup table, it gives the form itself as the
### lemma (identity mapping).

### The program performs training and testing in one run: it reads the
### training data, learns the lookup table and keeps it in memory,
### then reads the test data, runs the testing, and reports the
### results.

### The program takes two command line arguments, which are the paths
### to the training and test files. Both files are assumed to be
### already tokenized, in Universal Dependencies format, that is: each
### token on a separate line, each line consisting of fields separated
### by tab characters, with word form in the second field, and lemma
### in the third field. Tab characters are assumed to occur only in
### lines corresponding to tokens; other lines are ignored.

import sys
import re

### Global variables

# Paths for data are read from command line
train_file = sys.argv[1]
test_file = sys.argv[2]

# Counters for lemmas in the training data: word form -> lemma -> count
lemma_count = {}

# Lookup table learned from the training data: word form -> lemma
lemma_max = {}

# Variables for reporting results
training_stats = ['Wordform types' , 'Wordform tokens' , 'Unambiguous types' , 'Unambiguous tokens' , 'Ambiguous types' , 'Ambiguous tokens' , 'Ambiguous most common tokens' , 'Identity tokens']
training_counts = dict.fromkeys(training_stats , 0)

test_outcomes = ['Total test items' , 'Found in lookup table' , 'Lookup match' , 'Lookup mismatch' , 'Not found in lookup table' , 'Identity match' , 'Identity mismatch']
test_counts = dict.fromkeys(test_outcomes , 0)

accuracies = {}

### Training: read training data and populate lemma counters

train_data = open (train_file,'r')
wordforms = []
lemmas = []
for line in train_data:
    
    # Tab character identifies lines containing tokens
    if re.search ('\t' , line):

        # Tokens represented as tab-separated fields
        field = line.strip().split('\t')

        # Word form in second field, lemma in third field
        form = field[1]
        lemma = field[2]
        wordforms.append(form)
        lemmas.append(lemma)
        key = (form,lemma)
        if key not in lemma_count:
            lemma_count[key]=1
        else:
            val = lemma_count.get(key)
            lemma_count[key]=val+1
            
lemma_count_dict = {}
lemma_wordform_dict = {}
for key,value in lemma_count.items():
    wordform = key[0]
    lemma = key[1]
    if wordform not in lemma_count_dict:
        val = []
        val.append((lemma,value))
        lemma_count_dict[wordform] = val
    else:
        pair = lemma_count_dict.get(wordform)
        pair.append((lemma,value))
        lemma_count_dict[wordform] = pair
    if lemma not in lemma_wordform_dict:
        val = []
        val.append((wordform,value))
        lemma_wordform_dict[lemma]=val
    else:
        pair = lemma_wordform_dict.get(lemma)
        pair.append((wordform,value))
        lemma_wordform_dict[lemma] = pair
        
lemma_max = {}
umambiguous_tokens = []
ambiguous_tokens = []
unambiTokens = 0 
ambiTokens = 0 
ambimostcommon = 0 
identitytokens = 0 
maxlemmatoken = 0 
for key,value in lemma_count_dict.items():
    if len(value)==1:
        lemma_max[key] = value[0][0]
        if key==value[0][0]:
            identitytokens = identitytokens + value[0][1]
        umambiguous_tokens.append(key)
        unambiTokens = unambiTokens + value[0][1]
        maxlemmatoken = maxlemmatoken + value[0][1]
    else:
        ambiguous_tokens.append(key)
        i = 0 
        maxm = 0 
        for i in range(len(value)):
            lemma = value[i][0]
            count = value[i][1]
            ambiTokens = ambiTokens + count
            if key==value[i][0]:
                identitytokens = identitytokens + value[i][1]
            if count>maxm:
                maxm = count
                final_lemma = lemma
                
        maxlemmatoken = maxlemmatoken + maxm
        ambimostcommon = ambimostcommon + maxm   
        lemma_max[key] = final_lemma
        


accuracies['Expected lookup'] = maxlemmatoken/len(lemmas)### Calculate expected accuracy if we used lookup on all items ###

accuracies['Expected identity'] = identitytokens/len(lemmas)### Calculate expected accuracy if we used identity mapping on all items ###

### Testing: read test data, and compare lemmatizer output to actual lemma
    
test_data = open (test_file , 'r')
testItems = 0 
lookupmatch = 0 
lookupmismatch = 0 
found = 0 
notfound = 0 
match = 0 
mismatch = 0

for line in test_data:

    # Tab character identifies lines containing tokens
    if re.search ('\t' , line):

        # Tokens represented as tab-separated fields
        field = line.strip().split('\t')

        # Word form in second field, lemma in third field
        form = field[1]
        lemma = field[2]
        testItems = testItems + 1
        if form in lemma_max:
            found = found + 1
            val = lemma_max.get(form)   
            if val==lemma:
                lookupmatch = lookupmatch + 1
            else:
                lookupmismatch  = lookupmismatch  + 1        
        else:
            notfound = notfound + 1
            if form==lemma:
                match = match +1
            else:
                mismatch = mismatch + 1

accuracies['Lookup'] = lookupmatch/found### Calculate accuracy on the items that used the lookup table ###

accuracies['Identity'] = match/notfound ### Calculate accuracy on the items that used identity mapping ###

accuracies['Overall'] = found/testItems### Calculate overall accuracy ###

### Report training statistics and test results

training_counts['Wordform types'] = len(set(wordforms)) 
training_counts['Wordform tokens'] = len(wordforms)
training_counts['Unambiguous types'] = len(umambiguous_tokens)
training_counts['Unambiguous tokens'] = unambiTokens
training_counts['Ambiguous types'] = len(ambiguous_tokens)
training_counts['Ambiguous tokens'] = ambiTokens
training_counts['Ambiguous most common tokens'] = ambimostcommon
training_counts['Identity tokens'] = identitytokens


test_counts['Total test items'] = testItems
test_counts['Found in lookup table'] = found
test_counts['Lookup match'] = lookupmatch
test_counts['Lookup mismatch'] = lookupmismatch
test_counts['Not found in lookup table'] = notfound
test_counts['Identity match'] = match
test_counts['Identity mismatch'] = mismatch
                
output = open ('lookup-output.txt' , 'w')

output.write ('Training statistics\n')

for stat in training_stats:
    output.write (stat + ': ' + str(training_counts[stat]) + '\n')

for model in ['Expected lookup' , 'Expected identity']:
    output.write (model + ' accuracy: ' + str(accuracies[model]) + '\n')

output.write ('Test results\n')

for outcome in test_outcomes:
    output.write (outcome + ': ' + str(test_counts[outcome]) + '\n')

for model in ['Lookup' , 'Identity' , 'Overall']:
    output.write (model + ' accuracy: ' + str(accuracies[model]) + '\n')

output.close

