import pandas as pd
import numpy as np
d=pd.read_pickle("ncaa.pkl")
def colley_iter(d, t):
    n_team = len(d['team'])
    n_wins = np.array([i[1] for i in d.values])
    n_losses = np.array([i[2] for i in d.values])
    n_games = n_wins + n_losses
    teams = [i[0] for i in d.values]
    opps = [i[3] for i in d.values]
    r = (1+n_wins)/(2+n_games)
    opps_r= []
    for i in range(n_team):
        opps_r.append(sum(r[opps[i]]))
    opps_r = np.array(opps_r)
    max_diff = 1000
    n =0
    while max_diff > t:
        prev_r = r.copy()
        eff_wins = (n_wins-n_losses)/2 + opps_r
        r = (1+eff_wins)/(2+n_games)
        opps_r = list(opps_r)
        opps_r.clear()
        for i in range(n_team):
            opps_r.append(sum(r[opps[i]]))
        opps_r = np.array(opps_r)
        max_diff = max(abs(r-prev_r))
        n+=1
    df = pd.DataFrame({'team': teams, 'score': r}).sort_values('score', ascending=False)
    return [df,n]

