#!/usr/bin/env python3
"""
forgo: active learning for explainable multi-objective optimization
(c) 2025, Tim Menzies <timm@ieee.org>, MIT License.

Options:
  -h         show help
  -p p       distance coefficient           = 2
  -f file    csv data file                  = ../../moot/optimize/misc/auto93.csv
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
import fileinput, random, math, sys, re
sys.dont_write_bytecode = True

# Simple structs (with names fields) that can print themselves.
class o: 
  __init__ = lambda i,**d: i.__dict__.update(**d)
  __repr__ = lambda i: i.__class__.__name__ + '(' + ' '.join(
                       [f":{k} {say(v)}" for k,v in i.__dict__.items()]) + ')'

def say(x):
  if type(x) == float:
    less = x // 1
    return str(less) if x==less else f"{x:.3f}".rstrip("0").rstrip(".")
  return str(x)

"""make cuts an object with its own __repr__

using kernel desnity cuts (the x-value between the means that minismizes abs(pdf(a) - pdf(b)
)
import random, math, matplotlib.pyplot as plt

def best_split_pdf(a, b):
    data = sorted(a + b)
    bins = math.ceil(math.sqrt(len(data)))
    lo, hi = data[0], data[-1]
    width = (hi - lo) / bins
    mids = [lo + (i + 0.5) * width for i in range(bins)]
    mean_a, mean_b = sum(a)/len(a), sum(b)/len(b)

    def pdf_and_var(xs):
        h, n, mu = [0]*bins, len(xs), sum(xs)/len(xs)
        for x in xs:
            h[min(int((x - lo) / width), bins - 1)] += 1
        pdf = [h[i]/n for i in range(bins)]
        var = sum((x - mu)**2 for x in xs) / n
        return pdf, var

    pdfa, vara = pdf_and_var(a)
    pdfb, varb = pdf_and_var(b)

    best = min(
        [m for m in mids if min(mean_a, mean_b) <= m <= max(mean_a, mean_b)],
        key=lambda m: abs(pdfa[mids.index(m)] - pdfb[mids.index(m)])
    )
    weighted_var = (len(a)*vara + len(b)*varb) / (len(a)+len(b))

    plt.plot(mids, pdfa, label="PDF A", marker="o")
    plt.plot(mids, pdfb, label="PDF B", marker="s")
    plt.axvline(best, color="red", linestyle="--", label=f"Split ≈ {best:.2f}")
    plt.legend(); plt.title("PDFs and Split"); plt.grid(); plt.tight_layout(); plt.show()

    return best, weighted_var

# Example usage
random.seed(1)
a = [random.gauss(3, 1) for _ in range(100)]
b = [random.gauss(7, 1) for _ in range(100)]
split, wvar = best_split_pdf(a, b)
print(f"Best split: {split:.2f}, Weighted post-split variance: {wvar:.2f}")

"""
def eq(v,x): 
  "="
  return v == x
  
def le(v,x): 
  "<="
  return v <= x 
  
def gt(v,x): 
  ">"
  return v >  x

def selects(row,t) : return t.test(row[t.at],t.x)

#------------------------------------------------------------------------------
class Col(o):
  def __init__(i,txt=' ',at=0):
    i.txt, i.at, i.n = txt, at, 0
    i.w = 1 # if zero, then ignore this column

  def add(i,x,n=1, flip=1): 
    if x != "?": i.n += flip*n; i.add1(x,n,flip)
    return x

  def sub(i,x,n=1): return i.add(x, n=n, flip = -1) 

  def values(i,rows):
    for row in rows:
      x = row[i.at]
      if x !="?": yield x,row
     
#------------------------------------------------------------------------------
class Num(Col):
  def __init__(i,*_):
    super().__init__(*_); 
    i.lo, i.hi, i.mu, i.m2 = 1e32, -1e32, 0, 0   
    i.goal = 0 if i.txt[-1]=="-" else 1 # define the utopia point  

  def mid(i)   : return i.mu
  def norm(i,x): return x if x=="?" else (x-i.lo)/(i.hi-i.lo+1e-32)
  def var(i)   : 
    return 0 if i.n <= 2 else (max(0,i.m2)/(i.n - 1))**0.5
    
  def add1(i, x, n=1, flip=1):  
    i.lo = min(i.lo,x)
    i.hi = max(i.hi,x)
    if flip < 0 and i.n < 2:
      i.n = i.mu = i.sd = 0
    else:
      d = x-i.mu
      i.mu += flip*d/i.n
      i.m2 += flip*d*(x - i.mu) 

  def cuts(i, rows, Y, Klass):
    least, b4, out = 1E32, None, o(var=1E32, tests=[])
    L, R = Klass(), adds([Y(row) for row in rows], Klass())
    for x,row in i.values(rows):
      R.sub( L.add( Y(row)))
      if x != b4:
        e = (L.n * L.var() + R.n * R.var()) / len(rows)
        if e < least:
          least, out = e, o(var = e, 
                            tests = [o(at=i.at, txt=i.txt, x=x, test=le),
                                     o(at=i.at, txt=i.txt, x=x, test=gt)])
      b4 = x
    return out
     
  def dist(i,a,b):
    if a=="?" and b=="?": return 1
    a,b = i.norm(a), i.norm(b)
    a = a if a!="?" else (1 if b < .5 else 0)
    b = b if b!="?" else (1 if a < .5 else 0)
    return abs(a - b)
 
#------------------------------------------------------------------------------
class Sym(Col):
  def __init__(i,*_): super().__init__(*_); i.has={}

  def add1(i,x, n=1,flip=1): i.has[x] = i.has.get(x,0) + flip*n
  def dist(i,a,b): return a!=b
  def mid(i)     : max(i.has, key=i.has.get)
  def norm(i,x)  : return x
  def var(i)     : return -sum(n/i.n*math.log(n/i.n,2) for n in i.has.values())

  def cuts(i, rows, Y, Klass):
    n,tmp = 0,{}
    for x,row in i.values(rows):
      n += 1 
      tmp[x] = tmp.get(x) or Klass()
      tmp[x].add(Y(row))
    return  o(
      var= 1E32 if n==0 else sum(x.var()*x.n for x in tmp.values())/n,
      tests= [] if n==0 else [o(at=i.at,txt=i.txt,x=x,test=eq) for x in tmp])

#------------------------------------------------------------------------------
class Cols(o):
  def __init__(i,names):
    i.x, i.y, i.names,i.klass,i.ok = [],[],names,None,True
    i.all = [(Num if s[0].isupper() else Sym)(s, j) 
              for j, s in enumerate(names)]
    for c in i.all: 
      if c.txt[-1] != "X":
        if c.txt[-1] == "!": i.klass = c
        (i.y if c.txt[-1] in "!+-" else i.x).append(c)

  def add(i,row): return [c.add(row[c.at]) for c in i.all]
  def sub(i,row): return [c.sub(row[c.at]) for c in i.all]

#------------------------------------------------------------------------------
class Data(o):
  def __init__(i,src=[]): 
    i.rows,i.cols = [],None
    [i.add(row) for row in src]

  def clone(i,rows=[]): return Data([i.cols.names]+rows)
  def ydists(i,rows=None): return adds(i.ydist(row) for row in rows or i.rows) 

  def add(i,row):
    if i.cols: i.rows += [i.cols.add(row)]
    else: i.cols=Cols(row)
    return row

  def kpp(i, k, rows=None):
    def D(x, y):
      key = tuple(sorted((id(x), id(y))))
      if key not in mem: mem[key] = i.xdist(x,y)
      return mem[key] 
      
    row, *rows = shuffle(rows or i.rows)[:the.some]
    out, mem = [row], {}
    for _ in range(1, k):
      dists = [min(D(x, y)**2 for y in out) for x in rows]
      r     = random.random() * sum(dists)
      for j, d in enumerate(dists):
        r -= d
        if r <= 0:
          out.append(rows.pop(j))
          break
    return out, mem

  def nodes(i,lvl=0, key=None):
    yield lvl,i
    for kid in (sorted(i.kids, key=key) if key else i.kids):
      for node1 in kid.nodes(lvl+1, key=key):
        yield node1
     
  def sub(i, row, purge=True):
    i.cols.sub(row)
    if purge: i.rows.remove(row)

  def tree(i, rows=None, Y=None, Klass=Num, test=None):
    Y         = Y or (lambda row: i.ydist(row))
    rows      = rows or i.rows
    here      = i.clone(rows)
    here.ys   = i.ydists(rows)
    here.test = test 
    here.kids = []
    for test1 in min([col.cuts(rows,Y,Klass) for col in i.cols.x],
                     key=lambda x:x.var).tests:
      rows1 = [row for row in rows if selects(row,test1)]
      if the.leaf <= len(rows1) < len(rows):
        here.kids += [i.tree(rows1, Y, Klass, test1)]
    return here
  
  def xdist(i,a,b):
    p = the.p
    def fun(c): return c.w * c.dist(a[c.at], b[c.at])
    return (sum(fun(c)**p for c in i.cols.x) / len(i.cols.x))**(1/p)

  def ydist(i,row):
    p = the.p
    def fun(c): return abs(c.goal - c.norm(row[c.at]))
    return (sum(fun(c)**p for c in i.cols.y) / len(i.cols.y))**(1/p)
  
#------------------------------------------------------------------------------
def shuffle(lst): random.shuffle(lst); return lst

def csv(file=None):
  buf = ""
  for line in fileinput.input(file):
    if line := line.split("#")[0].replace(" ", "").strip():
      buf += line
      if buf and buf[-1] != ",": 
        yield [coerce(x) for x in buf.split(",")]
        buf = ""

def adds(src=[], out=None):
  for x in src:
    out = out or (Sym if type(x) is str else Num)()
    out.add(x)
  return out

def values(i,rows):
  for row in rows:
    x = row[i.at]
    if x != "?": yield x,row

def coerce(x, specials= {'true':1,'True':1, 'false':0, 'False':0, 
                         'none':None, 'None':None}):
  try: return int(x)
  except:
    try: return float(x)
    except: 
      x = x.strip()
      return specials[x] if x in specials else x
      
def cli(d, args):
  "CLI flags for boolean settings need no arg (we just reverse)"
  for c,arg in enumerate(args):
    if seeking := arg[0]=="-" and len(arg)==2 and arg[1].isalpha():
      if arg=="-h": continue
      for k,v in d.items():
        if arg == "-"+k[0]:  
          d[k] = coerce("False" if str(v) == "True"  else (
                        "True"  if str(v) == "False" else (
                        args[c+1] if c < len(args) - 1 else str(v))))
          seeking = False 
      if seeking: print("??",arg,"not in -h,",', '.join("-"+k[0] for k in d))
                   
#------------------------------------------------------------------------------
# too har d   nums
def select(data, cols, k=16, g=5):
  m = len(data[0])
  w = [1] * m
  for _ in range(g):
    centers = data.kpp(k, data, cols)
    rows = []
    for x in data:
      i = min(range(k), key=lambda j: data.xdist(x, centers[j], cols))
      rows.append(x + [chr(97 + i)])
    keep = data.tree(rows)
    w = [w[i] if i in keep else 0 for i in range(m)]
  return [i for i, v in enumerate(w) if v > 0]

def main():
  for n,s in enumerate(sys.argv):
    if fun := globals().get("eg" + s.replace("-","_")):
      random.seed(the.rseed) 
      fun(None if n==len(sys.argv) - 1 else sys.argv[n+1])

#------------------------------------------------------------------------------
def eg_h(_)    : eg__help(_)
def eg__help(_): print(__doc__)

def eg__the(_): print(the)

def eg__csv(f=None): 
  [print(row) for row in csv(f or the.file)]  

def eg__cols(_) :
  for col in Cols("age,name,heightX,Wealth+,Sadness-".split(",")).all:
     print(col)  

def eg__data(_) :
  [print(col) for col in Data(csv(the.file)).cols.all]

def eg__subs(_) :
  a   = Data(csv(the.file))
  b,c = a.clone(), a.clone()
  tmp = []
  for j,row in enumerate(a.rows):
    c.add(b.add(row))
    if len(c.rows)==200: tmp += [str(c) for c in c.cols.x]
  for j,row in enumerate(a.rows[::-1]):
    c.sub(row)
    if len(c.rows)==200: tmp += [str(c) for c in c.cols.x]
  [print(x) for x in sorted(tmp)]

def eg__kpp(k):
  k = coerce(k or "64")
  d = Data(csv(the.file))
  for rows in [d.kpp(k=k)[0], 
               random.choices(d.rows,k=k)]:
    print(k,adds([d.xdist(*random.choices(rows,k=2)) for _ in range(100)]))

def eg__tree(f):
  k = 32
  d = Data(csv(f or the.file))
  showTree( d.tree(d.kpp(k)[0]))

def showTree(tree):
  def show(t): return f"{t.txt} {t.test.__doc__} {t.x}" if t else ""
  def win(t): return 1-(t.ys.mu - tree.ys.lo) / (tree.ys.mu - tree.ys.lo)
  print("   n      d2h     win")
  print(" ---     ----     ---")
  for lvl,node in tree.nodes(key=lambda t:t.ys.mu):    #----  
    post = "" if node.kids else ";"
    pre  = f"{len(node.rows):>4}  |  {node.ys.mu:>4.2f}  | {int(100*win(node)):>4}\t   " 
    print(pre,((lvl - 1) * "|  ") + show(node.test) + post)       #
#------------------------------------------------------------------------------
the = o(**{m[1]:coerce(m[2]) 
        for m in re.finditer(r"-\w+\s*(\w+).*=\s*(\S+)", __doc__)})

if __name__ == "__main__": 
  cli(the.__dict__, sys.argv)
  main()
