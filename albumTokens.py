from helpers.simple_tokenize import simple_tokenize
import sqlite3

db = 'The Beatles.db' # database
conn = sqlite3.connect(db) # connection
c = conn.cursor() # iterable cursor

# albumTokens tokenizes song lyrics and stores the tokens in a dictionary of the form {album: [tokens]}
albumTokens = dict()
for row in c.execute('select Album, Lyrics from Master'):
    album = row[0]
    lyrics = row[1]
    songTokens = simple_tokenize(lyrics) # tokenize song lyrics
    
    if album in albumTokens:
        albumTokens[album] += songTokens
    else:
        albumTokens[album] = songTokens