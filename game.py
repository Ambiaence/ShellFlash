from deck import Deck 
import numpy 
from integral_mapper import IntegralMap
dk = Deck()
im = IntegralMap(dk.numOfCards(), lambda x: -numpy.log(x), 0, 1)
while(True):
    dk.repCard(im.pickRandomIndex())
    dk.sortCardsByProficiency()
    dk.updateSaveFile()
    dk.printState()
