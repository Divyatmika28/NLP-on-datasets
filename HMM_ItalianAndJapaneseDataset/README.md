Two files (one Italian, one Japanese) with tagged training data in the word/TAG format, with words separated by spaces and each sentence on a new line.
Two files (one Italian, one Japanese) with untagged development data, with words separated by spaces and each sentence on a new line.
Two files (one Italian, one Japanese) with tagged development data in the word/TAG format, with words separated by spaces and each sentence on a new line, to serve as an answer key.


You will write two programs: hmmlearn.py will learn a hidden Markov model from the training data, and hmmdecode.py will use the model to tag new data. If using Python 3, you will name your programs hmmlearn3.py and hmmdecode3.py. The learning program will be invoked in the following way:

> python hmmlearn.py /path/to/input

The argument is a single file containing the training data; the program will learn a hidden Markov model, and write the model parameters to a file called hmmmodel.txt. The format of the model is up to you, but it should follow the following guidelines:

The model file should contain sufficient information for hmmdecode.py to successfully tag new data.
The model file should be human-readable, so that model parameters can be easily understood by visual inspection of the file.
The tagging program will be invoked in the following way:

> python hmmdecode.py /path/to/input

The argument is a single file containing the test data; the program will read the parameters of a hidden Markov model from the file hmmmodel.txt, tag each word in the test data, and write the results to a text file called hmmoutput.txt in the same format as the training data.

The accuracy of your tagger is determined by a scoring script which compares the output of your tagger to a reference tagged text. Note that the tagged output file hmmoutput.txt must match line for line and word for word with the input to hmmdecode.py. A discrepancy in the number of lines or in the number of words on corresponding lines could cause the scoring script to fail.

Notes
Tags. Each language has a different tagset; the surprise language will have some tags that do not exist in the Italian and Japanese data. You must therefore build your tag sets from the training data, and not rely on a precompiled list of tags.
Slash character. The slash character ‘/’ is the separator between words and tags, but it also appears within words in the text, so be very careful when separating words from tags. Slashes never appear in the tags, so the separator is always the last slash in the word/tag sequence.
Smoothing and unseen words and transitions. You should implement some method to handle unknown vocabulary and unseen transitions in the test data, otherwise your programs won’t work.
Unseen words: The test data may contain words that have never been encountered in the training data: these will have an emission probability of zero for all tags.
Unseen transitions: The test data may contain two adjacent unambiguous words (that is, words that can only have one part-of-speech tag), but the transition between these tags was never seen in the training data, so it has a probability of zero; in this case the Viterbi algorithm will have no way to proceed.
The reference solution will use add-one smoothing on the transition probabilities and no smoothing on the emission probabilities; for unknown tokens in the test data it will ignore the emission probabilities and use the transition probabilities alone. You may use more sophisticated methods which you implement yourselves.
End state. You may choose to implement the algorithm with transitions ending at the last word of a sentence (as in the written homework assignment or in Jurafsky and Martin, figure 8.5), or by adding a special end state after the last word (see for example an older draft of Jurafsky and Martin, figure 9.11). The reference solution will use an end state.
