'''
TODO LIST:
    - finish board setup function
'''

import math
import random

players = []
dnu = [
    'GO', 'Mediterranean Avenue', 'Community Chest', 'Baltic Avenue', 
    'Income Tax', 'Reading Railroad', 'Oriental Avenue', 'Chance', 
    'Vermont Avenue', 'Conneticut Avenue', 'Jail', 'St. Charles Place', 
    'Electric Company', 'States Avenue', 'Virginia Avenue', 
    'Pennsylvania Railroad', 'St. James Place', 'Community Chest', 
    'Tennessee Avenue', 'New York Avenue', 'Free Parking', 'Kentucky Avenue',
    'Chance', 'Indiana Avenue', 'Illinois Avenue', 'B. & O. Railroad', 
    'Atantic Avenue', 'Ventor Avenue', 'Water Works', 'Marvin Gardens', 
    'Go To Jail', 'Pacific Avenue', 'North Carolina Avenue', 'Community Chest',
    'Pennsylvania Avenue', 'Short Line', 'Chance', 'Park Place', 'Luxury Tax', 
    'Boardwalk'
    ]
board = []
# lists for comparing when finsing space type
properties = [
    'Mediterranean Avenue', 'Baltic Avenue', 'Oriental Avenue', 
    'Vermont Avenue', 'Conneticut Avenue', 'St. Charles Place', 
    'States Avenue', 'Virginia Avenue', 'St. James Place', 
    'Tennessee Avenue', 'New York Avenue', 'Kentucky Avenue',
    'Indiana Avenue', 'Illinois Avenue', 'Atantic Avenue', 
    'Ventor Avenue', 'Marvin Gardens', 'Pacific Avenue', 
    'North Carolina Avenue', 'Pennsylvania Avenue', 'Park Place', 
    'Boardwalk'
    ]
railroads = ['Reading Railroad', 'Pennsylvania Railroad', 'B. & O. Railroad', 'Short Line']
utilities = ['Electric Company', 'Water Works']
# Decks and Discards
chance_deck = [
    'Advance to Boardwalk', 'Advance to Go', 'Advance to Illinois Avenue', 'Advance to St. Charles Place', 'Advance to the nearest Railroad',
    'Advance to the nearest Railroad', 'Advance to nearest Utility', 'Bank pays you dividend of $50', 'Get Out of Jail Free', 'Go Back 3 Spaces'
    'Go to Jail', 'Make general repairs on all your property. For each house pay $25. For each hotel pay $100', 'Speeding fine $15', 
    'Take a trip to Reading Railroad', 'Elected Chairman of the Board. Pay each player $50', 'Your building loan matures. Collect $150'
]
chance_discard = []
community_chest_deck = [
    'Advance to Go', 'Bank error in your favor', 'Doctors fee', 'sale of stock', 'Get Out of Jail Free', 'Go to Jail', 'Holiday fund matures',
    'Income tax refund', 'It is your birthday', 'Life insurance matures', 'Pay hospital fees', 'Pay school fees', 'Receive $25 consultancy fee',
    'You are assessed for street repair', 'You have won second prize in a beauty contest', 'You inherit'
]
community_chest_discard = []

max_houses = 32
max_hotels = 12

#FIXME: class User extends Player
class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0
        self.cash = 1500
        self.properties = []
        self.inJail = False
        self.jailCards = 0
    # Getters
    def get_cash(self):
        return self.cash
    def get_name(self):
        return self.name
    def get_position(self):
        return self.position
    def get_properties(self):
        return self.properties
    def get_distance(self, findSpace):
        try:
            findIndex = board.index(findSpace)
            currentIndex = board.index(self.position)
            distance = (currentIndex - findIndex) % len(board)
            return min(distance, len(board) - distance)
        except ValueError:
            print('get_distance failed')
        # for i in range(40):
        #     checkSpace = board[self.position % i]
        #     if findSpace == 'Railroad' and 'Railroad' in checkSpace.get_name():
        #         if i != 0:
        #             break
        #     if findSpace == 'Utility' and (checkSpace == 'Electric Company' or board[self.position + i] == 'Water Works'):
        #         if i != 0:
        #             break
        #     if findSpace == board[self.position + i]:
        #         if i != 0:
        #             break
        #     distance += 1
    # Modifiers
    def buy(self, other):
        self.charge(other.get_cost())
        self.properties.append(other)
    def charge(self, amount):
        self.cash -= amount
    def fund(self, amount):
        self.cash += amount
    def pay(self, other, amount):
        self.cash -= amount
        other.cash += amount
    def move(self, spaces):
        self.position += spaces
        if self.position >= 40:
            self.position -= 40
            self.fund(200)
    def advance(self, Space):
        distance = self.get_distance(Space)
        self.move(distance)
    def go_to_jail(self):
        self.position = 10
        self.inJail = True
    def add_jail_card(self):
        self.jailCards += 1
    def repairs(self, house, hotels):
        cost = 0
        for property in self.properties:
            buildings = property.get_buildings()
            if buildings < 5:
                cost += (house * buildings)
            elif buildings == 5:
                cost += hotels
        self.cash -= cost

        
#FIXME: class CPU extends Player

class Tile:
    def __init__(self, name, cost, rent, mortgage, mortgaged = False, status = 'unowned', owner = 'none'):
        self.name = name
        self.cost = cost
        self.rent = rent
        self.mortgage = mortgage
        self.mortgaged = mortgaged
        self.status = status
        self.owner = owner
        board.append(self)
    def get_name(self):
        return self.name
    def get_status(self):
        return self.status
    def get_cost(self):
        return self.cost
    def get_owner(self):
        return self.owner

class Property(Tile):
    def __init__(self, name, color, cost, housecost, rent, house1, house2, house3, house4, hotel, mortgage, mortgaged = False, status = 'unowned', owner = 'none'):
        super().__init__(name, cost, rent, mortgage, mortgaged, status, owner)
        #would have been nice to automate this but monopoly costs have no patterns for some reason :(
        self.housecost = housecost
        self.house1 = house1
        self.house2 = house2
        self.house3 = house3
        self.house4 = house4
        self.hotel = hotel
        self.color = color
        self.buildings = 0
    def __str__(self):
        return self.name
    def getBuildings(self):
        return self.buildings
    def build(self, other, house_max, hotel_max):
        if self.buildings < 5:
            if other.get_cash() >= self.housecost:
                other.charge(self.housecost)
                self.buildings += 1
                if self.buildings < 4:
                    house_max -= 1
                    return f'Added 1 house to {self.name}. {self.name} has {self.buildings} houses.'
                else:
                    hotel_max -= 1
                    house_max += 4
                    return f'Added a hotel to {self.name}. {self.name} has {self.buildings} .'
        else:
            return 'Max houses reached'
    def destroy(self, other, house_max, hotel_max):
        other.cash += 0.5 * (self.housecost)
        self.buildings -= 1
        if self.buildings == 5:
            hotel_max += 1
        else:
            house_max += 1

#FIXME: class Utility extends Space
class Utility(Tile):
    def __init__(self, name, cost, mortgage, mortgaged = False, status = 'unowned', owner = 'none'):
        super().__init__(name, cost, mortgage, mortgaged, status, owner)
    def get_rent(self, player, other, roll):
        if self.name == 'Electric Company':
            other = 'Water Works'
        else: 
            other = 'Electric Company'
        if other in player.get_properties():
            rent = roll * 10
        else:
            rent = roll * 4
        return rent
    
#FIXME: class Railroad extends Tile
class Railroad(Tile):
    def __init__(self, name, cost, mortgage, mortgaged = False, status = 'unowned', owner = 'none'):
        super().__init__(name, cost, mortgage, mortgaged, status, owner)
    def get_rent(self, player):
            # Workaround for if/in statement including self railroad.
        rent = 25
        for property in player.get_properties:
            if 'Railroad' in property:
                rent *= 2
        return rent

# doesnt really need to be a class, but will shorten the code in the draw function
class Chance:
    def __init__(self):
        board.append(self)
    def __str__(self):
        return 'Chance'
    def draw(self):
        card = chance_deck[random.randint(0, 15)]
        print(f'You drew: {card}')
        if 'Advance to' in card:
            if 'nearest' in card:
                location = card.replace('Advance to the nearest ', '')
            else:
                location = card.replace('Advance to ', '')
            player.advance(location)
        elif card == 'Get Out of Jail Free':
            player.add_jail_card()
        elif card == 'Go Back 3 Spaces':
            player.move(-3)
        elif card == 'Go to Jail':
            player.go_to_jail()
        elif card == 'Make general repairs on all your property. For each house pay $25. For each hotel pay $100':
            player.repairs(25, 100)
        elif card == 'Speeding fine $15':
            player.charge(15)
        elif card == 'Take a trip to Reading Railroad':
            player.advance('Reading Railroad')
        elif card == 'Elected Chairman of the Board. Pay each player $50':
            for other_player in players:
                if other_player != player:
                    player.pay(other_player, 50)
        elif card == 'Your building loan matures. Collect $150':
            player.fund(150)
        else:
            print(f'Chance failed... Card name [{card}] not recognized')
        chance_deck.remove(card)
        chance_discard.append(card)
    
class CommunityChest:
    def __init__(self):
        board.append(self)

class Special:
    def __init__(self, name):
        self.name = name
        board.append(self)

# FUNCTIONS

def set_board():
    Special('GO')
    Property('Mediterranean_Avenue', 'brown', 60, 50, 2, 10, 30, 90, 160, 250, 30)
    board.append('Community Chest')
    Property('Baltic Avenue', 'brown', 60, 50, 4, 20, 60, 180, 320, 450, 30)
    Special('Income Tax')
    Railroad('Reading Railroad', 200, 100)
    Property('Oriental Avenue', 'light blue', 100, 50, 6, 30, 90, 270, 400, 550, 50)
    Chance()
    Property('Vermont Avenue', 'light blue', 100, 50, 6, 30, 90, 270, 400, 550, 50)
    Property('Conneticut Avenue', 'light blue', 120, 50, 8, 40, 100, 300, 450, 600, 60)
    Special('Jail')
    Property('St. Charles Place', 'magenta', 140, 100, 10, 50, 150, 450, 625, 750, 70)
    Utility('Electric Company', 150, 0)
    Property('States Avenue', 'magenta', 140, 100, 10, 50, 150, 450, 625, 750, 70)
    Property('Virginia Avenue', 'magenta', 160, 100, 12, 60, 180, 500, 700, 900, 80)
    Railroad('Pennsylvania Railroad', 200, 100)
    Property('St. James Place', 'orange', 180, 100, 14, 70, 200, 550, 750, 950, 90)
    CommunityChest()
    Property('Tennessee Avenue', 'orange', 180, 100, 14, 70, 200, 550, 750, 950, 90)
    Property('New York Avenue', 'orange', 200, 100, 16, 80, 220, 600, 800, 1000, 100)
    Special('Free Parking')
    Property('Kentucky Avenue', 'red', 220, 150, 18, 90, 250, 700, 875, 1050, 110)
    Chance()
    Property('Indiana Avenue', 'red', 220, 150, 18, 90, 250, 700, 875, 1050, 110)
    Property('Illinois Avenue', 'red', 240, 150, 20, 100, 300, 750, 925, 1100, 120)
    Railroad('B&O Railroad', 200, 100)
    Property('Atlantic Avenue', 'yellow', 260, 150, 22, 110, 330, 800, 975, 1150, 130)
    Property('Ventnor Avenue', 'yellow', 260, 150, 22, 110, 330, 800, 975, 1150, 130)
    Utility('Water Works', 150, 75)
    Property('Marvin Gardens', 'yellow', 280, 150, 24, 120, 360, 850, 1025, 1200, 140)
    Special('Go To Jail')
    Property('Pacific Avenue', 'green', 300, 200, 26, 130, 390, 900, 1100, 1275, 150)
    Property('North Carolina Avenue', 'green', 300, 200, 26, 130, 390, 900, 1100, 1275, 150)
    CommunityChest()
    Property('Pennysylvania Avenue', 'green', 320, 200, 28, 150, 450, 1000, 1200, 1400, 160)
    Railroad('Short Line', 200, 100)
    Chance()
    Property('Park Place', 'blue', 350, 200, 35, 175, 500, 1100, 1300, 1500, 175)
    Special('Luxury Tax')
    Property('Boardwalk', 'blue', 400, 200, 50, 200, 600, 1400, 1700, 2000, 200)

def get_num_players():
    playercount = False
    # while loop to keep prompting until valid num players
    while playercount is False:
        num_players = int(input('Enter number of players: '))
        # error if input isnt 1-6
        if 0 < num_players < 7:
            playercount = True
        else:
            print('Error: please enter a mumber between 1 and 6')
    return playercount

def get_players():
    num_players = get_num_players()
    for i in range(num_players):
        player_name = str(input(f'Player {i + 1}, enter your name: '))
        players.append(Player(player_name))

def dice_roll(turns):
    #dice1 = random.randrange(1, 6)
    #dice2 = random.randrange(1, 6)
    die1 = 3
    die2 = 3
    roll = die1 + die2
    if die1 == die2 and turns < 3:
        print(f'Wow! You rolled two {die1}s. You will move {roll} spaces and get amother turn!')
    elif die1 == die2 and turns >= 3:
        print('Uh Oh! You rolled 3 doubles in a row. You will go to jail for speeding.')
        # FIXME: go to jail
    else:
        print(f'You rolled a {die1} and a {die2}, and will move {roll} spaces.')
    return roll


if __name__ == '__main__':
    # GAME SETUP
    print(
        '''
    Welcome to Python Monopoly.
    To play, enter the number of players you would like to play with.
    Enter CPU as the players name to make the player a bot.
    Once it is your turn, you will use a series of commands to play. 
    Type help to get the list of commands and their uses.
    Good luck and hanve fun!
        '''
    )
    set_board()
    get_players()
    
    # GAME LOGIC
    for player in players:
        # stops asking for commands when false (ends turn) *ONLY AT END OF COMMAND*
        play = True
        # used for deciding if a player can roll
        rolled = False
        print(f"{player.get_name()} is up.")
        turns = 1
        while play is True:
            command = str(input(f'{player.get_name()}, what would you like to do: ')).lower()

            if command == 'help':
                print(
                    '''
    Here is a list of commands: 

        help: thats me! help displays all available commands

        roll: rolls the dice

        distance: tells you your distance from andy given space

        info: gives you all important information on a property
                    '''
                    )
                
            elif command == 'roll':
                if rolled is False and turns <= 3:
                        ### DIE LOGIC ###
                    roll = dice_roll(turns)
                        ### TURN LOGIC ###
                    if turns != 3:
                        player.move(roll)
                        current_space = board[player.get_position()]            # Equal to the item in the list
                        print(f'You landed on: {current_space}.')
                        if type(current_space) == Chance:
                            current_space.draw()
                        if type(current_space) == Property:
                            # FIXME: add property is owned
                            if current_space.get_status() == 'unowned':
                                print(f'{current_space} is unowned.')
                                if player.get_cash() < current_space.get_cost():
                                    print('Uh oh! Looks like you cant afford this space. It will go to auction')
                                    #FIXME add auction function
                                else:
                                    bought = False
                                    while not bought:
                                        to_buy = str(input(f'Would you like to buy {current_space} for {current_space.get_cost()}M? Your current balance is {player.get_cash()}M. ')).lower()
                                        if to_buy == 'yes':
                                            player.buy(current_space)
                                            print(f'You have successfully purchased {current_space.get_name()}. Remaining balance is: {player.get_cash()}M.')
                                            bought = True
                                        else:
                                            print("Please enter yes/no.")
                        turns += 1
                else:
                    print("Looks like youve already rolled. If youre ready to end your turn, use end.")

            #  FIXME: elif command == 'distance'        #return number of spaces from specified space

            #  FIXME: elif command == 'money'        #returns player money

            elif command == 'end':
                play = False

            elif command == 'kill':
                exit()

            elif command == 'balance':
                print(f'You have ${player.get_cash()}M.')

            else:
                print(f"'{command}' is not a registered command.")

        print(turns)
        #end of player turn
