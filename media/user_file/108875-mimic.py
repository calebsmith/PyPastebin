#!/usr/bin/env python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

"""Mimic pyquick exercise -- optional extra exercise.
Google's Python Class

Read in the file specified on the command line.
Do a simple split() on whitespace to obtain all the words in the file.
Rather than read the file line by line, it's easier to read
it into one giant string and split it once.

Build a "mimic" dict that maps each word that appears in the file
to a list of all the words that immediately follow that word in the file.
The list of words can be be in any order and should include
duplicates. So for example the key "and" might have the list
["then", "best", "then", "after", ...] listing
all the words which came after "and" in the text.
We'll say that the empty string is what comes before
the first word in the file.

With the mimic dict, it's fairly easy to emit random
text that mimics the original. Print a word, then look
up what words might come next and pick one at random as
the next work.
Use the empty string as the first word to prime things.
If we ever get stuck with a word that is not in the dict,
go back to the empty string to keep things moving.

Note: the standard python module 'random' includes a
random.choice(list) method which picks a random element
from a non-empty list.

For fun, feed your program to itself as input.

"""

import random
import sys

def mimic_file(filename, word):
    mdict, wordcount = mimic_dict(sys.argv[1])
    output = print_mimic(mdict, word, wordcount)
    return output
    
def mimic_dict(filename):
    """Returns mimic dict mapping each word to list of words which follow it."""
    
    #Read text from file into a string called text.
    #make a list called words with an empty string, followed by the text
    f = open(filename, "rU")
    text = f.read()
    words = ['']    
    words.extend(text.split())
    
    #make a two tuple of each word and the following word, then pack into a
    #dictionary
    dword = {}
    for iter, word in enumerate(words):
        if iter + 1 < len(words):
            wordpair = (word, words[iter + 1])  
            #use the two tuple to fill the dictionary          
            if wordpair[0] in dword:
                dword[word] += ", " + wordpair[1]  
            else:                          
                dword[word] = wordpair[1]
    
    #turn , seperated values in the dictionary into lists
    for k, v in dword.items():
        v = v.split(", ")
        dword[k] = v    
        
    #return the dictionary with format {key : [values],...}
    return dword, len(words)

def print_mimic(mimic_dict, word, wordcount):
    """Given mimic dict and start word, prints 200 random words."""
    
 
    kchoice = list(mimic_dict.viewkeys())
    begin = random.choice(kchoice)    
   
    if word: begin = word
    output = begin
    
    word_count = 0
    chars = 0
    while word_count < wordcount:
        v = mimic_dict.get(begin)
        try:
            vchoice = random.choice(v)
            begin = vchoice
            output += " " + vchoice
            chars += len(vchoice)            
            word_count += 1
            
        except:
            begin = random.choice(kchoice)
            
        if chars > 70:
            output += '\n'
            chars = 0
            
    return output

# main
def main():
    if len(sys.argv) != 2:
        print 'usage: ./mimic.py file-to-read'
        sys.exit(1)
        
    output = mimic_file(sys.argv[1], '')
    print output


if __name__ == '__main__':
    main()
