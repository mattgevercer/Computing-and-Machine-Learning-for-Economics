import pandas as pd
#import os
import numpy as np
#os.chdir('/Users/mattgevercer/Downloads/')
data=pd.read_pickle("ncaa.pkl")
n_team = len(data['team'])
def colley_rank(d):
    n_wins = np.array([i[1] for i in d.values])
    teams = [i[0] for i in d.values]
    n_losses = np.array([i[2] for i in d.values])
    n_games = n_wins+n_losses
    opps = [i[3] for i in d.values]
    n_team = len(d['team'])
    A = [np.zeros(n_team) for i in range(n_team)]
    b = 1+(n_wins-n_losses)/2
    for i in range(n_team):
        for j in range(n_team):
            if i == j:
                A[i][j] = 2+n_games[i]
    for i in range(n_team):
        for j in range(n_team):
            if j in opps[i]:
                A[i][j] -= 1*np.count_nonzero(opps[i]==j)
    rank = np.matmul(np.linalg.inv(A),b)
    df = pd.DataFrame({'team':teams,'score':rank}).sort_values('score',ascending=False)
    return [df,A,b]



