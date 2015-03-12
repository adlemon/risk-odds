# construct a list of all possible outcomes
X = range(1,7)
def nlists(X,n):
    if n == 0:
        return [[]]
    else:
        return [x + [y] for x in nlists(X,n-1) for y in X]
Z = {n:[sorted(x , reverse = True) for x in nlists(X,n)] for n in range(1,4)}

def cartesian_product(X,Y):
    return {(x,y) for x in X for y in Y}

def dictsum(X,Y):
    return {k:(X[k] if k in X else 0) + (Y[k] if k in Y else 0)
            for k in X.keys() | Y.keys()}
def dictscale(a,X):
    return {k:a*X[k] for k in X}

# compute the probabilities of outcomes for a single roll of the dice
P = {num_att:
        {num_def:
            {loss_att:0 for loss_att in range(3)}
            for num_def in range(1,3)}
        for num_att in range(1,4)}
for num_att in range(1,4):
    for num_def in range(1,3):
        p = 1 / (len(Z[num_att]) * len(Z[num_def]))
        for x_att in Z[num_att]:
            for x_def in Z[num_def]:
                loss_att = 0
                for i in range(min(num_att,num_def)):
                    if x_att[i] <= x_def[i]:
                        loss_att = loss_att + 1
                P[num_att][num_def][loss_att] = P[num_att][num_def][loss_att] + p

# compute the probabilities of outcomes for a fight to the death
NUM_ATT = eval(input("number of attackers: "))
NUM_DEF = eval(input("number of defenders: "))
Y = cartesian_product(set(range(num_att+1)) , set(range(num_def+1)))
Q = {num_att:
        {num_def:
            {att_left:0 for att_left in range(NUM_ATT+1)}
            for num_def in range(NUM_DEF+1)}
        for num_att in range(NUM_ATT+1)}
for num_att in range(NUM_ATT+1):
    Q[num_att][0][num_att] = 1
for num_def in range(NUM_DEF+1):
    Q[0][num_def][0] = 1
for NDICE in range(2,NUM_ATT+NUM_DEF+1):
    for num_att in range(max(NDICE-NUM_DEF,1),min(NDICE-1,NUM_ATT)+1):
        num_def = NDICE - num_att
        num_attd = min(num_att,3)
        num_defd = min(num_def,2)
        for loss_att in range(min(num_attd,num_defd)+1):
            loss_def = min(num_attd,num_defd) - loss_att
            Q[num_att][num_def] = \
                    dictsum(Q[num_att][num_def] ,
                            dictscale(P[num_attd][num_defd][loss_att] ,
                                      Q[num_att - loss_att][num_def - loss_def]))

print(" # | p == # | p <= # | p >= #")
print("===|========|========|=======")
F = 0
for k in range(NUM_ATT+1):
    F = F + Q[NUM_ATT][NUM_DEF][k]
    print("{0:2d} | {1:6.4f} | {2:6.4f} | {3:6.4f}"\
            .format(k , Q[NUM_ATT][NUM_DEF][k] , F , 1-F+Q[NUM_ATT][NUM_DEF][k]))
print("probability(attacker victory) = {0:f}".format(1 - Q[NUM_ATT][NUM_DEF][0]))
