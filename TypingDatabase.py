import sqlite3
import string

connector = sqlite3.connect("testUsers.db")
cursor = connector.cursor()


def initialconstruction():
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                name TEXT, 
                dateCreated DATE,
                timeUsedMinutes FLOAT, 
                id INTEGER PRIMARY KEY)
                """)

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS typingStats(
                date INTEGER,
                numOfCharacters INTEGER, 
                averageWPM FLOAT, 
                userid INTEGER, 
                id INTEGER PRIMARY KEY, 
                CONSTRAINT users FOREIGN KEY (userid)
                REFERENCES users(id)
                ON DELETE CASCADE)
                    """)

    cursor.execute("""
            CREATE TABle IF NOT EXISTS letterStats(
            letter TEXT,
            letterCount INTEGER,
            letterHistory FLOAT,
            id INTEGER PRIMARY KEY,
            userid INTEGER,
            CONSTRAINT users FOREIGN KEY (userid)
            REFERENCES users(id)
            ON DELETE CASCADE)
            """)

initialconstruction()
