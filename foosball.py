import trueskill
from exceptions import *


class Player(trueskill.Rating):
    def __init__(self, name=None, n_games=0):
        super().__init__()
        self.name = name
        self.n_games = n_games
        self.rank = self.mu

    def __str__(self):
        return self.name

    def print_info(self):
        return "{}'s rating is {}".format(self.name, self.mu)


class Team:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

        if player1 is player2:
            raise SamePlayerException('Players have to be different!')

    def __str__(self):
        return 'Team is composed of {} and {}'.format(self.player1, self.player2)


class Match:

    def __init__(self, team1, team2, winner=None):
        self.team1 = team1
        self.team2 = team2

        if team1 is team2:
            raise SameTeamException('Teams have to be different')

        self.winner = winner
        if self.winner is not None:
            try:
                self.make_win(self.winner)
            except WinnerException:
                print('Pick correct winner')
            

    def make_win(self, winner):
        if winner != self.team1 or winner != self.team2:
            raise WinnerException('Winner has to be one of ')
        else:
            if winner == self.team1:
                ranks = [0, 1]
            else:
                ranks = [1, 0]

            (self.team1.player1, self.team1.player2) = trueskill.rate([self.team1, self.team2], ranks=ranks)


if __name__ == '__main__':
    a = Player('A')
    b = Player('B')
    c = Player('C')
    d = Player('D')

    players = [a, b, c, d]

    for player in players:
        print(player)
        print(player.rank)

    team1 = Team(a, b)
    print(team1.player1)
