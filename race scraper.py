'''
 test to pull TypeRacer race data (full texts and mistakes made) from my personal history
'''
# ******************************************************************************

from bs4 import BeautifulSoup
from selenium import webdriver
import re
import sys
import json

# ******************************************************************************

# use selenium/chromedriver/beautifulsoup to do things

path = r'C:\Users\theja\Documents\python stuff\chromedriver.exe'
browser = webdriver.Chrome(executable_path = path)

baseURL = 'https://data.typeracer.com/pit/result?id=|tr:softaco|'
urlProfile = 'https://data.typeracer.com/pit/profile?user=softaco'

browser.get(urlProfile)
allHTML = browser.execute_script("return document.body.innerHTML")
soup = BeautifulSoup(allHTML, 'html.parser')
raceNum = soup.find(text=re.compile("Races Completed"))
raceNum = int(raceNum.find_next().get_text().strip())
print 'total races: ', raceNum, '\n'

# ******************************************************************************

# go through all races
results = {}
allMistakes = set()
completed = 0
racesToScrape = int(input("how many races shall we scrape? enter a number: "))
if racesToScrape < 0:
    racesToScrape = 0
elif racesToScrape > raceNum:
    racesToScrape = raceNum
print 'scraping', racesToScrape, 'races ... '

## main loop
while completed < racesToScrape:
    url = baseURL + str(raceNum - completed)
    browser.get(url)
    allHTML = browser.execute_script("return document.body.innerHTML") 
    soup = BeautifulSoup(allHTML, 'html.parser')    

    fullText = soup.find(class_= "fullTextStr").get_text()
    mistakes = soup.find_all("div", class_ = "replayWord")
    for j in range(len(mistakes)):
        mistakes[j] = mistakes[j].get_text()[2:]
    
    # save results
    results[raceNum - completed] = {'full text': fullText, 'mistakes made': mistakes}
    allMistakes = allMistakes | set(mistakes)

    completed += 1
## end main loop

# ******************************************************************************

# common words to exclude from unique mistake list
commonWordList = ['the', 'be', 'to', 'and', 'a', 'in', 'that', 'have', 'I', 'it',
            'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 
            'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 
            'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what', 
            'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 
            'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 
            'take', 'person', 'into', 'year', 'your', 'good', 'some', 'could', 
            'them', 'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come', 
            'its', 'over', 'think', 'also', 'back', 'after', 'use', 'two', 'how', 
            'our', 'work', 'first', 'well', 'way', 'even', 'new', 'want', 'any', 
            'these', 'give', 'day', 'most', 'us', 'of', 'saw', 'many']

## record results in files
with open('raceresults.txt', 'r+') as resultFile:
    json.dump(results, resultFile)

with open('mistakes.txt', 'r+') as mistakesFile:
    json.dump(list(allMistakes), mistakesFile)

print 'saved data from', completed, 'races!!'

## clean up    
browser.close() # close browser window
browser.quit()  # quits task, clears memory etc
sys.exit(0)

# ******************************************************************************
