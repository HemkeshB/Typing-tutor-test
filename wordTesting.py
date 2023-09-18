import string
import sqlite3
import json



def count_letters(word):
    """Counts and returns how many of each letter are in the word"""
    letter_count = {letter: 0 for letter in string.ascii_lowercase}
    for letter in word:
        if letter.isalpha():
            letter_count[letter.lower()] += 1
    return letter_count



connector = sqlite3.connect("wordBank.db")
cursor = connector.cursor()
"""This is initial construction of the wordBank database"""
cursor.execute('''
            CREATE TABLE IF NOT EXISTS wordStats(
                id INTEGER PRIMARY KEY,
                word TEXT NOT NULL
            )
        ''')
  for char in string.ascii_lowercase:
         cursor.execute(f'ALTER TABLE wordStats ADD COLUMN {char} INTEGER DEFAULT 0')
def storeWord():
    """Reads words from a json file then inserts all the words in to a sqlite Database"""
    f = open('E:\pycharmProj\pythonWords\words\common.json')
    data = json.load(f)
    print(list(data.items())[1][1])
    for word in list(data.items())[1][1]:
        count = count_letters(word)
        submission = (word, list(count.values())[0],
              list(count.values())[1], list(count.values())[2], list(count.values())[3],
              list(count.values())[4], list(count.values())[5], list(count.values())[6],
              list(count.values())[7], list(count.values())[8], list(count.values())[9],
              list(count.values())[10], list(count.values())[11], list(count.values())[12],
              list(count.values())[13], list(count.values())[14], list(count.values())[15],
              list(count.values())[16], list(count.values())[17], list(count.values())[18],
              list(count.values())[19], list(count.values())[20], list(count.values())[21],
              list(count.values())[22], list(count.values())[23], list(count.values())[24],
              list(count.values())[25])
        print(submission)
        cursor.execute("""INSERT INTO wordStats VALUES
                               (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                       (submission))
        connector.commit()

storeWord()