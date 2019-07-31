import os
global clearVar
syst = os.name
if syst == 'nt':
    clearVar = "cls"
else:
    clearVar = "clear"
    
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

def menuSelect(ask, options):
    while True:
        i = 1
        for option in options:
            print(str(i)+'.',option)
            i+=1
        action = input()
        if menuValid(action, len(options)):
            action = int(action)
            return action

def potion(player, pokemon):
    if pokemon.HP == pokemon.maxHP:
        print('It won\'t have any effect!')
    else:
        print('used a potion on',pokemon.name+'!')
        pokemon.heal(20)
        player.itemList[2][1]-=1

def pokeball(player, opponentPoke): #fix this and potions
    player.itemList[1][1]-=1
    print('Threw a pokeball!')
    catch = player.catchPoke(opponentPoke)
    return catch
    
def itemShop(player):
    while True:
        os.system(clearVar)
        print('Welcome to the Pokemart!')
        print('You have',player.money,'credits')
        items = [['Pokeball',100],['Potion',50]]
        options = ['Pokeball','Potion','Cancel']
        action = menuSelect('What would you like to buy?', options)
        if action == len(options):
            print('Come back and see us again!')
            input()
            break
        elif player.money >= items[action-1][1]:
            player.money -= items[action-1][1]
            for item in player.itemList: #Have to make it so that it checks if item is in inventory already
                if items[action-1][0] == item[0]:
                    inInvent = True
                    player.itemList[action-1][1] += 1
                    break
                else:
                    inInvent = False
            if inInvent == False:
                player.itemList.append([items[action-1][0],1])
            print('one',items[action-1][0],'has been added to your inventory!')
            print('You now have',player.itemList[action-1][1],player.itemList[action-1][0]+'s')
            input()
        else:
            print('You don\'t have enough money!')
            input()
        

    
