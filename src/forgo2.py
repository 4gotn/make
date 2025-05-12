#!/usr/bin/env python3
# <!-- vim: set et ts=2 sw=2 sts=2 : -->
"""
forgo: active learning for explainable multi-objective optimization
(c) 2025, Tim Menzies <timm@ieee.org>, MIT License.

Options:
  -h         show help
  -b bins    number of bins                 = 10
  -f file    csv data file = ../../moot/optimize/misc/auto93.csv
  -k k       low frequency Bayes hack       = 1  
  -l leaf    min number leaves per tree     = 2
  -m m       low frequency Bayes hack       = 2  
  -r rseed   random number seed             = 1234567890
  -s some    sub-samples used for distances = 128
"""
import fileinput, random, sys, re
from collections import defaultdict

sys.dont_write_bytecode = True
BIG = 1E32

class o: 
  __init__ = lambda i, **d: i.__dict__.update(d)
  __repr__ = lambda i: return i.__class__.__name__+'('+show(i.__dict__)+')'

def show(d):
  return str({k: (f"{v:3g}" if type(v)==float else v) for k,v in d.items()})

 # in this code, when possible, i=self, c=column index, r=row
#------------------------------------------------------------------------------
class Num(o):
  def __init__(i, has=[], txt=" "): 
    i.txt = txt
    i.sd = i.m2 = i.mu = i.n = 0
    [i.add(x) for x in has]
  
  def add(i,x,inc=1):
    i.n += inc
    i.lo = min(v, i.lo)
    i.hi = max(v, i.hi)
    if inc < 0 and i.n < 2: 
      i.n = i.mu = i.m2 = i.sd = 0
    else:
      d = i.mu - x
      i.mu += inc * d/i.n
      i.m2 += inc * d * (x - i.mu)
      i.sd  = 0 if i.n <=2  else (max(0,i.m2)/(i.n-1))**.5
    return x

  def bin(i,x) : return min(the.bins-1, int(i.cdf(x)*the.bin))

  def cdf(i,x):
    def fun(z): return 1 - 0.5 * math.exp(-0.717 * z - 0.416 * z * z) 
    z = (x - i.mu) / i.sd
    return  z>=0 and fun(z) or 1 - fun(-z) end

  def norm(i,x): return (x - i.lo) / (i.hi - i.lo + 1/BIG)

  def sub(i,x) : return i.add(x,-1)

class Data(o):
  def __init__(i, rows):
    rows = iter(rows)
    i.names, i.nums, i.goals, i.rows = next(rows), {}, {}, []
    i.header()
    [i.add(row) for row in rows]

  def add(i, row, inc=1, purge=False):
    "Add one row, update the num knowledge."
    i.f = None
    for c,n in i.nums.items():
      x = row[c]
      if x != "?":
        row[c] = n.add(float(x),inc)
    if inc==1 : i.rows.append(row)w
    elif purge: i.rows.remove(row) # disabled by default sice remove is slow
    return row

  def bin(i,c,x): return i.nums[c].bins(c) if c in i.nums else x

  def clone(i,rows=[]): return Data([i.names] + rows)

  def header(i):
    i.f = None
    for c,s in enumerate(i.names):
      if s[0].isupper():
        i.nums[c] = Num() # hi lo
        if s[-1] in "+-":
          i.goals[c] = 0 if s[-1]=='-' else 1

  # need to be able to talk to a global space of discretization
  def like(i, row, f, nh, nall):
    _like = lambda c,b: (f[c][b] + the.m*prior) / (len(i.rows) + the.m + 1/BIG)
    prior = (len(i.rows) + the.k) / (nall + the.k*nh)
    tmp   = [_like(c, i.bin(c,x)) for c,x in enumerate(row) 
             if x != "?" and c not in goals]
    return sum(math.log(n) for n in tmp + [prior] if n>0)

  def ok(i):
    "Fill in the bins and the frequency counts."
    if not i.f:
      i.f  = lambda: defaultdict(lambda: defaultdict(int))
      for row in i.rows:
        for c,x in enumerate(row):
          if x != "?": 
            i.f[c][ i.bin(c,x) ] += 1
    return i

  def sort(i,rows=None): 
    (rows or i.rows).sort(key=lambda row: i.ydist(row)); return i

  def sub(i,row, purge=False): i.add(row,-1,purge)

  def ydist(i,row):
    n= sum(abs(i.nums[c].norm(row[c]) - g) ** the.p for c,g in i.goals.items())
    return (n / len(d.goals)) ** (1 / the.p)

#------------------------------------------------------------------------------
def actLearn(d):
  random.shuffle(d.rows)
  n    = the.start
  m    = round(n**the.guess)
  todo = d.rows[n:]
  labeled = d.clone(d.rows[:n]).sort()
  best = d.clone(labeled.rows[:m])
  rest = d.clone(labeled.rows[m:])
  while len(todo) > 2 and m < the.Stop:
    n += 1
    hi, *todo = sorted(todo[:the.Few], key=aq, reverse=True) + todo[the.Few:]
    best.add(hi)
    br.add(hi)
    if len(best.rows) >= round(n**the.guess):
      rest.add( best.sub( best.sort().rows.pop(-1)))
  return o(best=best, rest=rest, todo=todo)

#------------------------------------------------------------------------------
def csv(file=None):
  for line in fileinput.input(file):
    if line:
      yield [x.strip() for x in line.split(",")]

def cli(d):
  for c,arg in enumerate(sys.argv):
    for k,v in d.items():
      if arg == "-"+k[0]:  
        d[k] = coerce(sys.argv[c+1])

#------------------------------------------------------------------------------
def eg_h(_): print(__doc__)
def eg__the(_): print(the)

#------------------------------------------------------------------------------
the = o(**{m[1]:coerce(m[2]) 
        for m in re.finditer(r"-\w+\s*(\w+).*=\s*(\S+)", __doc__)})

if __name__ == "__main__":
  cli(the.__dict__) # update 'the' from the command line
  for n,s in enumerate(sys.argv):
    if fun := globals().get("eg" + s.replace("-","_")):
      random.seed(the.rseed) # reset the random seed before running an eg
      fun(None if n==len(sys.argv)-1 else coerce(sys.argv[n+1]))
