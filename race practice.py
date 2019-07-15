# pull race data from scraped files and test on them
# perhaps use code from practice typing words.py for now, test random strings
# make a ui later?

# ******************************************************************************

import sys
import random

# ******************************************************************************

def newWord():
    # pick a random 'trouble' word and practice it
    practiceWord = mistakes[random.randint(0, len(mistakes)-1)]
    practiceWord = practiceWord[0:len(practiceWord)-1] #gets rid of newline character
    print 'new word: ', practiceWord
    return practiceWord


def practice(practiceWord):
    
    correctCounter = 0

    # type word correctly x times     
    while (correctCounter < 10):
        wordAttempt = raw_input('attempt: ')
        if (wordAttempt == practiceWord):
            correctCounter += 1
            print 'consecutive correct: ', correctCounter
        elif (wordAttempt == 'cw'):
            practiceWord = newWord()
            correctCounter = 0
        elif (wordAttempt == 'exitprogram'):
            print 'ok bye'
            sys.exit(0)
        else:
            correctCounter = 0
            print 'back to 0'
    # end while loop
    print 'nice'

# ******************************************************************************

# open files created from scraping
resultsFile = open('raceresults.txt', 'r')
results = resultsFile.readlines()
mistakesFile = open('mistakes.txt', 'r')
mistakes = mistakesFile.readlines()
resultsFile.close()
mistakesFile.close()

print 'cw to change word, exitprogram to exit'

# main loop
while True:
    practiceWord = newWord()
    practice(practiceWord)
# end main loop

# ******************************************************************************
