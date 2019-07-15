# test to pull TypeRacer race data

# ******************************************************************************

from bs4 import BeautifulSoup
from selenium import webdriver
import re
import sys

# ******************************************************************************

# create/open output files
resultsFile = open('raceresults.txt', 'w+')
mistakesFile = open('mistakes.txt', 'w+')

# ******************************************************************************

# use selenium/chromedriver/beautifulsoup to do things

path = r'C:\Users\theja\Documents\python stuff\chromedriver.exe'
browser = webdriver.Chrome(executable_path = path)

baseURL = 'https://data.typeracer.com/pit/result?id=|tr:softaco|'   # append race number to this
urlProfile = 'https://data.typeracer.com/pit/profile?user=softaco'  # use this to get total number of races

browser.get(urlProfile)
allHTML = browser.execute_script("return document.body.innerHTML") #returns the inner HTML as a string
soup = BeautifulSoup(allHTML, 'html.parser')    # convert into a beautifulsoup object so i can use its stuff
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
    url = baseURL + str(raceNum - completed)    # create the next url by appending the race number
    browser.get(url)
    allHTML = browser.execute_script("return document.body.innerHTML") #returns the inner HTML as a string
    soup = BeautifulSoup(allHTML, 'html.parser')    # convert into a beautifulsoup object so i can use its stuff

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
for i in results:
    resultsFile.write(str(i))
    resultsFile.write('\t')
    resultsFile.write(str(results[i]['full text']))
    resultsFile.write('\t')
    resultsFile.write(str(results[i]['mistakes made']))
    resultsFile.write('\n')

for mistake in allMistakes:
    if mistake.lower() in commonWordList:
        pass
    else:
        mistakesFile.write(str(mistake))
        mistakesFile.write('\n')

print 'saved data from', completed, 'races!!'

## clean up    
browser.close() # close browser window
browser.quit()  # quits task, clears memory etc
resultsFile.close()
mistakesFile.close()
sys.exit(0)

# ******************************************************************************
