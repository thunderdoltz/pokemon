from random import *
import os

global clearVar
syst = os.name
if syst == 'nt':
    clearVar = "cls"
else:
    clearVar = "clear"

def typeChart(defendType, attackType):
    base = 1
    noEffect = 0
    notVeryEffective = 0.5
    superEffective = 2
    types = {'normal':{'fighting':superEffective, 'ghost':noEffect},\
             'fighting':{'flying':superEffective,'rock':notVeryEffective,'bug':notVeryEffective,'psychic':superEffective},\
             'flying':{'fighting':notVeryEffective,'ground':noEffect,'rock':superEffective,'bug':notVeryEffective,'grass':notVeryEffective, 'electric':superEffective, 'ice':superEffective},\
             'poison':{'fighting':notVeryEffective, 'poison':notVeryEffective, 'ground':superEffective,'bug':superEffective,'grass':notVeryEffective, 'psychic':superEffective},\
             'ground':{'poison':notVeryEffective, 'rock':notVeryEffective, 'water':superEffective, 'grass':superEffective, 'electric':noEffect, 'ice':superEffective},\
             'rock':{'normal':notVeryEffective, 'fighting':superEffective, 'flying':notVeryEffective, 'poison':notVeryEffective, 'ground':superEffective, 'fire':notVeryEffective, 'water':superEffective, 'grass':superEffective},\
             'bug':{'fighting':notVeryEffective, 'flying':superEffective, 'poison':superEffective, 'ground':notVeryEffective, 'rock':superEffective, 'fire':superEffective, 'grass':notVeryEffective},\
             'ghost':{'normal':noEffect, 'fighting':noEffect, 'poison':notVeryEffective, 'bug':notVeryEffective, 'ghost':superEffective},\
             'fire':{'ground':superEffective, 'rock':superEffective, 'bug':notVeryEffective, 'fire':notVeryEffective, 'water':superEffective, 'grass':notVeryEffective},\
             'water':{'fire':notVeryEffective, 'water':notVeryEffective, 'grass':superEffective, 'electric':superEffective, 'ice':notVeryEffective},\
             'grass':{'flying':superEffective, 'poison':superEffective, 'ground':notVeryEffective, 'bug':superEffective, 'fire':superEffective, 'water':notVeryEffective, 'grass':notVeryEffective, 'electric':notVeryEffective, 'ice':superEffective},\
             'electric':{'flying':notVeryEffective, 'ground':superEffective, 'electric':notVeryEffective},\
             'psychic':{'fighting':notVeryEffective, 'bug':superEffective, 'ghost':noEffect, 'psychic':notVeryEffective},\
             'ice':{'fighting':superEffective, 'rock':superEffective, 'fire':superEffective, 'ice':notVeryEffective},\
             'dragon':{'fire':notVeryEffective, 'water':notVeryEffective, 'grass':notVeryEffective, 'electric':notVeryEffective, 'ice':superEffective, 'dragon':superEffective}}
    if attackType in types[defendType]:
        return types[defendType][attackType]
    else:
        return base
    
def printChart():
    types = ['normal','fighting','flying','poison','ground','rock','bug','ghost','fire','water','grass','electric','psychic','ice','dragon']
    print('      ', end = ' ')
    for poke in types:
        spacing = 8 - len(poke)
        if poke == 'dragon':
            print(poke)
        else:
            print(poke+' '*spacing, end = " ")
    for poke in types:
        spacing = 8 - len(poke)
        print(poke+' '*spacing, end = "")
        for poke1 in types:
            x = typeChart(poke1, poke)
            digSpace = 4 - len(str(x))
            if poke1 == 'dragon':
                print('   ',x,' '*digSpace)
            else:
                print('   ',x,' '*digSpace, end ="")
        

def typeMod(damageType, attackerType, defenderType):
    """
    returns the damage multiplier based on attack type, attacker type, and defender type
    damage type; string
    attacker type; list of two strings
    defender type; list of two strings
    """
    base = 1
    if damageType in attackerType:
        base *= 1.5
    effectiveMod = typeChart(defenderType[0], damageType)
    if defenderType[0] != defenderType[1]:
        effMod2 = typeChart(defenderType[1], damageType)
        effectiveMod *= effMod2
    if effectiveMod > 1:
        print('It\'s super effective!')
    elif effectiveMod == 0:
        print('It had no effect!')
    elif effectiveMod <1 and effectiveMod>0:
        print('it wasn\'t very effective...')
    base *= effectiveMod
    return base

def battleDisplay(playerPoke, opponentPoke):
    """
    Will display sprites and HP bars
    """
    print(str(opponentPoke.name),str(opponentPoke.level), 'HP:'+opponentPoke.HPBar(),str(opponentPoke.HP)+'/'+str(opponentPoke.maxHP))
    print(str(playerPoke.name),str(playerPoke.level), 'HP:'+playerPoke.HPBar(),str(playerPoke.HP)+'/'+str(playerPoke.maxHP))

def hit(percent):
    didHit = randint(1,100)
    if didHit <= percent:
        return True
    else:
        return False

def damage(attacker, defender, power, attackStat, defenseStat):
    a = (2*attacker.level)/5+2
    b = power*attacker.tempStats[attackStat]/defender.tempStats[defenseStat]
    c = a*b/50+2
    return c

def statusCheck(target):
    exclusiveStatus = ['paralyzed','sleep','poison','frozen','burn']
    if len(target.status) == 0:
        return True
    else:
        for oneStatus in target.status:
            if oneStatus in exclusiveStatus:
                return False
        return True
    
    
def scratchAttack(attacker, defender, computer):
    """
    Main damage attack, right now all the other physical attacks are clones of this
    """
    damageType = 'normal'
    power = 40
    if hit(95) == True: #95% hit rate
        damageMod = typeMod(damageType, attacker.typ, defender.typ)
        damageDone = damage(attacker, defender, power, 'attack', 'defense')
        damageDone *= damageMod
        defender.damageTaken(round(damageDone))
    else:
        print('but it missed!')

def tailWhipAttack(attacker, defender, computer):
    """
    main defense damaging attack, right now all the other stat damage attacks are clones of this
    """
    if hit(95)==True:
        defender.statChange('defense', False)
    else:
        print('but it missed!')

def tackleAttack(attacker, defender, computer):
    damageType = 'normal'
    power = 40
    if hit(95) == True: #95% hit rate
        damageMod = typeMod(damageType, attacker.typ, defender.typ)
        damageDone = damage(attacker, defender, power, 'attack', 'defense')
        damageDone *= damageMod
        defender.damageTaken(round(damageDone))
    else:
        print('but it missed!')

def leerAttack(attacker, defender, computer):
    if hit(95)==True:
        defender.statChange('defense', False)
    else:
        print('but it failed!')

def wingAttackAttack(attacker, defender, computer):
    damageType = 'normal'
    power = 40
    if hit(95) == True: #95% hit rate
        damageMod = typeMod(damageType, attacker.typ, defender.typ)
        damageDone = damage(attacker, defender, power, 'attack', 'defense')
        damageDone *= damageMod
        defender.damageTaken(round(damageDone))
    else:
        print('but it missed!')

def gustAttack(attacker, defender, computer):
    power = 40
    damageType = 'flying'
    if hit(95)==True: #95% hit rate
        damageMod = typeMod(damageType, attacker.typ, defender.typ)
        damageDone = damage(attacker, defender, power,'attack','defense')
        damageDone *= damageMod
        defender.damageTaken(round(damageDone))
    else:
        print('but it missed!')

def bubbleAttack(attacker, defender, computer):
    damageType = 'water'
    power = 40
    if hit(95) == True:
        if randint(1,10) == 5:
            defender.statChange('speed', False)
        damageMod = typeMod(damageType, attacker.typ, defender.typ)
        damageDone = damage(attacker, defender, power,'sp.attack','sp.defense')
        damageDone *= damageMod
        defender.damageTaken(round(damageDone))
    else:
        print('but it missed!')
        
def emberAttack(attacker, defender, computer):
    damageType = 'fire'
    power = 40
    if hit(95) == True:
        if statusCheck(defender):
            if randint(1,10) == 5:
                defender.status.append('burn')
                print(defender.name,'was burned!')
        damageMod = typeMod(damageType, attacker.typ, defender.typ)
        damageDone = damage(attacker, defender, power, 'sp.attack','sp.defense')
        damageDone *= damageMod
        defender.damageTaken(round(damageDone))
    else:
        print('but it missed!')

def leechSeedAttack(attacker, defender, computer):
    damageType = 'grass'
    if 'grass' in defender.typ:
        print(defender.name,'was not affected')
    else:
        if 'leech' not in defender.status:
            print(defender.name,'was seeded')
            defender.status.append('leech')
        else:
            print('There was no effect')

def quickAttackAttack(attacker, defender, computer):
    damageType = 'normal'
    power = 40
    if hit(95) == True:
        damageMod = typeMod(damageType, attacker.typ, defender.typ)
        damageDone = damage(attacker, defender, power, 'attack','defense')
        damageDone *= damageMod
        defender.damageTaken(round(damageDone))
    else:
        print('but it missed!')

def poisonStingAttack(attacker, defender, computer):
    damageType = 'poison'
    power = 40
    if hit(95) == True:
        damageMod = typeMod(damageType, attacker.typ, defender.typ)
        if damageMod != 0 and statusCheck(defender):
            if randint(1,10) == 5:
                defender.status.append('poison')
                print(defender.name,'was poisoned!')
            damageDone = damage(attacker, defender, power, 'attack', 'defense')
            damageDone *= damageMod
            defender.damageTaken(round(damageDone))
    else:
        print('but it missed!')

def stringShotAttack(attacker, defender, computer):
    if hit(95)==True:
        defender.statChange('speed', False)
    else:
        print('but it missed!')

def hardenAttack(attacker, defender, computer):
    attacker.statChange('defense',True)

def twinNeedleAttack(attacker, defender, computer):
    damageType = 'bug'
    power = 25
    input()
    for i in range(2):
        os.system(clearVar)
        if computer == True:
            battleDisplay(defender,attacker)
        else:
            battleDisplay(attacker,defender)
        if hit(95) == True:
            damageMod = typeMod(damageType, attacker.typ, defender.typ)
            if damageMod != 0:
                if i == 0:
                    print('first strike hit!')
                    input()
                if i == 1:
                    print('second strike hit!')
                if statusCheck(defender):
                    if randint(1,5) == 5:
                        defender.status.append('poison')
                        print(defender.name,'was poisoned!')
                damageMod = typeMod(damageType, attacker.typ, defender.typ)
                damageDone = damage(attacker, defender, power, 'attack', 'defense')
                damageDone*=damageMod
                defender.damageTaken(round(damageDone))
            
        else:
            if i == 0:
                print('first strike missed!')
                input()
            if i == 1:
                print('second strike missed!')

def confusionAttack(attacker, defender, computer):
    damageType = 'psychic'
    power = 50
    if hit(95) == True:
        if 'confusion' not in defender.status:
            if randint(1,10) == 5:
                defender.status.append('confusion')
                defender.timesAttacked = 0
                print(defender.name,'became confused!')
        damageMod = typeMod(damageType, attacker.typ, defender.typ)
        damageDone = damage(attacker, defender, power, 'sp.attack', 'sp.defense')
        damageDone*=damageMod
        defender.damageTaken(round(damageDone))
    else:
        print('but it missed!')

def thundershockAttack(attacker, defender, computer):
    damageType = 'electric'
    power = 40
    if hit(95) == True:
        damageMod = typeMod(damageType, attacker.typ, defender.typ)
        if damageMod != 0:
            if statusCheck(defender):
                if randint(1,10) == 5:
                    defender.status.append('paralyzed')
                    print(defender.name,'became paralyzed!')
            damageDone = damage(attacker, defender, power, 'sp.attack', 'sp.defense')
            damageDone*=damageMod
            defender.damageTaken(round(damageDone))
    else:
        print('but it missed!')

def defenseCurlAttack(attacker, defender, computer):
    attacker.statChange('defense',True)

def screechAttack(attacker, defender, computer):
    if hit(85)==True:
        for i in range(2):
            defender.statChange('defense', False)
    else:
        print('but it failed!')

def peckAttack(attacker, defender, computer):
    power = 35
    damageType = 'flying'
    if hit(95)==True: #95% hit rate
        damageMod = typeMod(damageType, attacker.typ, defender.typ)
        damageDone = damage(attacker, defender, power,'attack','defense')
        damageDone *= damageMod
        defender.damageTaken(round(damageDone))
    else:
        print('but it missed!')

def doubleKickAttack(attacker, defender, computer):
    damageType = 'fighting'
    power = 25
    input()
    for i in range(2):
        os.system(clearVar)
        if computer == True:
            battleDisplay(defender,attacker)
        else:
            battleDisplay(attacker,defender)
        if hit(95) == True:
            damageMod = typeMod(damageType, attacker.typ, defender.typ)
            if damageMod != 0:
                if i == 0:
                    print('first strike hit!')
                    input()
                if i == 1:
                    print('second strike hit!')
                damageMod = typeMod(damageType, attacker.typ, defender.typ)
                damageDone = damage(attacker, defender, power, 'attack', 'defense')
                damageDone*=damageMod
                defender.damageTaken(round(damageDone))
            
        else:
            if i == 0:
                print('first strike missed!')
                input()
            if i == 1:
                print('second strike missed!')

def hornAttackAttack(attacker, defender, computer):
    """
    Main damage attack, right now all the other physical attacks are clones of this
    """
    damageType = 'normal'
    power = 65
    if hit(95) == True: #95% hit rate
        damageMod = typeMod(damageType, attacker.typ, defender.typ)
        damageDone = damage(attacker, defender, power, 'attack', 'defense')
        damageDone *= damageMod
        defender.damageTaken(round(damageDone))
    else:
        print('but it missed!')

def swiftAttack(attacker, defender, computer):
    """
    Main damage attack, right now all the other physical attacks are clones of this
    """
    damageType = 'normal'
    power = 65
    damageMod = typeMod(damageType, attacker.typ, defender.typ)
    damageDone = damage(attacker, defender, power, 'attack', 'defense')
    damageDone *= damageMod
    defender.damageTaken(round(damageDone))

def furySwipesAttack(attacker, defender, computer):
    damageType = 'normal'
    power = 18
    hits = [2,2,2,3,3,3,4,5]
    noHits = choice(hits)
    input()
    if hit(85) == True:
        damageMod = typeMod(damageType, attacker.typ, defender.typ)
        for i in range(noHits):
            print(i,'hits!')
            os.system(clearVar)
            if computer == True:
                battleDisplay(defender,attacker)
            else:
                battleDisplay(attacker,defender)
            damageMod = typeMod(damageType, attacker.typ, defender.typ)
            damageDone = damage(attacker, defender, power, 'attack', 'defense')
            damageDone*=damageMod
            defender.damageTaken(round(damageDone))
            
    else:
        print('but it missed!')

def growlAttack(attacker, defender, computer):
    defender.statChange('attack',False)

def agilityAttack(attacker, defender, computer):
    for i in range(2):
        attacker.statChange('speed', True)

def rockThrowAttack(attacker, defender, computer):
    """
    Main damage attack, right now all the other physical attacks are clones of this
    """
    damageType = 'rock'
    power = 50
    if hit(90) == True: #95% hit rate
        damageMod = typeMod(damageType, attacker.typ, defender.typ)
        damageDone = damage(attacker, defender, power, 'attack', 'defense')
        damageDone *= damageMod
        defender.damageTaken(round(damageDone))
    else:
        print('but it missed!')

def takeDownAttack(attacker, defender, computer):
    """
    Main damage attack, right now all the other physical attacks are clones of this
    """
    damageType = 'normal'
    power = 90
    if hit(85) == True: #95% hit rate
        damageMod = typeMod(damageType, attacker.typ, defender.typ)
        damageDone = damage(attacker, defender, power, 'attack', 'defense')
        damageDone *= damageMod
        defender.damageTaken(round(damageDone))
        attacker.damageTaken(round(damageDone/4))
        print(attacker.name,'was hit with the recoil!')
    else:
        print('but it missed!')

def furyAttackAttack(attacker, defender, computer):
    damageType = 'normal'
    power = 15
    hits = [2,2,2,3,3,3,4,5]
    noHits = choice(hits)
    input()
    if hit(85) == True:
        damageMod = typeMod(damageType, attacker.typ, defender.typ)
        for i in range(noHits):
            print(i,'hits!')
            os.system(clearVar)
            if computer == True:
                battleDisplay(defender,attacker)
            else:
                battleDisplay(attacker,defender)
            damageMod = typeMod(damageType, attacker.typ, defender.typ)
            damageDone = damage(attacker, defender, power, 'attack', 'defense')
            damageDone*=damageMod
            defender.damageTaken(round(damageDone))
            
    else:
        print('but it missed!')

def acidAttack(attacker, defender, computer):
    damageType = 'poison'
    power = 40
    damageMod = typeMod(damageType, attacker.typ, defender.typ)
    if damageMod != 0:
        if hit(95) == True:
            if randint(1,10) == 5:
                defender.statChange('sp.defense', False)
            damageMod = typeMod(damageType, attacker.typ, defender.typ)
            damageDone = damage(attacker, defender, power,'sp.attack','sp.defense')
            damageDone *= damageMod
            defender.damageTaken(round(damageDone))
        else:
            print('but it missed!')

def biteAttack(attacker, defender, computer):
    """
    Main damage attack, right now all the other physical attacks are clones of this
    """
    damageType = 'normal'
    power = 60
    cantFlinch = ['sleep','frozen']
    flinch = True
    if hit(95) == True: #95% hit rate
        for thisStatus in defender.status:
            if thisStatus in cantFlinch:
                flinch = False
        if flinch:
            chance = [True, False, False]
            if choice(chance):
                defender.status.append('flinched')
        damageMod = typeMod(damageType, attacker.typ, defender.typ)
        damageDone = damage(attacker, defender, power, 'attack', 'defense')
        damageDone *= damageMod
        defender.damageTaken(round(damageDone))
    else:
        print('but it missed!')

def vineWhipAttack(attacker, defender, computer):
    """
    Main damage attack, right now all the other physical attacks are clones of this
    """
    damageType = 'grass'
    power = 45
    if hit(95) == True: #95% hit rate
        damageMod = typeMod(damageType, attacker.typ, defender.typ)
        damageDone = damage(attacker, defender, power, 'attack', 'defense')
        damageDone *= damageMod
        defender.damageTaken(round(damageDone))
    else:
        print('but it missed!')

def thunderWaveAttack(attacker, defender, computer):
    damageType = 'electric'
    damageMod = typeMod(damageType, attacker.typ, defender.typ)
    if damageMod != 0 and statusCheck(defender):
        print(defender.name,'was paralyzed!')
        defender.status.append('paralyzed')
    else:
        print('There was no effect')

def slashAttack(attacker, defender, computer):
    """
    Main damage attack, right now all the other physical attacks are clones of this
    """
    damageType = 'normal'
    power = 70
    if hit(95) == True: #95% hit rate
        damageMod = typeMod(damageType, attacker.typ, defender.typ)
        damageDone = damage(attacker, defender, power, 'attack', 'defense')
        damageDone *= damageMod
        defender.damageTaken(round(damageDone))
    else:
        print('but it missed!')

def bodySlamAttack(attacker, defender, computer):
    """
    Main damage attack, right now all the other physical attacks are clones of this
    """
    damageType = 'normal'
    power = 85
    if hit(95) == True: #95% hit rate
        if statusCheck(defender):
            if randint(1,3) == 3:
                defender.status.append('paralyzed')
        damageMod = typeMod(damageType, attacker.typ, defender.typ)
        damageDone = damage(attacker, defender, power, 'attack', 'defense')
        damageDone *= damageMod
        defender.damageTaken(round(damageDone))
    else:
        print('but it missed!')

def bideAttack(attacker, defender, computer):
    attacker.referenceHP = attacker.HP
    damageType = 'normal'
    attacker.status.append('bide')
    attacker.timesAttacked = 0
    print(attacker.name,'is biding their time')
        
class move:
    def __init__(self, name, priority, duration, technique):
        self.name = name
        self.priority = priority
        self.technique = technique
        self.duration = duration
        
    def useMove(self, attacker, defender, computer = False):
        print(attacker.name,'used',self.name+'!')
        return self.technique(attacker, defender, computer)
              
scratch = move('scratch',0,0,scratchAttack)
tackle = move('tackle',0,0,tackleAttack)
leer = move('leer',0,0,leerAttack)
tailWhip = move('tail whip',0,0,tailWhipAttack)
wingAttack = move('wing attack',0,0,wingAttackAttack)
gust = move('gust',0,0,gustAttack)
bubble = move('bubble',0,0,bubbleAttack)
ember = move('ember',0,0,emberAttack)
leechSeed = move('leech seed',0,0,leechSeedAttack)
quickAttack = move('quick attack',1,0,quickAttackAttack)
poisonSting = move('poison sting',0,0,poisonStingAttack)
stringShot = move('string shot',0,0,stringShotAttack)
harden = move('harden',0,0,hardenAttack)
twinNeedle = move('twin needle',0,0,twinNeedleAttack)
confusion = move('confusion',0,0,confusionAttack)
thundershock = move('thunder shock',0,0,thundershockAttack)
defenseCurl = move('defense curl',0,0,defenseCurlAttack)
screech = move('screech',0,0,screechAttack)
peck = move('peck',0,0,peckAttack)
doubleKick = move('double kick',0,0,doubleKickAttack)
hornAttack = move('horn attack',0,0,hornAttackAttack)
swift = move('swift',0,0,swiftAttack)
furySwipes = move('fury swipes',0,0,furySwipesAttack)
agility = move('agility',0,0,agilityAttack)
furyAttack = move('fury attack',0,0,furyAttackAttack)
rockThrow = move('rock throw',0,0,rockThrowAttack)
takeDown = move('take down',0,0,takeDownAttack)
acid = move('acid',0,0,acidAttack)
bite = move('bite',0,0,biteAttack)
vineWhip = move('vine whip',0,0,vineWhipAttack)
thunderWave = move('thunder wave',0,0,thunderWaveAttack)
slash = move('slash',0,0,slashAttack)
bodySlam = move('body slam',0,0,bodySlamAttack)
growl = move('growl',0,0,growlAttack)
bide = move('bide',0,0,bideAttack)



              



