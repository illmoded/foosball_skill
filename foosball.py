import trueskill


class Player(trueskill.Rating):
    def __init__(self, name=None, n_games = 0):
        super().__init__()
        self.name = name
        self.n_games = n_games


    def __str__(self):
        return "{}'s score is {} with {} games".format(self.name, self.mu, self.n_games)


class Team:
    def __init__(self, player1, player2):
        if player1 is player2:
            print('wtf') # raise
        pass


class Match:
    pass


if __name__ == '__main__':
    a = Player('A')
    b = Player('B')
    c = Player('C')
    d = Player('D')

    players = [a, b, c, d]

    for player in players:
        print(player)

    team1 = Team(a, a)
    print(team1)
