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
  __init__ = lambda i,**d: i.__dict__.update(d)
  __repr__ = lambda     i: i.__class__.__name__+'(f{say(i.__dict__)}))'

def say(d): 
  return {k: (f"{v:3g}" if type(v)==float else v) for k,v in d.items()}

# in this code, when possible, i=self, c=column index, r=row.
#------------------------------------------------------------------------------
class Sym(o):
  def __init__(i, has=[], txt=" ", at=0): 
    i.txt, i.at, i.n, i.has = txt, at, 0, {}
    [i.add(x) for x in has]
  
  def add(i, x, inc=1):
    if x !="?":
      i.n += inc
      i.has[x] = (i.has[x] if x in i.has else 0) + inc
    return x

  def bin(i,x): return x
    
class Num(o):
  def __init__(i, has=[], txt=" ", at=0): 
    i.txt, i.at, i.n = txt, at, 0
    i.sd, i.m2, i.mu, i.goal = 0, 0, 0, 0 if txt[-1]=="-" else 1
    [i.add(x) for x in has]
  
  def add(i, x, inc=1):
    if x != "?": 
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

  def bin(i,x): return min(the.bins-1, int(i.cdf(x)*the.bin))

  def cdf(i,x):
    def fun(z): return 1 - 0.5 * math.exp(-0.717 * z - 0.416 * z * z) 
    z = (x - i.mu) / i.sd
    return  fun(z) if z>=0 else 1 - fun(-z)

  def norm(i,x): return (x - i.lo) / (i.hi - i.lo + 1/BIG)

class Cols(o):
  def __init__(i,names):
    i.names, i.all, i.x, i.y, i.klass = names, {}, {}, {}, None
    for c,s in enumerate(i.names):
      col = (Num if s[0].isupper() else Sym)(txt=s, at=c)
      if s[-1] != "X":
        if s[-1] == "!": i.klass = col
        (i.y if s[-1] in "+-!" else i.x).append(col)

  def add(i, row, inc=1): [c.add(row[c.at], inc) for col in i.all]
      
class Data(o): 
  def __init__(i, src=[]):
    i.rows, i.cols, i.f = [], None, None
    [i.add(row) for row in src]

  def add(i,row, inc=1, purge=False):
    i.f = None
    if not i.cols: i.cols = Cols(row)
    else:
      if purge: i.rows.remove(row)
      i.cols.add(row, i, inc)
    return row
    
  def clone(i,rows=[]): return Data([i.cols.names]+rows)  

  def bin(i,c,x): 
    z = Data.zero
    return z.nums[c].bins(c) if c in z.nums else x

  def clone(i,rows=[]): return Data([i.names] + rows)

  def ok(i, rows=[]):
    if not i.f:
      i.f = lambda: defaultdict(lambda: defaultdict(int))
      for row in rows or i.rows:
        for c,x in enumerate(row):
          if x != "?": 
            i.f[c][ i.bin(c,x) ] += 1 
    return i
    
  def like(i,  row, f, nh, nall):
    def _like(c,b): return (f[c][b]+the.m*prior) / (len(i.rows)+the.m+1/BIG)
    prior = (len(i.rows) + the.k) / (nall + the.k*nh)
    tmp   = [_like(c, c.bin(x)) for c in i.cols.x if x != "?"]
    return sum(math.log(n) for n in tmp + [prior] if n>0)
    
  def sort(i, rows=None): 
    (rows or i.rows).sort(key=lambda row: i.ydist(row)); return i

  def sub(i, row, purge=False): i.add(row, -1, purge)

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
def coerce(x):
  try: return int(x)
  except:
    try: return float(x)
    except: return x.strip()
  
def csv(file=None):
  for line in fileinput.input(file):
    if line: yield [coerce(x) for x in line.split(",")]

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
