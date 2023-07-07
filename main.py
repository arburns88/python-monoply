'''
define globals (board, total properties, die, etc.)
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
max_houses = 32
max_hotels = 12

class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0
        self.cash = 1500
        self.properties = []
    def get_cash(self):
        return self.cash
    def get_name(self):
        return self.name
    def get_position(self):
        return self.position
    def buy(self, other):
        if self.cash >= other.get_cost():
            self.charge(other.get_cost())
            self.properties.append(other)
        else:
            return 'Cannot Afford'
    def charge(self, price):
        self.cash -= price
    def refund(self, price):
        self.cash += price
    def move(self, spaces):
        self.position += spaces
        


#class CPU extends Player

class Property:
    def __init__(self, name, color, cost, housecost, rent, house1, house2, house3, house4, hotel, mortgage):
        self.name = name
        self.cost = cost
        self.rent = rent
        #would have been nice to automate this but monopoly costs have no patterns for some reason :(
        self.housecost = housecost
        self.house1 = house1
        self.house2 = house2
        self.house3 = house3
        self.house4 = house4
        self.hotel = hotel
        self.color = color
        self.mortgage = mortgage
        self.mortgaged = False
        self.buildings = 0
        self.status = 'unowned'
        self.owner = 'none'
        board.append(self)
    def __str__(self):
        if self.status == 'unowned':
            return f'{self.name}. It is unowned.'
        else:  
            if self.mortgaged is True:
                return f'{self.name}. Owned by {self.owner}. Mortgaged.'
            else:
                return f'{self.name}. Owned by {self.owner}. Rent with {self.buildings} buildings is {self.rent}.'
    def get_name(self):
        return self.name
    def get_status(self):
        return self.status
    def get_cost(self):
        return self.cost
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

def dice_roll():
    #dice1 = random.randrange(1, 6)
    #dice2 = random.randrange(1, 6)
    dice1 = 1
    dice2 = 1
    return dice1, dice2

if __name__ == '__main__':
    # BOARD SETUP
    Property('Mediterranean_Avenue', 'brown', 60, 50, 2, 10, 30, 90, 160, 250, 30)
    Property('Baltic Avenue', 'brown', 60, 50, 4, 20, 60, 180, 320, 450, 30)
    Property('Oriental Avenue', 'light blue', 100, 50, 6, 30, 90, 270, 400, 550, 50)
    Property('Vermont Avenue', 'light blue', 100, 50, 6, 30, 90, 270, 400, 550, 50)
    Property('Conneticut Avenue', 'light blue', 120, 50, 8, 40, 100, 300, 450, 600, 60)
    Property('St. Charles Place', 'magenta', 140, 100, 10, 50, 150, 450, 625, 750, 70)
    Property('States Avenue', 'magenta', 140, 100, 10, 50, 150, 450, 625, 750, 70)
    Property('Virginia Avenue', 'magenta', 160, 100, 12, 60, 180, 500, 700, 900, 80)
    print(board)

    # GAME SETUP
    num_players = int(input('Enter number of players: '))
    if 0 > num_players > 6:                                             # doesnt work?
        print('Error: please enter a mumber between 1 and 6 ')
        num_players = int(input('Re-enter number of players: '))
    for i in range(num_players):
        player_name = str(input(f'Player {i + 1}, enter your name: '))
        players.append(Player(player_name))
    
    # GAME LOGIC
    for i in players:
        play = True
        print(f"{i.get_name()} is up.")
        turns = 1
        while play is True:
            command = str(input(f'{i.get_name()}, what would you like to do: ')).lower()
            if command == 'roll':
                die1, die2 = dice_roll()
                roll = die1 + die2
                # Logic for rolling doubles
                if die1 == die2 and turns < 3:
                    print(f'Wow! You rolled two {die1}s. You will move {roll} spaces and get amother turn!')
                elif die1 == die2 and turns >= 3:
                    print('Uh Oh! You rolled 3 doubles in a row. You will go to jail for speeding.')
                    #go to jail
                    play = False
                    break
                else:
                    print(f'You rolled a {die1} and a {die2}, and will move {roll} spaces.')
                    play = False
                i.move(roll)
                current_space = board[i.get_position()]            # Equal to the property object
                if current_space.get_status() == 'unowned':
                    to_buy = str(input(f'You landed on {current_space} Would you like to buy it for {current_space.get_cost()}M? ')).lower()
                    if to_buy == 'yes':
                        i.buy(current_space)
                        print(f'You have successfully purchased {current_space.get_name()}. Remaining balance is: {i.get_cash()}M')
                turns += 1
                # end of playable turn
            else:
                print(f"'{command}' is not a registered command")
        print(turns)
