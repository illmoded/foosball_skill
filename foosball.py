import trueskill
from exceptions import *


class Player(trueskill.Rating):

    @property
    def n_games(self):
        return self.n_games

    @property
    def rank(self):
        return self.mu

    def __init__(self, name=None, n_games=0):
        super().__init__()
        self.name = name
        self._n_games = n_games
        self._rank = self.rank

    def __str__(self):
        return self.name

    def print_info(self):
        print("{}'s rating is {:04.2f}".format(self.name, self._rank))
        return "{}'s rating is {:04.2f}".format(self.name, self._rank)


class Team:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

        if player1 is player2:
            raise SamePlayerException('Players have to be different!')

    def __str__(self):
        return '"{} and {}"'.format(self.player1, self.player2)


class Match:
    def __init__(self, team1, team2, winner=None):
        self.team1 = team1
        self.team2 = team2

        if team1 is team2:
            raise SameTeamException('Teams have to be different')

        self.winner = winner
        if self.winner is not None:
            self.make_win(self.winner)

    def rate(self, team1, team2, ranks):
        t1 = [team1.player1, team1.player2]
        t2 = [team2.player1, team2.player2]

        (t1p1, t1p2), (t2p1, t2p2) = trueskill.rate([t1, t2], ranks=ranks)
        team1.player1._rank = t1p1.mu
        # todo: update others
        # todo: fix saving, solve global variables

    def make_win(self, winner):
        if winner != self.team1 and winner != self.team2:
            raise WinnerException('Winner has to be one')
        else:
            if winner == self.team1:
                ranks = [0, 1]
            else:
                ranks = [1, 0]
            self.rate(self.team1, self.team2, ranks)

    def __str__(self):
        return "The winner of {} vs {} is {}".format(self.team1, self.team2, self.winner)


if __name__ == '__main__':
    a = Player('A')
    b = Player('B')
    c = Player('C')
    d = Player('D')

    team1 = Team(a, b)
    team2 = Team(c, d)

    match = Match(team1, team2, winner=team1)
    print(match)
    a.print_info()
    b.print_info()
    c.print_info()
    d.print_info()

    match = Match(team1, team2, winner=team2)
    print(match)
    a.print_info()
    b.print_info()
    c.print_info()
    d.print_info()
