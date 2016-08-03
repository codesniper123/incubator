'''
Scores are maintained in SCurrent and generated in SNext.

SCurrent is a dictionary where:
    the key is the digit we are currently in
    the value is another dictionary of all possible scores with their respective probabilities


Todo:
    10 digit formatting
    Test!!
'''

import math

class Phonepad:
    def __init__(self):
        self.setupNext();
        self.setupS();

    def createNext(self, modulo):
        self.SNext = {}

        # currentScores is a dictionary of all possible scores:
        for currentDigit, currentScores in self.SCurrent.iteritems():
            # nextDList is a list of next digit with the probability:
            nextDList = self.nextD[currentDigit]
            # Go through all scores:
            for currentScore, currentProb in currentScores.iteritems():
                # nextDP = (nextDigit, probability)
                for nextDP in nextDList:
                    if nextDP[0] not in self.SNext:
                        self.SNext[nextDP[0]] = {}
                    nextScores = self.SNext[nextDP[0]]
                    nextScore = (currentScore + nextDP[0])
                    if modulo != None:
                        nextScore = nextScore % modulo
                    nextProb = currentProb * nextDP[1]
                    if nextScore in nextScores:
                        nextScores[nextScore] = nextScores[nextScore] + nextProb
                    else:
                        nextScores[nextScore] = nextProb

        self.SCurrent = self.SNext

    def prettyPrint(self):
        for digit, scores in self.SCurrent.iteritems():
            print "digit = {} possible values of S {}".format(digit, len(scores))
            for score, prob in scores.iteritems():
                print "score = {} probability = {}".format(score, prob)

    #
    # E(X) = sum x*p(x)
    # V(X) = sum x^2*p(x) - (E(X))^2
    def printExpectedVariance(self):
        e = 0.0
        exsquared = 0.0
        v = 0.0
        for digit, scores in self.SCurrent.iteritems():
            for score, prob in scores.iteritems():
                e += score * prob
                exsquared += score * score * prob;


        v = math.sqrt( exsquared - (e*e) )

        print "Expected Value = {} Variance = {}".format(e, v)

    def printConditionalProb(self, which, given, debug):
        # which is the numerator
        # given is the denominator:
        l_scores = []
        numer = 0.0
        denom = 0.0
        for digit, scores in self.SCurrent.iteritems():
            for score, prob in scores.iteritems():
                if debug:
                    l_scores.append(score)
                if score % given == 0:
                    denom += prob
                    if score % which == 0:
                        numer += prob

        whichProb = numer / denom

        if debug:
            print l_scores

        print "Probability S is divisible by {} given S is divisible by {} is {}".format(which, given, whichProb)





    def setupNext(self):
        tempNextD = {
            0: (4,6),
            1: (6,8),
            2: (7,9),
            3: (4,8),
            4: (0,3,9),
            5: (),
            6: (0,1,7),
            7: (2,6),
            8: (1,3),
            9: (2,4)
        };

        self.nextD = dict()
        for d, nextD in tempNextD.iteritems():
            l = len(nextD)
            tempV = list()
            for i in nextD:
                tempV.append( (i, 1.0/l) )
            self.nextD[d]  = tempV

        ## print self.nextD


    def setupS(self):
        self.SCurrent = { 0 : {0:1} }
        self.SNext = {}

def main():
    pad = Phonepad()

    print "10 iterations;  modulo 10"
    for i in range(0,10):
        ##print "Iteration = {}".format(i+1)
        pad.createNext(10)
        # pad.prettyPrint()

    pad.printExpectedVariance()

    pad = Phonepad()

    print "1024 iterations;  modulo 1024"
    for i in range(0,1024):
        ##print "Iteration = {}".format(i+1)
        pad.createNext(1024)
        # pad.prettyPrint()
    pad.printExpectedVariance()

    pad = Phonepad()

    print "10 iterations;  no modulo"
    for i in range(0,10):
        ##print "Iteration = {}".format(i+1)
        pad.createNext(None)
        # pad.prettyPrint()

    pad.printConditionalProb(5, 7, False)

    pad = Phonepad()

    print "1024 iterations;  no modulo"
    for i in range(0,1024):
        ##print "Iteration = {}".format(i+1)
        pad.createNext(None)
        # pad.prettyPrint()
    pad.printConditionalProb(23, 29, False)




if __name__ == "__main__":
    main();

