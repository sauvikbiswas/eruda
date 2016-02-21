# Concept of tokenizing
One way to tokenize a string is to pass it through a sequence of find-replace commands. These commands can be termed as substitution vectors. The operation is strictly unidirectional. A string passes through every element of the vector and breaks itself up into many fragments. An element of substitution vector may even join broken fragments together.

These fragments are separated by one or more blank spaces. This is by design. The idea is to pass the final string into a `string.split(' ')` and obtain a sequence of meaningful words. At this point no semantic, lexical or sentimental meaning is associated with any word.
