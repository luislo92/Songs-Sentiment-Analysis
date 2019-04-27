import os
import re
import pandas as pd

os.chdir('/Users/luislosada/Columbia Drive/Frameworks II/Group Assignment')

string = open("all_lyrics.txt").read()
new_str = re.sub(r'[\(\)]', '', str(string)) #remove punctuation
lyrics = new_str.lower()

##Python script to prepare the song lyrics for the fasttext modelling. It includes word tokenization and normalization.

## Tokenizing and Normalzing Lyrics

import unicodedata
import nltk
import contractions
import inflect
from nltk.corpus import stopwords
import collections
import pprint as pp

# Text Visualization

def top_words(txt,n):
    count = collections.Counter(txt.split())
    df = pd.DataFrame(count.most_common(n))
    df.columns = ['words','count']
    return df

pp.pprint(top_words(lyrics,20)) #mostly stop words lets fix this.

#Contractions gone
def replace_contractions(txt):
    return contractions.fix(txt)

lyrics = replace_contractions(lyrics)
#print(lyrics)

#Tokenization

words = nltk.word_tokenize(lyrics)

#Creating stopwords list

def shortw (txt):
    short = []
    for i in range(len(txt)):
        if len(txt[i]) < 6:
            short.append(txt[i])
    short = list(dict.fromkeys(short)) #removing duplicates
    return short

final_short_words = shortw(words) #we do not want to eliminate all stopwords on the stopwords dictionary just because
#we are using a 2 window vector approach, so the meaning of a word might change significantly if important words are removed
#What we did then was eliminate only shorter words (<6 letters).

#pp.pprint(final_short_words)

def compare(lang1,lang2,lang3,lst):
    comp = []
    lang1 = stopwords.words(lang1)
    lang2 = stopwords.words(lang2)
    lang3 = stopwords.words(lang3)
    for i in lst:
        for j in lang1:
            if j == i:
                comp.append(i)
        for k in lang2:
            if k == i:
                comp.append(i)
        for l in lang3:
            if l == i:
                comp.append(i)
    return comp

#stopw = stopwords.words('spanish')

comparison = compare('english','spanish','french',final_short_words) #we picked these languages because they are the most commont within our dataset

#Normalization

def remove_non_ascii(words):
    """Remove non-ASCII characters from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore') #remove strange words and words in languages that use a NON-ASCII format.
        new_words.append(new_word)
    return new_words

def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words

def replace_numbers(words):
    """Replace all integer occurrences in list of tokenized words with textual representation"""
    p = inflect.engine()
    new_words = []
    for word in words:
        if word.isdigit():
            new_word = p.number_to_words(word)
            new_words.append(new_word)
        else:
            new_words.append(word)
    return new_words

def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in words:
        if word not in comparison:
            new_words.append(word)
    for w in new_words:
        if len(w) == 1:
            new_words.remove(w)
    return new_words


def normalize(words):
    words = remove_non_ascii(words)
    words = remove_punctuation(words)
    words = replace_numbers(words)
    words = remove_stopwords(words)
    return words

words = normalize(words)

#Saving
T_lyrics = ' '.join(words)
open('cleanlyrics.txt', 'w').write(T_lyrics) #cleanlyrics file ready to train the model.
#pp.pprint(top_words(T_lyrics,20))

