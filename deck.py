import os
import time
class Deck:
    def __init__(self):
        self.cards = []
        self.directory = input("What is the name of the folder the deck is contained in?")
        os.chdir(self.directory)
        cardNames = self.loadCardListFromIndex()
        self.loadCards(cardNames)
        for card in self.cards:
            card.printContents()

    def loadCardListFromIndex(self):
        f = open("index", 'r')
        ls = []
        for line in f.readlines():
            ls.append(line[:-1]) #Last line ommited

        return ls
        
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

      #  print("AnswerTime", card.answerTime)
      #  start = time.time()
      #  os.system(self.cards[index].question)
      #  
      #  end = time.time() - start
      #  os.system(self.cards[index].answer)
      #  
      #  inp = None
      #  while inp != "y" and inp != "n":
      #      inp = input("Did you get it correct y/n")
      #  
      #  if inp == "y":
      #     cards.humanAnswerTime
      #                     
      # if inp == "n":
           
class Card:
    def __init__(self, name, question, answer):
        self.name = name
        self.question = question
        self.answer = answer
        self.answerTime = None #The amount of time it takes to physically answer a question
        self.humanAnswerTime = None  #The hypothetical human recall time

    def printContents(self):
        print(self.name)
        print(self.question)
        print(self.answer)

deck = Deck()
deck.repCard(2)
deck.repCard(3)
deck.repCard(2)
deck.repCard(3)
deck.repCard(3)
