import string
from collections import Counter
from operator import itemgetter

# NOTES:
# make song one long string, no changes in formatting, so we can append these 
# on an ablum basis and search them. Then, we can create flattened versions.

class Lyrics:
    '''
    Fields:
     - self.lyrics stores lyrics as a string
    '''
    # Lyrics(lyrics) initiates a new Lyrics object
    # Tuple --> Lyrics
    def __init__(self, lyrics):
        self.lyrics = lyrics
        
    
    # str(self) produces self as a string
    def __str__(self):
        return self.lyrics
        
    
    # self.get(attribute) produces a list contatining all instances of attribute
    # Lyric Str --> (listof Str)
    def get(self, attribute):
        '''
        character attributes:
         - chars: contains all characters, including newlines and spaces
         - chars_lower: contains all characters, which have been made lowercase
         - chars_exnewlines: contains all characters, excluding newlines
         - chars_exwhitespace: contains all characters, excluding whitespace
         - letters: contains all letters
         - letters_lower: contains all letters, which have been made lowercase
         - numbers: contains all numbers
         - alpha_numeric: contains all letters and numbers
         - punctuation: contains all punctuation marks
        word attributes:
         - words: contains all words (and nums); keeps hyphens and apostrophes
         - words_lower: contains words, which have been made lowercase
         - words_nopunct: contains all words (and nums) without punctuation
        line attributes:
         - lines_all: contains all lines, including empty lines
         - lines_full: contains all non-empty lines
        '''
        # chars
        if attribute is 'chars':
            return list(self.lyrics)
        
        # chars_lower
        if attribute is 'chars_lower':
            return list(map(lambda s: s.lower(), list(self.lyrics)))
        
        # chars_exnewlines
        elif attribute is 'chars_exnewlines':
            return list(filter(lambda char: char is not '\n', list(self.lyrics)))
        
        # chars_exwhitespace
        elif attribute is 'chars_exwhitespace':
            return list(filter(lambda char: char not in string.whitespace, list(self.lyrics)))
        
        # letters
        elif attribute is 'letters':
            return list(filter(lambda char: char.isalpha(), list(self.lyrics)))
        
        # letters_lower
        elif attribute is 'letters_lower':
            return list(map(lambda s: s.lower(), self.get('letters')))
        
        # numbers
        elif attribute is 'numbers':
            return list(filter(lambda char: char.isnumeric(), list(self.lyrics)))
        
        # alpha_numeric
        elif attribute is 'alpha_numeric':
            return list(filter(lambda char: char.isalnum(), list(self.lyrics)))
        
        # punctuation
        elif attribute is 'punctuation':
            return list(filter(lambda char: char in string.punctuation, list(self.lyrics)))
        
        # words
        elif attribute is 'words':
            irr_punct = string.punctuation.replace("'",'').replace('-','')
            translation = lambda word: word.translate(str.maketrans('','',irr_punct))
            return list(map(translation, self.lyrics.split()))  
        
        # words_lower
        elif attribute is 'words_lower':
            words = list(map(lambda s: s.lower(), self.get('words')))
            return words
        
        # words_nopunct
        elif attribute is 'words_nopunct':
            translation = lambda word: word.translate(str.maketrans('','',string.punctuation))
            return list(map(translation, self.lyrics.split())) 
        
        # lines_all
        elif attribute is 'lines_all':
            return self.lyrics.splitlines()
        
        # lines_full
        elif attribute is 'lines_full':
            return list(filter(lambda line: len(line) > 0, self.lyrics.splitlines()))
    
    
    # self.count(attribute) produces the number of times attribute appears in
    #    self.
    # Lyrics Str --> Int
    def count(self, attribute):
        '''         
        character attributes:
         - chars: counts all characters, including newlines and spaces
         - chars_exnewlines: count all characters, excluding newlines
         - chars_exwhitespace: counts all characters, excluding whitespace
         - letters: counts all letters
         - numbers: counts all numbers
         - alpha_numeric: counts all letters and numbers
         - punctuation: counts all punctuation marks
         - vowels: counts vowels
        sentence attributes:
         - questions: counts all question marks
         - exclamations: counts all exclamation marks
         - periods: counts all periods
         - sentences: counts sentences
        word attributes:
         - words: counts all words (and nums)
         - words_alpha: counts all alphabetic words
         - words_numeric: counts all numbers
        line attributes:
         - lines_all: counts all lines, including empty lines
         - lines_full: counts non-empty lines
         - line_blocks: counts line blocks, represented by empty lines +1
        '''
        # chars
        if attribute is 'chars':
            return len(self.get('chars'))
        
        # chars_exnewlines
        elif attribute is 'chars_exnewlines':
            return len(self.get('chars_exnewlines'))        
        
        # chars_exwhitespace
        elif attribute is 'chars_exwhitespace':
            return len(self.get('chars_exwhitespace'))        
        
        # letters
        elif attribute is 'letters':
            return len(self.get('letters'))        
        
        # numbers
        elif attribute is 'numbers':
            return len(self.get('numbers'))        
        
        # alpha_numeric
        elif attribute is 'alpha_numeric':
            return len(self.get('alpha_numeric'))        
        
        # punctuation
        elif attribute is 'punctuation':
            return len(self.get('punctuation')) 
        
        # vowels
        elif attribute is 'vowels':
            vowels = ['a','e','i','o','u']
            return len(list(filter(lambda word: word in vowels, self.get('chars_lower'))))
        
        # questions
        elif attribute is 'questions':
            return self.lyrics.count('?')    
        
        # exclamations
        elif attribute is 'exclamations':
            return self.lyrics.count('!')         
        
        # periods    
        elif attribute is 'periods':
            return self.lyrics.count('.') 
        
        # sentences
        elif attribute is 'sentences':
            return self.lyrics.count('?')\
                   + self.lyrics.count('!')\
                   + self.lyrics.count('.')
        
        # words
        elif attribute is 'words':
            return len(self.get('words_nopunct'))
        
        # words_alpha
        elif attribute is 'words_alpha':
            return len(list(filter(lambda word: word.isalpha(), self.get('words_nopunct'))))  
        
        # words_numeric
        elif attribute is 'words_numeric':
            return len(list(filter(lambda word: word.isnumeric(), self.get('words_nopunct'))))         
        
        # lines_all
        elif attribute is 'lines_all':
            return len(self.get('lines_all'))        
        
        # lines_full
        elif attribute is 'lines_full':
            return len(self.get('lines_full'))        
        
        # line_blocks
        elif attribute is 'line_blocks':
            return len(list(filter(lambda line: line is '', self.get('lines_all'))))+1        
    
    
    def mean(self, attribute):
        '''
        attributes
         - chars_per_word: mean alpha-numeric characters per word
         - words_per_line: mean words per non-empty line
         - words_per_sentence: mean words per sentence
         - lines_per_block: mean lines per line block
        '''
        try: 
            # chars_per_word
            if attribute is 'chars_per_word':
                return round(self.count('alpha_numeric') / self.count('words'),2)
            
            # words_per_line
            elif attribute is 'words_per_line':
                return round(self.count('words') / self.count('lines_full'),2)
            
            # words_per_sentence
            elif attribute is 'words_per_sentence':
                return round(self.count('words') / self.count('sentences'),2)
            
            # lines_per_block
            elif attribute is 'lines_per_block':
                return round(self.count('lines_full') / self.count('line_blocks'),2)
        except ZeroDivisionError:
            return
    
    
    # self.proportion(attribute) produces the proportion of lyrics that is 
    #    attribute.
    def proportion(self, attribute):
        '''
        sentence attributes:
         - questions: proportion of sentences marked by a question mark
         - exclamations: proportion of sentences marked by an exclamation mark
         - periods: proportion of sentences marked by a period
        character attributes:
         - numeric: proportion of non-whitespace characters that are numeric
         - alphabetic: proportion of non-whitespace characters that are alphabetic
         - punctuation: proportion of non-whitespace characters that are punctuation marks
         
        # or, we could just make attribute any string - create lookup_proportion(self, type[char,word], value). 
        '''
        try:
            # questions
            if attribute is 'questions':
                return round(self.count('questions') / self.count('sentences'), 4)
            
            # exclamations
            elif attribute is 'exclamations':
                return round(self.count('exclamations') / self.count('sentences'), 4)
            
            # periods
            elif attribute is 'periods':
                return round(self.count('periods') / self.count('sentences'), 4)      
            
            # numeric
            elif attribute is 'numeric':
                return round(self.count('numbers') / self.count('chars_exwhitespace'), 4)        
            
            # alphabetic
            elif attribute is 'alphabetic':
                return round(self.count('letters') / self.count('chars_exwhitespace'), 4)         
            
            # punctuation
            elif attribute is 'punctuation':
                return round(self.count('punctuation') / self.count('chars_exwhitespace'), 4) 
        
        except ZeroDivisionError:
            return        
    
    
    # use map reduce
    def frequency(self, attribute):
        '''
        attributes
         - words
         - chars
         - letters
         - numbers
         - punctuation
        '''
        # string_counter(items) converts a Counter to a string of the form:
        #    "[val1, count1]\n[val2, count2]\n...[valn, countn]"
        # (listof Any) --> Str
        def string_counter(items):
            counter = Counter(items)
            dictionary = dict(counter)
            lis = []
            for key in dictionary:
                lis += [[key, dictionary[key]]]
            lis = list(reversed(sorted(lis, key=itemgetter(1))))
            string = list(map(str, lis))
            string = '\n'.join(str(item) for item in lis)
            #tup = (string, )
            return string     
        
        # words
        if attribute is 'words':
            return string_counter(self.get('words_lower'))
        
        # chars
        elif attribute is 'chars':
            return string_counter(self.get('chars_lower'))
        
        # letters
        elif attribute is 'letters':
            return string_counter(self.get('letters_lower'))       
        
        # numbers
        elif attribute is 'numbers':
            return string_counter(self.get('numbers'))       
        
        # punctuation
        elif attribute is 'punctuation':
            return string_counter(self.get('punctuation'))     
        
    
    
    # produces a list of lines containing keyword
    def line_search(self, keyword):
        # need to create self.get('lines_lower') and use here
        lines = self.lyrics.splitlines()
        key_lines = []
        for line in lines:
            if keyword in line:
                key_lines += [line]
        return key_lines
    
    
    def summary(self):
        summary = {
            # self.get
            'List Characters' : self.get('chars'),
            'List Characters in lowercase' : self.get('chars_lower'),
            'List Characters ex. newlines' : self.get('chars_exnewlines'),
            'List Characters ex. whitespace' : self.get('chars_exwhitespace'),
            'List Letters' : self.get('letters'),
            'List letters in lowercase' : self.get('letters_lower'),
            'List Numbers' : self.get('numbers'),
            'List Alpha-numeric characters' : self.get('alpha_numeric'),
            'List Punctuation marks' : self.get('punctuation'),
            'List Words' : self.get('words'),
            'List words in lowercase' : self.get('words_lower'),
            'List Words ex. punctuation' : self.get('words_nopunct'),
            'List Lines' : self.get('lines_all'),
            'List Non-empty lines' : self.get('lines_full'),
                
            # self.count
            'Count Characters' : self.count('chars'),
            'Count Characters ex. newlines' : self.count('chars_exnewlines'),
            'Count Characters ex. whitespace' : self.count('chars_exwhitespace'),
            'Count Letters' : self.count('letters'),
            'Count Numbers' : self.count('numbers'),
            'Count Alpha-numeric characters' : self.count('alpha_numeric'),
            'Count Punctuation marks' : self.count('punctuation'),
            'Count vowels' : self.count('vowels'),
            'Count "?"' : self.count('questions'),
            'Count "!"' : self.count('exclamations'),
            'Count "."' : self.count('periods'),
            'Count sentences' : self.count('sentences'),
            'Count words' : self.count('words'),
            'Count alphabetic words' : self.count('words_alpha'),
            'Count numeric words' : self.count('words_numeric'),
            'Count lines' : self.count('lines_all'),
            'Count non-empty lines' : self.count('lines_full'),
            'Count line blocks' : self.count('line_blocks'),
            
            # self.mean
            'Mean characters per word' : self.mean('chars_per_word'),
            'Mean words per line' : self.mean('words_per_line'),
            'Mean words per sentence' : self.mean('words_per_sentence'),
            'Mean lines per block' : self.mean('lines_per_block'),
            
            # self.proportion
            'Proportion of questions' : self.proportion('questions'),
            'Proportion of exclamations' : self.proportion('exclamations'),
            'Proportion of periods' : self.proportion('periods'),
            'Proportion of numeric characters' : self.proportion('numeric'),
            'Proportion of alphabetic characters' : self.proportion('alphabetic'),
            'Proportion of punction characters' : self.proportion('punctuation'),
            
            # self.frequency
            'Word frequencies' : self.frequency('words'),
            'Character frequencies' : self.frequency('chars'),
            'Letter frequencies' : self.frequency('letters'),
            'Number frequencies' : self.frequency('numbers'),
            'Punctuation frequencies' : self.frequency('punctuation')
        }
        
        for key in summary:
            print(key+':', summary[key])
            
        return summary
    
     
    def count_summary(self):
        summary = {                
            'Words' : self.count('words'),
            'Characters (with spaces)' : self.count('chars_exnewlines'),
            'Characters (no spaces)' : self.count('chars_exwhitespace'),
            'Letters' : self.count('letters'),
            'Numbers' : self.count('numbers'),
            'Vowels' : self.count('vowels'),
            'Punctuation Marks' : self.count('punctuation'),
            'Question Marks' : self.count('questions'),
            'Exclamation Marks' : self.count('exclamations'),
            'Periods' : self.count('periods'),
            'Sentences' : self.count('sentences'),
            'Lines (including empty)' : self.count('lines_all'),
            'Lines (non-empty)' : self.count('lines_full'),
            'Line Blocks' : self.count('line_blocks')
        }
        '''
        for key in summary:
            print(key+':', summary[key])
        '''
        #keys = tuple(summary.keys())
        #print(keys)
        vals = tuple(summary.values())
        return vals
    
    
    def mean_summary(self):
        summary = {                
            'Characters/Word' : self.mean('chars_per_word'),
            'Words/Line' : self.mean('words_per_line'),
            'Words/Sentence' : self.mean('words_per_sentence'),
            'Lines/Block' : self.mean('lines_per_block')
        }
        '''
        for key in summary:
            print(key+':', summary[key])
        '''
        vals = tuple(summary.values())
        return vals  
    
    
    def proportion_summary(self):
        summary = {                
            'Questions' : self.proportion('questions'),
            'Exclamations' : self.proportion('exclamations'),
            'Periods' : self.proportion('periods'),
            'Numeric Characters' : self.proportion('numeric'),
            'Alphabetic Characters' : self.proportion('alphabetic'),
            'Punctuation Marks' : self.proportion('punctuation')
        }
        '''
        for key in summary:
            print(key+':', summary[key])
        '''    
        vals = tuple(summary.values())
        return vals 
    
    
    def freq_summary(self):
        summary = {                
            'Words' : self.frequency('words'),
            'Characters' : self.frequency('chars'),
            'Letters' : self.frequency('letters'),
            'Numbers' : self.frequency('numbers'),
            'Punctuation' : self.frequency('punctuation')
        }
        '''
        for key in summary:
            print(key+':', summary[key])
        '''    
        vals = tuple(summary.values())
        return vals    
    
    
# example Lyrics object
x = '(Rosetta.\nWho are you talking about?\nSweet Loretta Fart. She thought she was a cleaner\nSweet Rosetta Martin\nBut she was a frying pan, yeah\nRosetta\nThe picker! The picker! Picture the fingers burning!\nOo-wee!\nOK?\n1, 2, 1, 2, 3, 4)\n\nJo Jo was a man who thought he was a loner\nBut he knew it couldn\'t last\nJo Jo left his home in Tucson, Arizona\nFor some California grass\n\nGet back, get back\nGet back to where you once belonged\nGet back, get back\nGet back to where you once belonged\nGet back Jo Jo\nGo home\n\nGet back, get back\nGet back to where you once belonged\nGet back, get back\nBack to where you once belonged\nGet back, Jo\n\nSweet Loretta Martin thought she was a woman\nBut she was another man\nAll the girls around her say she\'s got it coming\nBut she gets it while she can\n\nOh, get back, get back\nGet back to where you once belonged\nGet back, get back\nGet back to where you once belonged\nGet back, Loretta\n\nGo home\nOh, get back, get back\nGet back to where you once belonged\nGet back, get back\nGet back to where you once belonged\n\nGet back\nWoo...\n\n(Thanks, Mo!\nI\'d like to say "thank you" on behalf of the group\nAnd ourselves and I hope we passed the audition!)'

l = Lyrics(x)
summary = l.summary()