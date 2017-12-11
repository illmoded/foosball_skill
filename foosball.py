"""
Script for rating foosball players
"""

import json
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import trueskill

from exceptions import *

env = trueskill.TrueSkill()


class Player:

    @property
    def rank(self):
        return self.rating.mu

    def __init__(self, name):
        self.rating = env.create_rating()
        self.name = name
        self.filename = './data/' + self.name + '.json'
        self.read()

    def __str__(self):
        return 'PLAYER {} RATING {}'.format(self.name, self.rank)

    def __repr__(self):
        return self.__str__()  # todo: fix this

    def read(self):
        try:
            data = []
            with open(self.filename) as f:
                for line in f:
                    data.append(json.loads(line))

            last = data[-1]

            self.name = last['name']
            self.rating = env.create_rating(mu=last['mu'], sigma=last['sigma'])
        except FileNotFoundError:
            print('Creating player: {}'.format(self.name))
            self.save()

    def save(self):
        with open(self.filename, 'a') as f:
            json.dump({'name': self.name, 'mu': self.rank, 'sigma': self.rating.sigma, 'time': str(datetime.now())},
                      f, ensure_ascii=False)
            f.write('\n')

    def __eq__(self, other):
        return self.rating.mu == other.rating.mu

    def __gt__(self, other):
        return self.rating.mu > other.rating.mu

    def __lt__(self, other):
        return self.rating.mu < other.rating.mu


class Team:
    def __init__(self, player1, player2, name=None):
        self.player1 = player1
        self.player2 = player2
        self.name = name
        self.make_dict()

        if player1 is player2:
            raise SamePlayerException('Players have to be different!')

    def __str__(self):
        return '"{}: {} and {}"'.format(self.name, self.player1.rating.mu, self.player2.rating.mu)

    def make_dict(self):
        self.data = {self.player1: self.player1.rating, self.player2: self.player2.rating}


class Game:

    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.team1_data = self.team1.data
        self.team2_data = self.team2.data

    def rate_teams(self, winner):
        self.winner = winner.data
        if self.winner is self.team1_data:
            ranks = [0, 1]
        elif self.winner is self.team2_data:
            ranks = [1, 0]
        else:
            print('wtf')
            return 0

        rating_groups = self.team1_data, self.team2_data
        self.rated_rating_groups = env.rate(rating_groups, ranks=ranks)

        for team in rating_groups:
            idx = rating_groups.index(team)
            for player in team:
                player.rating = self.rated_rating_groups[idx][player]
                player.save()

        self.update_teams()

    def update_teams(self):
        self.team1.make_dict()
        self.team2.make_dict()
        self.__init__(self.team1, self.team2)  # todo: :(

    def print_ratings(self):
        print(self.team1.player1)
        print(self.team1.player2)
        print(self.team2.player1)
        print(self.team2.player2)


def errorfill(x, y, yerr, color=None, alpha_fill=0.3, ax=None):  # todo: find sth better
    x = np.array(x)
    y = np.array(y)
    yerr = np.array(yerr)
    ax = ax if ax is not None else plt.gca()
    if np.isscalar(yerr) or len(yerr) == len(y):
        ymin = y - yerr
        ymax = y + yerr
        base_line, = ax.plot(x, y, color=color)
    if color is None:
        color = base_line.get_color()
    ax.fill_between(x, ymax, ymin, facecolor=color, alpha=alpha_fill)


class Foosball:

    def __init__(self):
        self.files = []
        self.players = {}
        self.teams = {}
        self.player_names = []
        self.check_player_files()
        self.add_players_from_files()

    def check_player_files(self):
        files = []
        for file in os.listdir("./data"):
            if file.endswith(".json"):
                files.append(file.rstrip('.json'))
        self.files = files

    def add(self, name):
        self.players[name] = Player(name)
        self.players[name].read()
        if name not in self.player_names:
            self.player_names.append(name)

    def add_players_from_files(self):

        for player_name in self.files:
            self.player_names.append(player_name)

        if self.player_names is not None:
            for player_name in self.player_names:
                if player_name in self.files:
                    self.add(player_name)

    def add_player_from_input(self, player_name):
        if player_name not in self.player_names:
            self.add(player_name)
        else:
            print('Player name taken!')

    def add_team(self, player1_name, player2_name, team_name):
        player1 = self.players[player1_name]
        player2 = self.players[player2_name]

        team = Team(player1, player2, team_name)
        self.teams[team_name] = team
        # todo: now same player can be in different teams

    def play(self, team1_name, team2_name):
        team1 = self.teams[team1_name]
        team2 = self.teams[team2_name]

        self.game = Game(team1, team2)
        winner_name = input("Type winning team name. \n")
        winner = self.teams[winner_name]
        self.game.rate_teams(winner=winner)

    def print_players(self):
        for player in self.player_names:
            print(player)

    def print_teams(self):
        for team in self.teams:
            print(team)

    def print_ratings(self):
        print(sorted(self.players.values()))


def main():
    f = Foosball()

    print('Adding players!')
    inp = 'FOOSBALL INPUT'
    while True:
        print('Players:')
        f.print_players()
        inp = input('Type new player name.\nType X to move to TEAMS\n')
        if inp == 'X':
            break
        f.add_player_from_input(inp)

    inp = 'FOOSBALL INPUT'
    print('Adding teams!')

    while True:
        print('Teams:')
        f.print_teams()
        inp = input('X to skip adding and ove to PLAY')
        if inp == 'X':
            break
        team_name = input('Type new team name.\n')
        player1_name = input('Type name of 1st player.\n')
        player2_name = input('Type name of 2nd player.\n')

        f.add_team(player1_name,player2_name,team_name)

    inp = 'FOOSBALL INPUT'
    print('Finally playing!')
    while True:
        team1_name = input('TEAM 1 NAME\n')
        team2_name = input('TEAM 2 NAME\n')
        f.play(team1_name, team2_name)

        if inp == 'X':
            break

    f.print_ratings()


if __name__ == '__main__':
    main()
