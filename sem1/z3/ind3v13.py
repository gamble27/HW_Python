import numpy as np
from random import sample

class pref_deck:
    def __init__(self):
        v = []
        for i in range(7, 15):
            v.append(100 + i)
            v.append(200 + i)
            v.append(300 + i)
            v.append(400 + i)
        self.cards = np.array(v)
        del v

    def _shuffle(self):
        for i, j in zip(range(32), sample(range(32), 32)):
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]

    def shuffle(self):
        self._shuffle()
        hand1 = self.cards[:10]
        prikup = self.cards[10:12]
        hand2 = self.cards[12:22]
        hand3 = self.cards[22:]
        return (hand1, hand2, hand3, prikup)


def miser(hand):
    '''
    proverka na chistyu bez prikupa => 7ka - hozyaika

    :param hand: ndarray of length 10
    :return: 0 or 1 just like Boolean
    '''
    # if 107 or 207 or 307 or 407 not in hand:
    #     return False

    masti = np.array([[i%100 for i in hand if i//100 == j] for j in range(1,5)])
    for mast in masti:
        if (7 not in mast)and(len(mast)>0):
            return 0
        if len(mast)>=2 and (8 not in mast) and (9 not in mast):
            return 0
        if len(mast)>=3 and (9 not in mast) and (10 not in mast) and (11 not in mast):
            return 0
        if len(mast)>=4 and (10 not in mast) and (11 not in mast) and (12 not in mast) and (13 not in mast):
            return 0
    return 1

N = 1000

r = pref_deck()
M = 0

for i in range(N):
    hands = r.shuffle()
    pr = hands[3]
    M += miser(np.concatenate([hands[0], pr]))
    M += miser(np.concatenate([hands[1], pr]))
    M += miser(np.concatenate([hands[2], pr]))

print('{m}/{n}={k}'.format(m=M,n=N,k=M/N))