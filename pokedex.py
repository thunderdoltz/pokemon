from moves import *
from random import *
import copy
import inspect

def menuValid(number, maxNum):
    noGood = 'invalid input'
    try:
        number = int(number)
        if number <= maxNum and number >0:
            return True
        else:
            print(noGood)
            return False
    except ValueError:
        print(noGood)
        
class pokemon:
    """
    creates a pokemon

    takes a name as a string
    starting pokemon level; integer
    typ is the pokemon type; list of two entries; ['water', 'fire']
    takes maxHP as an integer
    takes stats as a dictionary formatted as {'attack':30, 'defense':40, 'speed': 40}
    takes moves as a dictionary formatted as {1:[tackle, 'tackle'],etc}
    baseXP is the base amount of XP the pokemon gives if killed; integer
    needXP is amount of XP needed to gain a level; integer
    XPmod is how much the gained XP is adjusted; two digit, single decimel place; 1.6 or 0.8 
    """
    def __init__(self,name, pokeNum, entry, level,typ,statMods, moves, needXP,XPmod,evo, trainer=1):
        self.name = name
        self.pokeNum = pokeNum
        self.entry = entry
        self.level = level
        self.typ = typ
        self.maxHP = 10
        self.statMods = statMods
        self.moves = moves
        self.HP = self.maxHP #sets current HP equal to max HP at creation
        self.needXP = needXP
        self.XPmod = XPmod
        self.gainedXP = 0
        self.stats = {'attack':5, 'defense':5, 'sp.attack':5, 'sp.defense':5, 'speed':5}
        self.tempStats = copy.deepcopy(self.stats)
        self.status = []
        self.evo = evo
        self.trainer = trainer

    def getName(self): #gives the name of the pokemon
        print(self.name)

    def HPBar(self): #displays the current HP of the pokemon as a bar
        percentage = self.HP/self.maxHP
        remaining = round(20*percentage)
        taken = 20 - remaining
        return '('+'#'*remaining+'-'*taken+')'

    def getMoves(self): #returns the list of available moves
        for i in range(1,len(self.moves)+1):
            print(str(i)+'.', self.moves[i].name)
        print(str(i+1)+'. cancel')

    def learnMove(self, move):
        moveNo = len(self.moves)+1
        if moveNo<=4:
            self.moves[moveNo] = move
            print(self.name, 'learned', move.name+'!')
            input()
        else:
            while True:
                print(self.name, 'is trying to learn', move.name,'but',self.name,'already knows four moves')
                print('Would you like to replace one of these moves?')
                self.getMoves()
                print('5. No, do not learn move')
                action = input()                
                if menuValid(action, 5):
                    action = int(action)
                    if action == 5:
                        print(self.name, 'did not learn', move.name)
                        break
                    else:
                        print(self.moves[action].name,'will be replaced with',move.name)
                        while True:
                            print('Are you sure? y/n')
                            sure = input()
                            if sure ==  'y' or sure == 'n':
                                break
                        if sure == 'y':
                            self.moves[action] = move
                            print(self.name, 'learned', self.moves[action].name+'!')
                            break
                        

    def damageTaken(self, damage): #reduces the HP when damage is taken
        if damage == 0:
            self.HP = self.HP
        else:
            self.HP -= damage

    def useMove(self, index, opponent): #uses the indicated move
        x = self.moves[index][0]
        x(self, opponent)

    def statChange(self, stat, boost): #reduces the appropriate stat when stat damage is taken
        minstat = .131
        maxstat = 4
        ratio = self.tempStats[str(stat)]/self.stats[str(stat)]
        margin = 0.02
        if abs(ratio - minstat)<margin:
            print(str(self.name)+'\'s', stat,'can\'t be reduced anymore!')
        elif abs(ratio-maxstat)<margin:
            print(str(self.name)+'\'s',stat,'can\'t be increased anymore!')
        else:
            if boost:
                change = 'increased!'
                self.tempStats[str(stat)] *= 1.33
            else:
                change = 'decreased!'
                self.tempStats[str(stat)]*= 0.66
            print(self.name+'\'s',stat,change)

    def XPGain(self, opponent):
        gain = round(opponent.needXP/2)*opponent.trainer
        self.gainedXP += gain
        print(self.name,'gained',gain,'experience!')
        if self.gainedXP >= self.needXP:
            self.levelUp()

    def levelUp(self):
        print(self.name, 'grew to level', str(self.level+1)+'!')
        self.gainedXP = 0
        self.addLevel(2)
        print(self.stats)
        if self.level in moveTree[self.name]:
            self.learnMove(moveTree[self.name][self.level])

    def evolve(self):
        print('Huh?',self.name,'is evolving!')
        input()
        for level in self.evo:
            newPoke = self.evo[level]
        for thing in evos:
            if thing[0] == newPoke:
                newPoke = thing[1]
        print(self.name,'evolved into',newPoke.name+'!')
        self.name = newPoke.name
        self.pokeNum = newPoke.pokeNum
        self.statMods = newPoke.statMods
        self.entry = newPoke.entry
        self.evo = newPoke.evo
        self.needXP = newPoke.needXP
        self.maxHP = round(10+self.level*self.statMods[0])
        self.stats['attack'] = round(5+self.level*self.statMods[1])
        self.stats['defense'] = round(5+self.level*self.statMods[2])
        self.stats['sp.attack'] = round(5+self.level*self.statMods[3])
        self.stats['sp.defense'] = round(5+self.level*self.statMods[4])
        self.stats['speed'] = round(5+self.level*self.statMods[5])
        self.tempStats = self.stats
        
    def addLevel(self, endLevel):
        levelsAdded = endLevel - 1
        self.level+=levelsAdded
        if self.level in self.evo:
            self.evolve()
        self.maxHP += round(levelsAdded*self.statMods[0])
        self.HP += round(levelsAdded*self.statMods[0])
        self.stats['attack'] = round(self.stats['attack']+levelsAdded*self.statMods[1])
        self.stats['defense'] = round(self.stats['defense']+levelsAdded*self.statMods[2])
        self.stats['sp.attack'] = round(self.stats['sp.attack']+levelsAdded*self.statMods[3])
        self.stats['sp.defense'] = round(self.stats['sp.defense']+levelsAdded*self.statMods[4])
        self.stats['speed'] = round(self.stats['speed']+levelsAdded*self.statMods[5])
        self.tempStats['attack']= round(self.tempStats['attack']+levelsAdded*self.statMods[1])
        self.tempStats['defense']= round(self.tempStats['defense']+levelsAdded*self.statMods[2])
        self.tempStats['sp.attack']= round(self.tempStats['sp.attack']+levelsAdded*self.statMods[3])
        self.tempStats['sp.defense']= round(self.tempStats['sp.defense']+levelsAdded*self.statMods[4])
        self.tempStats['speed']= round(self.tempStats['speed']+levelsAdded*self.statMods[5])
        for i in range(levelsAdded):
            self.needXP = round(self.needXP*self.XPmod)

    def statRestore(self):
        self.tempStats = copy.deepcopy(self.stats)

    def heal(self, amount):
        self.HP += amount
        if self.HP > self.maxHP:
            self.HP = self.maxHP
    

    def statusAction(self, opponent, position):
        """
        Performs the relevant status effects
        position is the place in the battle sequence it happens
        'before' = before the turn
        'during' = during the turn
        'after' = after the turn
        """
        act = []

        #non-exclusive statuses
        if 'leech' in self.status:
            if position == 'after':
                damage = self.maxHP//16+1
                self.damageTaken(damage)
                opponent.heal(damage)
                print(opponent.name,'absorbed health from',self.name)
                input()

        if 'confusion' in self.status:
            if position == 'before':
                print(self.name,'is confused!')
            if position == 'during':
                chance = [True, False, False, False]
                hurt = [True,False]
                clear = choice(chance)
                if clear:
                    print(self.name,'broke out of it\'s confusion!')
                    self.status.remove('confusion')
                    act.append(True)
                else:
                    if hurt:
                        print(self.name,'hurt itself in it\'s confusion!')
                        selfDamage = damage(self, self, 40, 'attack','defense')
                        act.append(False)
                
        if 'burn' in self.status:
            if position == 'before':
                self.tempStats['attack'] = self.stats['attack']/2
            elif position == 'after':
                damage = round(self.maxHP/8)
                self.damageTaken(damage)
                print(self.name, 'was hurt by the burn')
                input()

        
        #exclusive statuses
        elif 'paralyzed' in self.status:
            if position == 'before':
                print(self.name,'is paralyzed, it may not attack')
            elif position == 'during':    
                chance = [True,True,False]
                paralyze = choice(chance)
                if paralyze == False:
                    print(self.name, 'is fully paralyzed!')
                    input()
                act.append(paralyze)
        
        elif 'sleep' in self.status:
            if position == 'before':
                print(self.name,'is asleep!')
            elif position == 'during':
                chance = [True,False,False]
                sleep = choice(chance)
                if sleep == True:
                    print(self.name,'woke up!')
                    self.status.remove('sleep')
                    act.append(True)
                else:
                    print(self.name,'is fast asleep')
                    input()
                    act.append(False)
                    
        elif 'poison' in self.status:
            if position == 'after':
                damage = round(self.maxHP/8)
                self.damageTaken(damage)
                print(self.name, 'was hurt by the poison')
                input()
              
        return False not in act

def pokemonGenerator(pokemon, level, givenMoves, trainer = 1):
    newPoke = copy.deepcopy(pokemon)
    newPoke.trainer = trainer
    newPoke.addLevel(level)
    i = 1
    for move in givenMoves:
        newPoke.moves[i] = move
        i += 1
    return newPoke

class pokedex: #fills the global pokedex
    def __init__(self):
        self.bulbasaur = pokemon('Bulbasaur', 1, 'This pokemon has a large plant bulb on it\'s back', 1, ['grass','poison'],\
                                 [2,0.98,0.98,1.3,1.3,0.9],{}, 20, 1.3,{15:'ivysaur'})
        self.ivysaur = pokemon('Ivysaur', 2, 'This pokemon has a small flower on it\'s back',1,['grass','poison'],\
                               [2.3,1.24,1.26,1.6,1.6,1.2],{},30,1.3,{34:'venusaur'})
        self.venusaur = pokemon('Venusaur',3, 'This pokemon has a large flower on it\'s back which it uses to photosynthesize',1,['grass','poison'],\
                                [2.7,1.64,1.66,2.0,2.0,1.6],{},40,1.3,{0:0})
        self.charmander = pokemon('Charmander', 4, 'This pokemon has a firey tail!', 1, ['fire','fire'],\
                                  [1.8,1.04,0.86,1.2,1,1.3],{}, 20, 1.3,{16:'charmeleon'})
        self.charmeleon = pokemon('Charmeleon',5,'This pokemon is very aggressive!',1,['fire','fire'],\
                                  [2.26,1.28,1.16,1.6,1.3,1.6],{},30,1.3,{36:'charizard'})
        self.charizard = pokemon('Charizard',6,'This pokemon flies over forests looking for small animals to scoop up',1,['fire','flying'],\
                                 [2.66,1.68,1.56,2.18,1.7,2.0],{},40,1.3,{0:0})
        self.squirtle = pokemon('Squirtle', 7, 'This pokemon likes to squirt water at people that get too close', 1, ['water','water'],\
                                [1.98,0.96,1.3,1,1.28,0.86],{}, 20, 1.3,{16:'wartortle'})
        self.wartortle = pokemon('Wartortle',8, 'This pokemon likes to withdraw into it\'s shell to avoid being hit',1,['water','water'],\
                                 [2.28,1.26,1.6,1.3,1.6,1.16],{},30,1.3,{36:'blastoise'})
        self.blastoise = pokemon('Blastoise',9, 'This pokemon can blast out water from the two cannons on it\'s back',1,['water','water'],\
                                 [2.68,1.66,2.0,1.7,2.1,1.56],{},40,1.3,{0:0})
        self.caterpie = pokemon('Caterpie',10,'This pokemon eats leaves until it\'s ready to enter a cocoon',1,['bug','bug'],\
                                [2.0,0.6,0.7,0.4,0.4,0.9],{},15,1.3,{7:'metapod'})
        self.metapod = pokemon('Metapod',11,'The outer shell of this pokemon is able to harden on command',1,['bug','bug'],\
                               [2.1,0.4,1.1,0.5,0.5,0.6],{},20,1.3,{10:'butterfree'})
        self.butterfree = pokemon('Butterfree',12,'This pokemon can put other pokemon to sleep with the spores from it\'s wings',1,['bug','flying'],\
                                  [2.3,0.9,1.0,1.8,1.6,1.4],{},30,1.3,{0:0})
        self.weedle = pokemon('Weedle',13,'This pokemon gives a painful sting from the stinger on it\'s head',1,['bug','poison'],\
                              [1.9,0.7,0.6,0.4,0.4,1.0],{},15,1.3,{7:'kakuna'})
        self.kakuna = pokemon('Kakuna',14, 'This pokemon it starting to form it\'s future powerful arm stingers',1,['bug','poison'],\
                              [2.0,0.5,1.0,0.5,0.5,0.7],{},20,1.3,{10:'beedrill'})
        self.beedrill = pokemon('Beedrill',15,'This pokemon hunts small insects and even some mammals with it\'s powerful sting',1,['bug','poison'],\
                                [2.4,1.8,0.8,0.9,1.6,1.5],{},30,1.3,{0:0})
        self.pidgey = pokemon('Pidgey',16,'This pokemon is very common in large cities where people feed them', 1, ['normal','flying'],\
                              [1.9,0.9,0.8,0.7,0.7,1.12], {}, 20, 1.3,{16:'pidgeotto'})
        self.pidgeotto = pokemon('Pidgeotto',17,'This pokemon can produce powerful gusts to blow away it\'s opponents',1,['normal','flying'],\
                                 [2.36,1.2,1.1,1,1,1.42],{},27,1.3,{25:'pidgeot'})
        self.pidgeot = pokemon('Pidgeot',18,'This pokemon has a long feather on it\'s head which it uses to attract a mate',1,['normal','flying'],\
                               [2.76,1.6,1.5,1.4,1.4,2.02],{},35,1.3,{0:0})
        self.ratata = pokemon('Ratata',19,'This pokemon has strong teeth, it has been known to chew through metal!', 1, ['normal','normal'],\
                              [1.7,1.12,0.7,0.5,0.7,1.44],{}, 20, 1.3, {12:'raticate'})
        self.raticate = pokemon('Raticate',19, 'This pokemon digs deep burrows which can sometimes cause damage to buildings',1,['normal','normal'],\
                                [2.2,1.62,1.2,1,1.4,1.94],{},25,1.3,{0:0})
pokedex = pokedex() #actually creates the pokedex
evos = []
for value in pokedex.__dict__.items():
    evos.append(value)

moveTree = {'Bulbasaur':{6:leechSeed},\
            'Ivysaur':{},\
            'Venusaur':{},\
            'Charmander':{6:ember},\
            'Charmeleon':{},\
            'Charizard':{},\
            'Squirtle':{6:bubble},\
            'Wartortle':{},\
            'Blastoise':{},\
            'Caterpie':{7:harden},\
            'Metapod':{7:harden},\
            'Butterfree':{10:confusion},\
            'Weedle':{5:tackle, 7:harden},\
            'Kakuna':{7:harden},\
            'Beedrill':{10:twinNeedle},\
            'Pidgey':{},\
            'Pidgeotto':{},\
            'Pidgeot':{},\
            'Ratata':{6:quickAttack},
            'Raticate':{},\
            }
