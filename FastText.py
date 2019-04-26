import os
os.chdir('/Users/luislosada/Columbia Drive/Frameworks II/Group Assignment')
import fasttext
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import collections
import pandas as pd
from numpy import random

#Model Creation

lyrics = open("cleanlyrics.txt").read()
model = fasttext.skipgram("cleanlyrics.txt",'model',lr=0.1, dim=300)
#model.words #visualizing your creation

#Selecting top N words
def top_words(txt,n,mwords):
    def top(txt, n):
        count = collections.Counter(txt.split())
        df = pd.DataFrame(count.most_common(n))
        df.columns = ['words', 'count']
        ls = list(df['words'])
        return ls
    ls = top(txt,n)
    top_n = []
    for i in ls:
        if i in mwords:
            top_n.append(i)
    return top_n

top_500 = top_words(lyrics,500,model.words) #In this case we choose the top 500 words to create the visualization but
all_words = top_words(lyrics,len(model.words),model.words) # for our final output we need the entire set of clean words. Changing the value of N will fix that.

#Vector Creation
def wordvec(words):
    tokens = []
    for word in words:
        tokens.append(model[word])
    return tokens

wordvec = wordvec(all_words)

# Label Creation
def label(words):
    labels = []
    for word in words:
        labels.append(word)
    return labels

label_500 = label(top_500)

# Dimension Reduction using TSNE

random.seed(100)
tsne_model = TSNE(perplexity=100, n_components=2, init='pca',metric='cosine', n_iter=5000, random_state=23)
new_values = tsne_model.fit_transform(wordvec)

#Plotting

def plotvec(tsne_value,labels):
    x = []
    y = []
    for value in tsne_value:
        x.append(value[0])
        y.append(value[1])

    plt.figure(figsize=(16, 16))
    for i in range(len(x)):
        plt.scatter(x[i], y[i])
        try:
            plt.annotate(labels[i],
                         xy=(x[i], y[i]),
                         xytext=(5, 2),
                         textcoords='offset points',
                         ha='right',
                         va='bottom')
        except IndexError:
            plt.annotate(" ",
                         xy=(x[i], y[i]),
                         xytext=(5, 2),
                         textcoords='offset points',
                         ha='right',
                         va='bottom')

    plt.show()

plotvec(new_values,label_500)

#Saving our word vector.

vector_of_words = pd.DataFrame(new_values)
label_for_vector = label(all_words)
vector_of_words['labels'] = label_for_vector
vector_of_words.to_csv(r'/Users/luislosada/Columbia Drive/Frameworks II/Group Assignment/vector_of_words.csv', index=True)
#Reference link: https://www.kaggle.com/jeffd23/visualizing-word-vectors-with-t-sne

