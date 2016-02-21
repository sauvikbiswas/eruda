# Concept of tokenizing
One way to tokenize a string is to pass it through a sequence of find-replace commands. These commands can be termed as substitution vectors. The operation is strictly unidirectional. A string passes through every element of the vector and breaks itself up into many fragments. An element of substitution vector may even join broken fragments together.

These fragments are separated by one or more blank spaces. This is by design. The idea is to pass the final string into a `string.split(' ')` and obtain a sequence of meaningful words. At this point, i.e. post splitting, no semantic, lexical or sentimental meaning is associated with any word. However, the formatted string would be good enough to be passed to some parser.

A simple period, '.', is usually the end of a sentence and hence must be a separate spaced entity. One way to achieve this is to use the following subsitution as the first (or one of the very first operation).
```
# '.' conditioning. Skips numbers (float representations)
\.([^0-9])
 . \1
```
Although it takes care of any float representation of numbers (or place separator if the number is repesented in European style), it fails to address the case of abbreviations. Since abbreviations are specific in nature, they are treated as a special class of substitution.

The `add_abbrev()` function reads a file and generates a sequence of substituton vectors. This assumes that a word like `Mr. Jones` has become `Mr . Jones` due to the aforementioned substitution. The substitution vectors generated would reverse that process. It also takes care of file extension. Thus, `filename.py`, which had become `filename . py` would see a reversal if the phrase `.py` is included in the abbreviation file.  
