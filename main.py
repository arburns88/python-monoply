'''
define globals (board, total properties, die, etc.)
'''

import math
import random

players = []
board = [
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
        self.cash = 1500
        self.properties = []
    def get_cash(self):
        return self.cash
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
        


#class CPU extends Player

class Property:
    def __init__(self, name, cost, rent, color, mortgage):
        self.name = name
        self.cost = cost
        self.rent = rent
        self.color = color
        self.mortgage = mortgage
        self.mortgaged = False
        self.buildings = 0
        self.owner = 'none'
        self.cost_to_build = 50 * self.color
    def __str__(self):
        if self.mortgaged:
            return f'{self.name}. Owned by {self.owner}. Mortgaged'
        else:
            return f'{self.name}. Owned by {self.owner}. Rent with {self.buildings} buildings is {self.rent}.'
    def build(self, other):
        if other.get_cash() >= self.cost_to_build:
            other.charge(self.cost_to_build)
            self.buildings += 1
            max_houses -= 1
            if self.buildings == 1:
                if self.name != 'Boardwalk':
                    self.rent *= 5
                else:
                    self.rent *= 4
            elif self.buildings == 2:
                if self.color == 'brown' or self.color == 'light blue' or self.color == 'magenta':
                    self.rent *= 3
    def destroy(self, other):
        other.cash += 0.5 * (self.cost_to_build)
    def get_cost(self):
        return self.cost

def diceroll():
    dice1 = random.randrange(1, 6)
    dice2 = random.randrange(1, 6)
    return dice1, dice2

if __name__ == '__main__':
    num_players = int(input('Enter number of players: '))
    if 0 > num_players > 6:                                             # doesnt work?
        print('Error: please enter a mumber between 1 and 6 ')
        num_players = int(input('Re-enter number of players: '))
    for i in range(num_players):
        player_name = str(input(f'Player {i + 1}, enter your name: '))
        players.append(Player(player_name))
    
