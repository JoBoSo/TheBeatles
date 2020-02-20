from helpers.simple_tokenize import simple_tokenize
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#from pyspark import SparkContext, SparkConf
#sc = SparkContext(appName="MyApp", master="local[2]")
import nltk
from collections import Counter
from operator import itemgetter

   
class WordTools:
    '''
    Fields:
        self.tokens stores lyric tokens by album
        self.freqs stores the frequencies of tokens by album
    '''
    def __init__(self, database='The Beatles.db'):
        conn = sqlite3.connect(database) # connection
        c = conn.cursor() # iterable cursor
        
        # self.tokens stores lyric tokens in the form {album: [tokens]}
        tokens = dict()
        for row in c.execute('select Album, Lyrics from Master'):
            album = row[0]
            lyrics = row[1]
            songTokens = simple_tokenize(lyrics) # tokenize song lyrics
            if album in tokens:
                tokens[album] += songTokens
            else:
                tokens[album] = songTokens
        self.tokens = tokens
        
        # self.freqs stores the number of token appears in an each album
        #   sorted in descending frequency
        countBin = {}
        for album in self.tokens:
            tokens = self.tokens[album]
            '''
            # spark implementation - is too slow
            wordCount = sc.parallelize(tokens) \
                          .map(lambda token: (token, 1)) \
                          .reduceByKey(lambda x,y: x+y) \
                          .sortBy(lambda x: x[1], ascending=False) \
                          .collect()
            '''
            # Counter implementation
            wordCount = [(k, v) for k, v in dict(Counter(tokens)).items()]
            
            countBin[album] = sorted(wordCount, key=itemgetter(1), reverse=True)
        self.freqs = countBin
    
    # WordFreq(self, word) produces the number of times word appears in each
    #   album.
    # measure is one of: precent, count
    def WordFreq(self, word, measure='percent'):
        counts = {}
        for album in self.freqs:
            freqs = self.freqs[album]
            try:
                count = list(filter(lambda x: x[0] == word, freqs))[0][1]
            except IndexError:
                count = 0
            if measure == 'count':
                counts[album] = count
            else:
                ntokens = len(self.tokens[album])
                counts[album] = 100 * count / ntokens
        return counts
    
    # WordFreqGraph(self, word, color='blue') produces a bar chart of the
    #   frequency of word by albums, where bars are coloured color.
    def WordFreqGraph(self, word, color='blue'):
        # get data
        data = self.WordFreq(word, measure='percent')
        albums = list(data.keys())
        albums = ["Sgt. Pepper's" if x == "Sgt. Pepper's Lonely Hearts Club Band" \
                  else x for x in albums]
        counts = list(data.values())
        # plot
        index = np.arange(len(albums))
        plt.bar(index, counts, color=color)
        #plt.xlabel('Album', fontsize=10)
        #plt.ylabel('Frequency', fontsize=10)
        plt.xticks(index, albums, fontsize=10, rotation=66)
        plt.title('{} Frequency (%)'.format(word), fontsize=18)
        plt.tight_layout()
        plt.savefig('Word Count Graphs\{} Count Graph.png'.format(word), dpi=1200)
        plt.figure(dpi=1200, figsize=(40,40))
        plt.show()
    
    # WordDistribution(self, threshold) produces the frequency of word 
    #   appearences that have a frequency rank >= min_rank
    def WordDistribution(self, min_rank=10):
        topX = {}
        for album in self.freqs:
            freqs = self.freqs[album]
            topX[album] = freqs[:min_rank]
        return topX
    
    # SongsContaining(self, word) produces the names of songs and their 
    #   associated albums that contain word.
    def SongsContaining(self, word):
        pass
    
    # correlation(self, word1, word2) produces the correlation between
    #   word frequencies for word1 and word2 across albums.
    def correlation(self, word1, word2):
        pass
    
    # word_class is one of noun, verb, adjectives
    def WordClassGrid(self, word_class):
        # tags
        noun_tags = ['NN', 'NNS', 'NNP', 'NNPS']
        verb_tags = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
        adj_tags = ['JJ', 'JJR', 'JJS']
        
        # create matrix
        data = dict()
        for album in self.tokens:
            # tokens
            tokens = nltk.word_tokenize(' '.join(self.tokens[album]))
            # tagged tokens
            tagged = nltk.pos_tag(tokens)
            # keep(tagged_pairs, keeper_tags) produces a list of tokens in
            #   tagged_pairs that have tags in keeper_tags
            def keep(tagged_pairs, keeper_tags):
                exclude = ['i', "'s", 'oh', 'yeah', 'ta', "c'mon", 'is', 'do',
                           "'m", 'na', "'v", "'ve", 'ah', "'re", 'goo', 'doo',
                           'mm', 'ha', 'bom', 'la', 'bop', 'ho', 's', 'bompa']
                keepers = []
                for x in tagged_pairs:
                    token = x[0]
                    tag = x[1]
                    if tag in keeper_tags and token not in exclude:
                        keepers += [token]
                return keepers
            
            # get top three words in word_class and store in data
            if word_class == 'verbs':
                top_verbs = Counter(keep(tagged, verb_tags)).most_common(3)
                data[album] = top_verbs
            elif word_class == 'adjectives':
                top_adjs = Counter(keep(tagged, adj_tags)).most_common(3)
                data[album] = top_adjs
            elif word_class == 'nouns':
                top_nouns = Counter(keep(tagged, noun_tags)).most_common(3)
                data[album] = top_nouns
        grid = pd.DataFrame.from_dict(data).T
        grid.columns = ['First', 'Second', 'Third']
        grid.to_excel('Word Class Grids\{} Grid.xlsx'.format(word_class))
        return grid
    
    
x = WordTools()
count = x.WordDistribution()

freq = x.WordFreq('love')

print(x.WordClassGrid('nouns'))
print(x.WordClassGrid('verbs'))
print(x.WordClassGrid('adjectives'))

'''
love = x.WordFreqGraph('love', color='red')
heart = x.WordFreqGraph('heart', color='pink')
girl = x.WordFreqGraph('girl', color='fuchsia')

need = x.WordFreqGraph('need', color='purple')
want = x.WordFreqGraph('want', color='purple')
got = x.WordFreqGraph('got', color='purple')

good = x.WordFreqGraph('good', color='yellow')
better = x.WordFreqGraph('better', color='orange')
man = x.WordFreqGraph('man', color='blue')
people = x.WordFreqGraph('people', color='blue')
time = x.WordFreqGraph('time', color='orange')
now = x.WordFreqGraph('now', color='blue')

think = x.WordFreqGraph('think', color='navy')
feel = x.WordFreqGraph('feel', color='navy')
know = x.WordFreqGraph('know', color='navy')

make = x.WordFreqGraph('make', color='chocolate')
have = x.WordFreqGraph('have', color='chocolate')
take = x.WordFreqGraph('take', color='chocolate')
'''