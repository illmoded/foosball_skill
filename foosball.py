import trueskill
from exceptions import *

env = trueskill.TrueSkill()


class Player():

    @property
    def rank(self):
        return self.rating.mu

    def __init__(self, name):
        # todo: read from db -> add params to create_rating()
        self.rating = env.create_rating()
        self.name = name

    def __str__(self):
        return 'PLAYER {} RATING {}'.format(self.name, self.rank)


class Team:
    def __init__(self, player1, player2, name = None):
        self.player1 = player1
        self.player2 = player2
        self.name = name
        self.make_dict()

        if player1 is player2:
            raise SamePlayerException('Players have to be different!')

    def __str__(self):
        return '"{}: {} and {}"'.format(self.name ,self.player1.rating.mu, self.player2.rating.mu)

    def make_dict(self):
        self.data = {self.player1: self.player1.rating, self.player2: self.player2.rating}


class Game():

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
        # print(rating_groups)
        self.rated_rating_groups = env.rate(rating_groups, ranks=ranks)

        for team in rating_groups:
            idx = rating_groups.index(team)
            for player in team:
                player.rating = self.rated_rating_groups[idx][player]
        self.update_teams()

    def update_teams(self):
        self.team1.make_dict()
        self.team2.make_dict()
        self.__init__(self.team1, self.team2) # todo: FIXXXXXXXXX

    def print_ratings(self):
        print(team1.player1)
        print(team1.player2)
        print(team2.player1)
        print(team2.player2)


p1 = Player('1')
p2 = Player('2')
p3 = Player('3')
p4 = Player('4')

team1 = Team(p1, p2, name='t1')
team2 = Team(p3, p4, name= 't2')

game = Game(team1, team2)

for i in range(7):
    game.rate_teams(winner=team2)
    game.print_ratings()
