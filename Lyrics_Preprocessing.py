import os
import re
import pandas as pd
import nltk
import contractions
from nltk.corpus import stopwords


# In[2]:

os.chdir('/Users/luislosada/Columbia Drive/Frameworks II/Group Assignment')
data = pd.read_csv('spotify_final.csv', encoding='latin-1')
lyrics = list(data['song_lyrics'])



# In[3]:


new_str = [re.sub(r'[\(\)]', '', str(x)) for x in lyrics] #remove paranthesis
lyrics = [new_str.lower() for new_str in new_str]


# In[4]:


def replace_contractions(songs):
    for i in range(len(songs)):
        songs[i] = contractions.fix(songs[i])
    return songs

lyrics = replace_contractions(lyrics) #removes contractions from lyrics


# In[5]:


new_str2=[re.sub(r'[^\x00-\x7f]','', str(x)) for x in lyrics] #remove nonascii chars
lyrics = [new_str1.lower() for new_str1 in new_str2]

new_str3=[re.sub(r'[^\w\s]','', str(x)) for x in lyrics] #remove punctuation
lyrics = [new_str11.lower() for new_str11 in new_str3]


# In[6]:


def tokenize(words):
    lst = []
    tokenlst = []
    for i in range(len(words)):
        lst = list(nltk.word_tokenize(words[i]))
        tokenlst.append(lst)
    return tokenlst

words = tokenize(lyrics) #words is list of tokenized lyrics


# In[7]:


def shortw(words):
    short = []
    for i in range(len(words)):
        lst = words [i]
        for j in range(len(lst)):
            if len(lst[j]) < 6:
                short.append(lst[j])
        short = list(dict.fromkeys(short)) # removing duplicates
    return short

short = shortw(words) #create a list of words whose length is less than 6


# In[8]:


def compare(lang1, lang2, lang3, stop): #we want a select number of stopwords
    lang1 = stopwords.words(lang1)
    lang2 = stopwords.words(lang2)
    lang3 = stopwords.words(lang3)
    comp = []
    for i in stop:
        for m in lang1:
            if m == i:
                comp.append(i)
        for k in lang2:
            if k == i:
                comp.append(i)
        for l in lang3:
            if l == i:
                comp.append(i)
    comp = list(dict.fromkeys(comp))  # removing duplicates
    return comp

comp_w = compare("english", "spanish", "french", short)


# In[9]:


def remove_stopwords(comp, w):
    """Remove stop words from list of tokenized words"""
    finalw=[]
    while w:
        stopw=[]
        for list_item in w:
            newt=[]
            for word in list_item:
                if word not in comp:
                    newt.append(word)
            stopw.append(newt)
        finalw.extend(stopw)
        return finalw

lyric_no_stopw=remove_stopwords(comp_w, words)


# In[12]:


df = pd.DataFrame(lyric_no_stopw)
df = df.transpose()


# In[13]:


df.to_csv('tokenized_lyrics.csv',index=False,header=True)


# In[16]:


#detokenize the lyrics
from nltk.tokenize.treebank import TreebankWordDetokenizer as Detok

def detokenize(lyric):
    detokenizer=Detok()
    detoken_list=[]
    while lyric:
        for list_item in lyric:
            text = detokenizer.detokenize(list_item)
            detoken_list.append(text)
        return detoken_list

detokenized_lyrics=detokenize(lyric_no_stopw)


# In[17]:


#turn list to dataframe
df2=pd.DataFrame(data = detokenized_lyrics , columns=['new_lyrics'])


# In[19]:


df2.to_csv('detokenized_lyrics.csv',index=False,header=True)