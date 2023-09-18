import sqlite3
import sys
import time
from datetime import date

import keyboard

import TestGenerator

avgWordLength = 5.0


def all_rows_print(table):
    connector = sqlite3.connect("testUsers.db")
    cursor = connector.cursor()

    print("current " + table + " :")
    print()
    cursor.execute(f"PRAGMA table_info({table})")
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]
    print(column_names)
    users = all_rows(table)
    for users in users:
        print(users)
    print()


def all_rows(table):
    connector = sqlite3.connect("testUsers.db")
    cursor = connector.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    users = cursor.fetchall()
    return users


def user_log():
    connector = sqlite3.connect("testUsers.db")
    cursor = connector.cursor()
    allUsers = all_rows('users')
    if allUsers.__len__() > 0:
        all_rows_print('users')
        print("Existing users press y and new user press n")
        while True:
            if (keyboard.is_pressed('n')):
                keyboard.press('backspace')
                userName = input("Enter your new username: ")
                today = date.today()
                cursor.execute("""INSERT INTO users VALUES(?,?,?,NULL)""", (userName, today, 0))
                print("press y to confirm your entry, or press n to exit")
                while True:
                    if keyboard.is_pressed('y') or keyboard.is_pressed('tab'):
                        connector.commit()
                        keyboard.press('backspace')
                        cursor.execute("SELECT * FROM users WHERE ROWID = LAST_INSERT_ROWID()")
                        user = cursor.fetchone()
                        print(user)
                        userID = user[3]
                        return userID
                    if keyboard.is_pressed('n') or keyboard.is_pressed('esc'):
                        print()
                        keyboard.press('backspace')
                        print("user creation canceled")
                        break
                break
            if keyboard.is_pressed('y'):
                keyboard.press('backspace')
                print("")
                userID = input("Enter your user ID (last number in the row): ")
                cursor.execute("SELECT * FROM users WHERE ROWID = ?", userID)
                user = cursor.fetchone()
                if user:
                    print("User found: ")
                    print(user)
                    return userID
                else:
                    print()
                    print("User with the specified id not found.")
                    print()
                print("Thank you for using this typing test")
                break
            if keyboard.is_pressed('esc'):
                print()
                print("action canceled")
                break
        connector.close()
    else:
        print("Welcome!")
        print()
        print("Press n to sign up or esc to quit")
        while True:
            if keyboard.is_pressed('n'):
                keyboard.press('backspace')
                time.sleep(0.02) #I dont know why the backspace thing doesnt work all the time
                keyboard.press('backspace')
                print()
                userName = input("Enter your name: ")
                today = date.today()
                cursor.execute("""INSERT INTO users VALUES(?,?,?,NULL)""", (userName, today, 0))
                print("press y to confirm your entry, or press n to exit")
                while True:
                    if keyboard.is_pressed('y') or keyboard.is_pressed('tab'):
                        keyboard.press('backspace')
                        connector.commit()
                        cursor.execute("SELECT * FROM users WHERE ROWID = LAST_INSERT_ROWID()")
                        user = cursor.fetchone()
                        print()
                        print(user)
                        userID = user[3]
                        return userID
                    if keyboard.is_pressed('n') or keyboard.is_pressed('esc'):
                        keyboard.press('backspace')
                        print("user creation canceled")
                        break
                break
            if keyboard.is_pressed('esc'):
                print()
                print("action canceled")
                break


def save_letter(letterStats):
    connector = sqlite3.connect("testUsers.db")
    cursor = connector.cursor()
    userID = letterStats[0][0]
    while letterStats.__len__() > 0 :
        letterStat = letterStats.pop(0)
        letter = letterStat[1]
        success = letterStat[2]

        cursor.execute("SELECT * FROM letterStats WHERE userid = ? AND letter = ?", (userID, letter))
        letter_previous = cursor.fetchone()

        if letter_previous is None:
            cursor.execute("INSERT INTO letterStats VALUES (?,?,?, null, ?)", (letter, 1, 0, userID))
        elif success:
            count = letter_previous[1] + 1
            history = round(letter_previous[2] + .2,1)
            cursor.execute("""UPDATE letterStats SET letterCount = ?, letterHistory = ? WHERE id = ?""",
                           (count, history, letter_previous[3]))
        else:
            count = letter_previous[1] + 1
            history = round(letter_previous[2] - 1,1)
            cursor.execute("""UPDATE letterStats SET letterCount = ?, letterHistory = ? WHERE id = ?""",
                           (count, history, letter_previous[3]))

    connector.commit()
def save_results(userID, testText, testTime, letterStats):
    print()
    print("Press y to save this test or n to not")
    if testTime is not None:
        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                keyboard.press('backspace')
                if (event.name == "y" or event.name == "tab" or event.name== "enter"):
                    time.sleep(0.01)
                    keyboard.press('backspace')
                    print("Test is being saved please wait :D")
                    save_letter(letterStats)
                    connector = sqlite3.connect("testUsers.db")
                    cursor = connector.cursor()
                    testTimeMin = testTime / 60
                    cursor.execute("SELECT * FROM users WHERE ROWID = ?", (userID,))
                    user = cursor.fetchone()
                    userTime = user[2]
                    updateQuery = """UPDATE users SET timeUsedMinutes = ? WHERE ROWID = ?"""
                    cursor.execute(updateQuery, (round(userTime + testTimeMin, 2), userID))
                    connector.commit()

                    speed = (testText.__len__() / avgWordLength) / testTime
                    speed = speed * 60
                    cursor.execute("""INSERT INTO typingStats VALUES(?,?,?,?,NULL)""",
                                   (date.today(), testText.__len__(), speed, userID))
                    connector.commit()
                    cursor.execute("""SELECT AVG(averageWPM) FROM typingStats WHERE userid = ?""", userID)
                    averageWPM = cursor.fetchone()[0] + 0
                    print()
                    print("User average WPM: " + round(averageWPM, 0).__str__())
                    break
                if (event.name == "n" or event.name == "esc"):
                    print()
                    print("Did not save this test")
                    break


def test_length():
    while True:
        try:
            user_input = input("How many words do you want the tests to have: ")
            count = int(user_input)  # Try to convert the input to a float
            return count  # Exit the loop if conversion to float succeeds
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def StartTest(userID):
    letterStats =[]

    def typing_text(testText):
        print("type the following text : ")
        print(testText)
        while True:
            event = keyboard.read_event()
            if event.name == testText[0]:
                start = time.perf_counter()
                i = 1
                while True:
                    event = keyboard.read_event()
                    if event.event_type == keyboard.KEY_DOWN:
                        if event.name == testText[i] or (event.name == 'space' and testText[i] == " "):
                            if userID != None and testText[i] != " ":
                                letterStats.append([userID, testText[i], True])
                            i += 1
                        elif event.name.__len__() == 1 or event.name == 'space':
                            keyboard.press('backspace')
                            if userID != None and testText[i] != " ":
                                letterStats.append([userID, testText[i], False])
                        if event.name == 'backspace':
                            keyboard.write(testText[i-1])

                    if i > len(testText) - 1:
                        end = time.perf_counter()
                        timeUser = end - start
                        return timeUser, letterStats

                    if keyboard.is_pressed('tab'):
                        print()
                        print("TEST STOPPED")
                        break
            if keyboard.is_pressed('tab'):
                print()
                print("TEST STOPPED")
                break

    def ContinueTest():
        keyboard.write("")
        print("Press y to test again or n to stop testing")
        while True:
            if (keyboard.is_pressed('y') or keyboard.is_pressed('tab')):
                keyboard.press('backspace')
                time.sleep(.05)
                print()
                return True
            if (keyboard.is_pressed('n') or keyboard.is_pressed('esc')):
                keyboard.press('backspace')
                time.sleep(.05)
                print()
                return False

    testContinue = True
    testLength = test_length()
    print()
    while testContinue:
        if userID is not None:
            testText = TestGenerator.newTestSQLUser(int(testLength), userID)
        else:
            testText = TestGenerator.newTestSQL(int(testLength))
        testTime, letterStats = typing_text(testText)
        time.sleep(0.02)
        print()
        if None != testTime:
            print("WPM for this test: " + round((testText.__len__() / avgWordLength) / testTime * 60, 0).__str__())

        if userID is not None:
            save_results(userID, testText, testTime, letterStats)
            print()
        testContinue = ContinueTest()


def userChoices():
    connector = sqlite3.connect("testUsers.db")
    userID = None
    while True:
        print()
        if userID != None:
            cursor = connector.cursor()
            cursor.execute("SELECT * FROM users WHERE ROWID = ?", userID)
            user = cursor.fetchone()
            print("Logged in: ")
            print(user)
        else:
            print("No user logged in")
        print()
        print("1. Start test")
        print("2. See Stats")
        print("3. Delete a user")
        print("4. Log in or Sign Up")
        print("5. Log out")
        print("6. Close the program")
        print()
        choice = input("Enter choice number: ")
        if choice == "1":
            StartTest(userID)
        if choice == "2":
            print("Stats page still in progress")
        if choice == "3":
            connector = sqlite3.connect("testUsers.db")
            connector.execute('PRAGMA foreign_keys = ON;')
            cursor = connector.cursor()
            if all_rows('users').__len__() > 0:
                all_rows_print('users')
                userID = input("Enter id of the user to be deleted: ")
                cursor.execute("DELETE FROM users WHERE rowid = ?", userID)
                connector.commit()
            else:
                print("No current users")

        if choice == "4":
            userID = user_log().__str__()
            if userID == "None":
                userID = None

        if choice == "5":
            userID = None
            print("User Logged out")
        if choice == "6":
            sys.exit()


userChoices()
