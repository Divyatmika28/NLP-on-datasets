A top-level directory with two sub-directories, one for positive reviews and another for negative reviews (plus license and readme files which you won’t need for the exercise).
Each of the subdirectories contains two sub-directories, one with truthful reviews and one with deceptive reviews.
Each of these subdirectories contains four subdirectories, called “folds”.
Each of the folds contains 80 text files with English text (one review per file).


The perceptron algorithms appear in Hal Daumé III, A Course in Machine Learning (v. 0.99 draft), Chapter 4: The Perceptron.

You will write two programs: perceplearn.py will learn perceptron models (vanilla and averaged) from the training data, and percepclassify.py will use the models to classify new data. If using Python 3, you will name your programs perceplearn3.py and percepclassify3.py. You are encouraged to reuse your own code from Coding Exercise 2 for reading the data and writing the output, so that you can concentrate on implementing the classification algorithm.

The learning program will be invoked in the following way:

> python perceplearn.py /path/to/input

The argument is the directory of the training data; the program will learn perceptron models, and write the model parameters to two files: vanillamodel.txt for the vanilla perceptron, and averagedmodel.txt for the averaged perceptron. The format of the model files is up to you, but they should follow the following guidelines:

The model files should contain sufficient information for percepclassify.py to successfully label new data.
The model files should be human-readable, so that model parameters can be easily understood by visual inspection of the file.
The classification program will be invoked in the following way:

> python percepclassify.py /path/to/model /path/to/input

The first argument is the path to the model file (vanillamodel.txt or averagedmodel.txt), and the second argument is the path to the directory of the test data file; the program will read the parameters of a perceptron model from the model file, classify each entry in the test data, and write the results to a text file called percepoutput.txt in the following format:

label_a label_b path1
label_a label_b path2
⋮

In the above format, label_a is either “truthful” or “deceptive”, label_b is either “positive” or “negative”, and pathn is the path of the text file being classified.

Note that in the training data, it is trivial to infer the labels from the directory names in the path. However, directory names in the development and test data on Vocareum will be masked, so the labels cannot be inferred this way.
