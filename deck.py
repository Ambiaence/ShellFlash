import os
import copy
import time
import statistics
from integral_mapper import IntegralMap
class Deck:
    def __init__(self):
        self.cards = []
        self.directory = input("What is the name of the folder the deck is contained in?")
        os.chdir(self.directory)
        cardNames = self.loadCardListFromIndex()
        self.loadCards(cardNames)


    def numOfCards(self):
        return len(self.cards)

    def loadCardListFromIndex(self):
        f = open("index", 'r')
        ls = []
        for line in f.readlines():
            ls.append(line[:-1]) #Last line ommited

        return ls
    def sortCardsByProficiency(self):  
        cards = self.cards
        numOfMissed = 0
        sortedCards = copy.copy(cards);
        for x in range(0, len(cards)):
            if cards[x].proficiency.missed > 0:     
                numOfMissed = numOfMissed + 1
                sortedCards.insert(0, sortedCards.pop(x))

        sortedCards[numOfMissed:] = sorted(sortedCards[numOfMissed:],key = lambda card : card.proficiency.avg , reverse = True)
        self.cards = sortedCards

    def printState(self):
        os.system("clear")
        for card in self.cards:
            print("Name:", card.name, "Avg:", card.proficiency.avg, "Missed:", card.proficiency.missed)

    def loadCards(self, cardNames):
        for name in cardNames: 
            f = open(name, 'r')
            question = f.readline()  
            answer = f.readline()  
            self.cards.append(Card(name, question, answer))

    def repCard(self, index):
        card = self.cards[index]

        if card.answerTime == None:
            print("Please write the answer to gage a answering time. The answer will appear twice. The second time will be used to gage time")
            input("")
            os.system(card.answer)
            start = time.time()
            os.system(card.answer)
            card.answerTime = time.time() - start
            return

        start = time.time()
        os.system(self.cards[index].question) 
        input("Hit any key to continue")
        total = time.time() - start
        os.system(self.cards[index].answer)
        
        inp = None
        while inp != "y" and inp != "n":
            inp = input("Did you get it correct y/n")
        
        if inp == "y":
            modifiedTime = (total - card.answerTime)
            if modifiedTime < 3:
                card.proficiency.newTime(3) 
            else:
                card.proficiency.newTime(modifiedTime) 

        if inp == "n":
            card.proficiency.miss()

        print(card.proficiency.avg)
        print(card.proficiency.missed)

class Card:
    def __init__(self, name, question, answer):
        self.name = name
        self.question = question
        self.answer = answer
        self.answerTime = None #The amount of time it takes to physically answer a question
        self.proficiency = Proficiency()
    def printContents(self):
        print(self.name)
        print(self.question)
        print(self.answer)

class Proficiency:
    def __init__(self):
        self.avg = None # Average of last three times
        self.missed = 3 # The number of correct answers before question is considered known
        self.__lastThreeTimes = []

    def newTime(self, time):
        if len(self.__lastThreeTimes) != 0:
            self.__lastThreeTimes.pop(0) 

        self.__lastThreeTimes.append(time)
        if self.missed > 0:
            self.missed = self.missed-1;
            print("Missed", self.missed)
        self.__average(self.avg)

    def miss(self):
        self.missed = 3

    def __average(self, avg):
        self.avg = statistics.mean(self.__lastThreeTimes)
