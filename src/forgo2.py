#!/usr/bin/env python3
# <!-- vim: set et ts=2 sw=2 sts=2 : -->
"""
forgo: active learning for explainable multi-objective optimization
(c) 2025, Tim Menzies <timm@ieee.org>, MIT License.

Options:
  -h         show help
  -b bins    number of bins                 = 10
  -s some    sub-samples used for distances = 128
  -l leaf    min number leaves per tree     = 2
  -r rseed   random number seed             = 1234567890
  -f file    csv data file = ../../moot/optimize/misc/auto93.csv

Demos: 
  --the      show settings
  --csv      show csv reader
  --cols     show col generation
  --data     show columns after reading data
  --subs     show we can incrementally add/delete rows
  --kpp      show kmeans++ centroids
"""
import fileinput, random, sys, re
sys.dont_write_bytecode = True
BIG = 1E32

the = {'big': 1E32, 'bins': 10, 'p': 2}
b4 = {k: k for k in ENV}

class Data:
  def __init__(i, names):
    i.names = names
    i.hi, i.lo, i.goal, i.f = {}, {}, {}, {}
    for c, txt in names.items():
      i.f[c] = {b: {0: 0, 1: 1} for b in range(1, the['bins'] + 1)}
      if txt[0].isupper():
        i.hi[c], i.lo[c] = -the['big'], the['big']
        if txt[-1] in "+-":
          i.goal[c] = 0 if txt.endswith('-') else 1
    i.rows = []
  
  def add(i, row):
    i.rows.append(row)
    for c in i.hi:
      x = row[c]
      i.hi[c] = max(i.hi[c], x)
      i.lo[c] = min(i.lo[c], x)

def threes(d):
    n = len(d.rows)
    d.rows.sort(key=lambda r1: ydist(r1, d))
    for r in range(n):
        kl = r < int(n ** 0.5)
        for c in range(len(d.rows[r])):
            x = bin(c, d.rows[r][c])
            F[c][x][kl] = F[c].get(x, {}).get(kl, 0) + 1

def ydist(row, d):
    total = sum(abs(norm(c, v) - d.goal[c])**the['p'] for c, v in row.items())
    return (total / len(d.goal))**(1 / the['p'])

def coerce(x): return float(x) if x.isdigit() else trim(x)

def trim(s): return s.strip()

def bin(c, x):
  if x=="?" or c not in in d.hi:
        if x == "?": return x
        return (x - d.lo[c]) / (d.hi[c] - d.lo[c] + 1 / the['big'])
    return x

#-----------------------------------------------------------------------------
def show(v):
  "Return pretty print float strings (everything else as a string)."
  if type(v) == float:
    w = v // 1
    v = w if v==w else f"{v:.3f}".rstrip("0").rstrip(".")
  return str(v)

def coerce(x):
  try: return int(x)
  except:
    try: return float(x)
    except: return x.strip()

def csv(file=None):
  for line in fileinput.input(file):
    if line := line.split("#")[0].replace(" ", "").strip():
      yield [coerce(x) for x in line.split(",")]

def cli(d, args):
  for c,arg in enumerate(args):
    for k,v in d.items():
      if arg == "-"+k[0]:  
        d[k] = coerce(args[c+1] if c < len(args) - 1 else str(v))

#-----------------------------------------------------------------------------
# convert doc string to "the" settings 
the = o(**{m[1]:coerce(m[2]) 
        for m in re.finditer(r"-\w+\s*(\w+).*=\s*(\S+)", __doc__)})

#-----------------------------------------------------------------------------
def eg_h(_): print(__doc__)
def eg__the(_): print(the)
#-----------------------------------------------------------------------------
if __name__ == "__main__":
  cli(the.__dict__, sys.argv) # update 'the' from the command line
  for n,s in enumerate(sys.argv):
    if fun := globals().get("eg" + s.replace("-","_")):
      random.seed(the.rseed) # reset the random seed before running an eg
      fun(None if n==len(sys.argv)-1 else coerce(sys.argv[n+1]))
