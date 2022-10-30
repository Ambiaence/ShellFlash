import os
import copy
import time
import statistics
import pickle
from integral_mapper import IntegralMap
from os.path import exists
class Deck:
    def __init__(self):
        self.cards = []
        self.directory = input("What is the name of the folder the deck is contained in?")
        os.chdir(self.directory)
        cardNames = self.loadCardListFromIndex()
        self.loadCards(cardNames)

        if exists("save"):
            self.save = self.loadSave()
        else:
            os.system("touch save") #Hacky way to do this not portable
            self.save = self.createSave()
        self.sortCardsByProficiency()

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

    def loadSave(self):
        pickle_in = open("save", "rb")
        save = pickle.load(pickle_in)

        for card in self.cards:
            for sav in save:
                if sav.nameOfCard == card.name:
                    print(sav.nameOfCard, "and", card.name)
                    card.proficiency = sav.proficiencyOfCard

    def createSave(self):
        save = [] 
        for card in self.cards:
            save.append(Save(card.name, card.proficiency))
        return save

    def updateSaveFile(self):
       self.save = self.createSave()
       pickle_out = open("save", "wb") 
       pickle.dump(self.save, pickle_out)
       pickle_out.close()

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

        if card.proficiency.answerTime == None:
            print("Please write the answer to gage a answering time. The answer will appear twice. The second time will be used to gage time")
            input("")
            os.system(card.answer)
            input("")
            start = time.time()
            os.system(card.answer)
            input("")
            card.proficiency.answerTime = time.time() - start
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
            modifiedTime = (total - card.proficiency.answerTime)
            if modifiedTime < 3:
                card.proficiency.newTime(3) 
            else:
                card.proficiency.newTime(modifiedTime) 

        if inp == "n":
            card.proficiency.miss()

        print(card.proficiency.avg)
        print(card.proficiency.missed)

class Save:
    def __init__(self, name, prof):
        self.nameOfCard = name
        self.proficiencyOfCard = prof

class Card:
    def __init__(self, name, question, answer):
        self.name = name
        self.question = question
        self.answer = answer
        self.proficiency = Proficiency()
    def printContents(self):
        print(self.name)
        print(self.question)
        print(self.answer)

class Proficiency:
    def __init__(self):
        self.avg = None # Average of last three times
        self.missed = 3 # The number of correct answers before question is considered known
        self.answerTime = None  
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
