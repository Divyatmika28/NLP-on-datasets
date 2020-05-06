A set of training and test data is available. The uncompressed archive contains the following files:

Three corpus files in universal dependencies format, with the file names indicating whether the file is for development, training, or testing (only the training and testing files will be used in the exercise).
Additional readme and license files, which will not be used for the exercise.
The submission script will learn the model from the training data, test it on the test data, output the results, and compare them to the known solution. The grading script will do the same, but on training and test data from a different language.

Program
You will write a program which will take the paths to the training and test data files as command-line arguments.

If using Python 2, name your program lookup-lemmatizer.py
If using Python 3, name your program lookup-lemmatizer3.py
Your program will be invoked in the following way:

> python lookup-lemmatizer.py /path/to/train/data /path/to/test/data

The program will read the training data, learn a lookup table, run the lemmatizer on the test data, and write its report to a file called lookup-output.txt. The report has a fixed format of 22 lines which looks as follows:

Training statistics
Wordform types: 16879
Wordform tokens: 281057
Unambiguous types: 16465
Unambiguous tokens: 196204
Ambiguous types: 414
Ambiguous tokens: 84853
Ambiguous most common tokens: 75667
Identity tokens: 201485
Expected lookup accuracy: 0.967316238343
Expected identity accuracy: 0.716883052192
Test results
Total test items: 35430
Found in lookup table: 33849
Lookup match: 32596
Lookup mismatch: 1253
Not found in lookup table: 1581
Identity match: 1227
Identity mismatch: 354
Lookup accuracy: 0.962982658276
Identity accuracy: 0.776091081594
Overall accuracy: 0.954642957945

The numbers above are the correct output when running the program on the supplied data (the submission script). The numbers will be different when the program is run on the data used by the grading script.
