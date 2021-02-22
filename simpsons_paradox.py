"""
simple detector of Simpson's paradox'
"""

from random import randint, random, seed, choices
from collections import defaultdict
from operator import gt, lt



def make_data(m:'number of observations', 
              p:'probability in independent variable'=0.5, 
              k:'number of distinct values in the confounding variable'=2, 
              column_wise:'If False, observation tuples are returned'=True,
              rs:'random seed as int. If True, the random seed number is printed'=None):
    # Manage random seed
    make_data.random_seed = make_data.rs = None
    if rs:
        if rs is True:
            rs = randint(0,999999)
        seed(abs(int(rs)))
        make_data.random_seed = make_data.rs = abs(int(rs))
    
    # Generate data
    independent = [1 if random() >= p else 0 for _ in range(m)]     # binary variable
    weights = [random() for _ in range(k)];  w = [w/sum(weights) for w in weights]
    confounding = choices(range(k), weights=w, k=m)
    dependent = [round(random() * (0.85 if v and random()>.5 else 1), 2) for v in independent]
    return (independent, confounding, dependent) if column_wise else tuple(zip(independent, confounding, dependent))



def print_tables(data):
    for s in ("(v1,)", "(v1, v2)"):
        print("\none variable:" if len(s.split()) == 1 else "\nboth variables (the second column is the confounding variable):")
        d = defaultdict(list)
        [d[e[0]].append(e[-1]) for e in sorted([(eval(s), y) for (v1,v2,y) in zip(*data)], key=lambda t: t[0])]
        [print(("{:<3}" * (len(t) + 1)).format(*t, v)) for (t,v) in sorted(tuple({k: round(sum(l)/len(l), 2) for k,l in d.items()}.items()), key=lambda t: t[0])]
    print()



def detect_simpsons_paradox(data:'list of columns'):
    """Detect Simpson's paradox"""
    d = defaultdict(list)
    [d[x].append(y) for (x,c,y) in zip(*data)]
    l = [sum(d[k])/len(d[k]) for k in sorted(d)]
    if len(l) <= 1:
        return False
    
    which_greater = 0 if l[0] > l[1] else 1 if l[1] > l[0] else None
    if which_greater is None:  # if both values are equal
        return False
    
    # Split the data into two groupy i.e. group by the independent variable
    d = defaultdict(list)
    [d[(x,c)].append(y) for (x,c,y) in zip(*data)]
    
    c0, c1 = list(), list()
    summarized = [(t, sum(l)/len(l)) for t,l in sorted(d.items())]
    [(c0,c1)[i].append((c,v)) for (i,c),v in summarized]    
    pairs = [(v, dict(c1)[k]) for k,v in c0 if dict(c1).get(k)]
    
    op = (lt, gt)[which_greater]
    bools = [op(l,r) for l,r in pairs]
    return (sum(bools) / len(bools) > 0.5) if bools else False




from pandas import DataFrame

def test():
    for _ in range(10000):
        k = randint(2, 5)
        m = randint(10, 10 * k)
        p = random()
        data = make_data(m=m, p=p, k=k)
        
        if detect_simpsons_paradox(data):
            break

    print("Simson's paradox detected:")
    print_tables(data)
    df = DataFrame(data).T
    df.iloc[:,0] = df.iloc[:,0].astype("uint8")
    df.iloc[:,1] = df.iloc[:,1].astype("uint8")
    return df
        


def main():
    df = test()
    globals()['df'] = df
if __name__ == '__main__': main()


