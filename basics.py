"""
Script uses trueskill algorithm to determine player score when playing foosball
"""

from trueskill import Rating, rate, quality

def main():
    a, b = Rating(25), Rating(30)

    c = Rating()
    d = Rating()
    for i in range(9):
        t1 = [a,b]
        t2 = [c,d]

        (a,b), (c, d) = rate([t1, t2], ranks=[0, 1])
        print(a,b,c,d)
        print(quality([t1,t2]))
        # print(c)

        # print(quality([[alice],[bob]]))
        # print(alice.mu, alice.sigma)
if __name__ == '__main__':
    main()