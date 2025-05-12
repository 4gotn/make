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

#------------------------------------------------------------------------------
class o: 
  __init__ = lambda i,**d : i.__dict__.update(**d)
  __repr__ = lambda i     : i.__class__.__name__ + '('+str(i.__dict__)+')'

#------------------------------------------------------------------------------
class Data:
  def __init__(i, names, rows=[]):
    """Numeric columns have `lo` and `hi`. Y-values have `goal`.
    `f` is where we store frequencies f[col][bin]."""
    i.names, i.hi, i.lo, i.goal, i.rows = names, {}, {}, {}, []
    i.f = lambda: defaultdict(lambda: defaultdict(int))
    for c,s in enumerate(names):
      if s[0].isupper():
        i.hi[c], i.lo[c] = -BIG, BIG
        if s[-1] in "+-":
          i.goal[c] = 0 if s[-1]=='-' else 1
    i.adds(rows)
 
  def clone(i, rows=[]): return Data(i.names, rows)

  def adds(i,rows=[]): 
    "Add multiple rows, update the frequency counts."
    [i.add(row) for row in rows]
    i.counts()

  def add(i, row):
    "Add one rows, update the lo and hi knowledge."
    i.rows += [row]
    i.bins += [row[:]]
    for c in i.hi:
      x = row[c]
      if x != "?":
        row[c]  = x = float(x)
        i.lo[c] = min(i.lo[c], x)
        i.hi[c] = max(i.hi[c], x)
    return i

  def counts(i):
    "Fill in the bins and the frequency counts."
    for rows in i.rows:
      for c,x in enumerate(i.rows):
        if x != "?" and c not in i.goal:
          i.f[c][ i.bin(c,x) ] += 1

  def like(i, row, nh, nall):
    def fun(c,b):
      return (i.f[c][b] + the.m*prior) / (len(i.rows) + the.m + 1/BIG)
    prior = (len(i.rows) + the.k) / (nall + the.k*nh)
    tmp   = [fun(c, i.bin(c,x)) for c,x in enumerate(row) 
             if x != "?" and c not in goal]
    return sum(math.log(n) for n in tmp + [prior] if n>0)

  def ydist(i,row):
    n = sum(abs(i.norm(c, row[c]) - g) ** the.p for c,g in i.goals.items())
    return (n / len(d.goal)) ** (1 / the.p)

  def rorder(i):
    rows.sort(key=lambda r: i.ydist(r))
    return i

  def norm(i,c,x):
    if x=="?" or c not in hi: return x
    return (x - i.lo[c]) / (i.hi[c] - i.lo[c] + 1/BIG)

  def bin(i,c,x):
    if x=="?" or c not in hi: return x
    return min(the.bin - 1, int(i.norm(c,x)*the.bin))

#------------------------------------------------------------------------------
def actLearn(d):
  random.shuffle(d.rows)
  n    = the.start
  m    = round(n**the.guess)
  done = d.clone(d.rows[:n]).rorder()
  todo = d.rows[n:]
  best = d.clone(done.rows[:m])
  rest = d.clone(done.rows[m:])
  while len(todo) > 2 and m < the.Stop:
    n += 1
    hi, *lo = sorted(todo[:the.Few], key=_guess, reverse=True)
    todo = lo + todo[the.Few:]
    best.add(hi)
    br.add(hi)
    if len(best.rows) >= round(n**the.guess):
      rest.add( best.sub( best.rorder().rows.pop(-1)))
  return o(best=best, rest=rest, todo=todo)

#------------------------------------------------------------------------------
def csv(file=None):
  for line in fileinput.input(file):
    if line := line.split("#")[0].replace(" ", "").strip():
      yield [x for x in line.split(",")]

def cli(d, args):
  for c,arg in enumerate(args):
    for k,v in d.items():
      if arg == "-"+k[0]:  
        d[k] = coerce(args[c+1] if c < len(args) - 1 else str(v))

#------------------------------------------------------------------------------
def eg_h(_): print(__doc__)
def eg__the(_): print(the)

#------------------------------------------------------------------------------
the = o(**{m[1]:coerce(m[2]) 
        for m in re.finditer(r"-\w+\s*(\w+).*=\s*(\S+)", __doc__)})

if __name__ == "__main__":
  cli(the.__dict__, sys.argv) # update 'the' from the command line
  for n,s in enumerate(sys.argv):
    if fun := globals().get("eg" + s.replace("-","_")):
      random.seed(the.rseed) # reset the random seed before running an eg
      fun(None if n==len(sys.argv)-1 else coerce(sys.argv[n+1]))
