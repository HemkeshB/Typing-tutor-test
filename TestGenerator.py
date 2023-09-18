import json
import random
import sqlite3

def newTest(count):
    text = ""
    f = open('E:\pycharmProj\pythonWords\words\common.json')
    data = json.load(f)
    while(count>1):
        text += random.choice(list(data.items())[1][1]) + " "
        count-=1
    text += random.choice(list(data.items())[1][1])
    return text
def get_alphabetical_chars(text):
    return ''.join(filter(str.isalpha, text))

def newTestSQL(count):
    text = ""
    connector = sqlite3.connect("wordBank.db")
    cursor = connector.cursor()
    while(count>1):
        cursor.execute("select word from wordStats ORDER BY RANDOM() LIMIT 1")
        text += get_alphabetical_chars(cursor.fetchall()[0]) + " "
        count -= 1
    cursor.execute("select word from wordStats ORDER BY RANDOM() LIMIT 1")
    text += get_alphabetical_chars(cursor.fetchall()[0])
    return text

def newTestSQLUser(count, userID):
    text = ""
    connector = sqlite3.connect("testUsers.db")
    cursor = connector.cursor()
    cursor.execute("SELECT * FROM letterStats WHERE userid = ? ORDER BY letterHistory LIMIT 5", userID)
    topRows = cursor.fetchall()
    if topRows.__len__() >= 4:
        connector = sqlite3.connect("wordBank.db")
        cursor = connector.cursor()
        i=0
        while (count>1):
            execute = f"select word from wordStats ORDER BY  {topRows[i][0]}  DESC "
            cursor.execute(execute)
            words = cursor.fetchall()
            insert = get_alphabetical_chars(words[0])
            b = 0
            while insert in text:
                b += 1
                insert = get_alphabetical_chars(words[b])
            text += insert + " "

            count -= 1
            if i < 4:
                i += 1
            else:
                i = 0
        execute = f"select word from wordStats ORDER BY  {topRows[i][0]}  DESC "
        cursor.execute(execute)
        words = cursor.fetchall()
        insert = get_alphabetical_chars(words[0])
        b = 0
        while insert in text:
            b += 1
            insert = get_alphabetical_chars(words[b])
        text += insert

        words = text.split()
        random.shuffle(words)
        text = ' '.join(words)
    else:
        text = newTestSQL(count)
    return text
