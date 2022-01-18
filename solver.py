from cgi import test
import random 
import re
from tabnanny import check

def chooseword():
    lines = open('temp', "r").read().splitlines()
    return random.choice(lines)

def validateinput(result):
    if re.search(r'[^a-c]', result):
        print("Invalid input: " + result)
        return False
    elif len(result) != 5:
        print("Invalid input: " + result)
        return False
    else:
        return True

def createtemp(wordlist):
    temp = open("temp", "w")
    temp.write("")
    temp = open("temp", "a")
    for line in wordlist:
        temp.write(line)
    return temp

def readandclear():
    temp = open("temp", "r")
    lines = temp.readlines()
    temp = open("temp", "w")
    temp.write("")
    return lines

def handleabsent(chars):
    lines = readandclear()
    temp = open("temp", "a")
    regex = "[" + chars + "]"
    for line in lines:
        if not re.search(regex, line):
            temp.write(line)

def handlepresent(char, i):
    lines = readandclear()
    temp = open("temp", "a")
    for line in lines:
        if re.search(char, line) and line[i] != char:
            temp.write(line)

def handlecorrect(char, i):
    lines = readandclear()
    temp = open("temp", "a")
    for line in lines:
        if line[i] == char:
            temp.write(line)
    
def solve():
    createtemp(open("wordlist", "r"))
    for i in range(6):
        word = chooseword()
        print("Enter: " + word.upper() + " on Worlde, then enter the response here.")
        print("a: absent, b: present, c: correct")
        result = input()
        if result == "ccccc":
            print("Solved!")
            exit()
        while(not validateinput(result)):
            result = input()
            if result == "ccccc":
                print("Solved!")
                exit()

        absent = ""
        for i in range(5):
            char = result[i]
            if char == 'a':
                absent += word[i]
            elif char == 'b':
                handlepresent(word[i], i)
            else:
                handlecorrect(word[i], i)
        if absent != "":
            handleabsent(absent)

def calculateresult(secret, word):
    result = ""
    for i in range(5):
        temp = "a"
        char = word[i]
        for secretchar in secret:
            if secretchar == char:
                temp = "b"
                if secretchar == secret[i]:
                    temp = "c"
        result += temp
    return result

def debugprint(debug, string):
    if debug:
        print(string)

def testsolve(debug = True):
    createtemp(open("wordlist", "r"))
    secret = chooseword()
    debugprint(debug,"Secret: " + secret)
    for i in range(6):
        debugprint(debug, "Step " + str(i + 1) + ":")
        word = chooseword()
        result = calculateresult(secret, word)
        debugprint(debug, word + "->" + result)
        if result == "ccccc":
            debugprint(debug, "Solved!")
            return True
        absent = ""
        for i in range(5):
            char = result[i]
            if char == 'a':
                absent += word[i]
            elif char == 'b':
                handlepresent(word[i], i)
            else:
                handlecorrect(word[i], i)
        if absent != "":
            handleabsent(absent)
    return False

def testalgorithm(iterations, debug = False):
    solves = 0
    for i in range(iterations):
        if testsolve(False):
            solves += 1
    print("Solved " + str(solves) + " out of " + str(iterations) + ". " + str((solves/iterations) * 100) + "%")

testalgorithm(100000, False)
