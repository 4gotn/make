#!/usr/bin/env python3
# <!-- vim: set et ts=2 sw=2 sts=2 : -->
"""
forgo: active learning for explainable multi-objective optimization
(c) 2025, Tim Menzies <timm@ieee.org>, MIT License.

Options:
  -h         show help
  -b bins    number of bins = 10
  -f file    csv data file = ../../moot/optimize/misc/auto93.csv
  -s some    sub-samples used for distances = 128
  -l leaf    min number leaves per tree     = 2
  -r rseed   random number seed             = 1234567890

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

#-----------------------------------------------------------------------------
class o: 
  "Simple structs (with named fields) that can print themselves."
  __init__ = lambda i,**d: i.__dict__.update(**d)
  __repr__ = lambda i: i.__class__.__name__ + '(' + ' '.join(
                       [f':{k} show(v)' for k,v in i.__dict__.items()])+')'

class Test(o):
  "Tests have text, operators and values."
  def __init__(i,col,op, val):
     i.txt, i.at, i.op, i.val, i.test = col.txt, col.at, op, val
     
  def __repr__(i): return f"{i.txt} {i.op} {i.val}" 
  def selects(row):
    v,w = row[i.at], i.val
    return v=="?" or v==w if i.op=="=" else (v<=w if i.op==">" else v>= w)

class Row(o):
  def __init__(i, a,bins=[]): i.cells, i.bins = a,bins
    
def bins(src):
  cols = None
  for row in src:
    if not head: cols=Cols(row)
    else: yield Row(row,[c.bin(c.has(row)) for c in cols.all]), cols 

class Col(o):
  def __init__(i,txt=' ',at=0):
    i.txt, i.at, i.n = txt, at, 0

  def add(i,x,n=1, flip=1): 
    if x != "?": i.n += flip*n; i.add1(x,n,flip)
    return x
    
  def has(i,row): return row[i.at]

class Num(o):
  def __init__(i,**_): 
    super().__init__(**_)
    i.lo, i.hi = BIG, -BIG
  def add1(i,x, *_):
    i.lo = min(x, i.lo)
    i.hi = max(x, i.hi)
    
  def norm(i,x): return x if x=="?" else (x - i.lo) / (i.hi - i.lo)
  def bin(i,x) : return min(int(i.norm(x)*the.bins), the.bins - 1)

class Sym(o): 
  def __init__(i,**_): 
    super().__init__(**_)
    i.has = {} 
  def add1(i,x,n=1,flip=1):
    i.has[x] = flip*n + (has[x] if x in has else 0)
  def bin(i,x): return x

#-----------------------------------------------------------------------------
def show(v):
  "Return pretty print float strings (everything else as a string)."
  if type(v) == float:
    w = v // 1
    v = w if v==w else f"{v:.3f}".rstrip("0").rstrip(".")
  return str(v)

def coerce(x, specials= {'True':1, 'False':0, 'None':None}):
  "Coerce a string to an atom."
  try: return int(x)
  except:
    try: return float(x)
    except: 
      x = x.strip()
      return specials[x] if x in specials else x

def csv(file=None):
  "Read csv rows after killing comments and spaces, join lines ending in ','"
  buf = ""
  for line in fileinput.input(file):
    if line := line.split("#")[0].replace(" ", "").strip():
      buf += line
      if buf and buf[-1] != ",": 
        yield [coerce(x) for x in buf.split(",")]
        buf = ""
  return out

def cli(d, args):
  "Update a dictionary 'slot' if there is a CLI flag -s Val"
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
