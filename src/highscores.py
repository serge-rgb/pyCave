#    This file is part of pyCave.
#
#    pyCave is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    pyCave is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with pyCave.  If not, see <http://www.gnu.org/licenses/>.


'''
This is a mostly functional module, all the state is kept in the file.
'''

import pickle

class Highscore (object):
    def __init__ (self,name,score):
        self.name = name
        self.score = score
        
    def __str__ (self):
        return str(self.name) + ': ' + str(self.score)

def load ():
    '''
    If file exists, load data. Else, insert our values.
    Return a highscore list
    '''
    #Initial values
    highscores = [
        Highscore('Rodrigo',59),
        Highscore('Daniel',823),
        Highscore('Matias',1234),
        Highscore('Sergio',1700)
        ]
    try:
        hsfile = open("media/hs.dat",'r')
        return pickle.load(hsfile)
    except:
        hsfile = open("media/hs.dat",'w')
        pickle.dump(highscores,hsfile)
        hsfile.close()
        return highscores
    
#print [str(a) for a in highscores]
          
def add (hs,new):
    def cmp (hs1, hs2):
        print "COMPARING" , hs1,hs2,hs1.score-hs2.score
        return int(hs1.score - hs2.score)
    if len(hs+[new])>10:
       del hs[0]
    print "DATA" ,hs,new
    return sorted(hs+[new],cmp)

def isCandidate (highscores,score):
    if len(highscores) <= 10 or score > highscores[0].score:
        return True
    return False

def checkNewScore(score):
    """Do we add this score to our highscores?"""
    hs = load()
    return isCandidate(hs,score)

def maybeAdd (highscores,name, score):
    hs = Highscore(name,score)
    if isCandidate(highscores,score):
        return add(highscores,Highscore(name,score))
    return highscores

def store (hs):
    hsfile = open("media/hs.dat",'w')
    pickle.dump(hs,hsfile)
    hsfile.close()
    
def maybeStore (name,score):
    hscores = maybeAdd(load(),name,score)
    store(hscores)
    return hscores
    
    
