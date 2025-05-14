#!/usr/bin/env gawk -f
BEGIN { BINS=10; BIG=1E32; SEED=1 }
      { for(c=1; c<=NF;  c++) $c = coerce($c) }
NR==1 { header()
        srand(SEED) }
NR>1  { data() }

function header(   c) {
  for(c=1; c<=NF; c++) { 
    Names[c]=$c
    if ($c ~ /^[A-Z]/) { Hi[c] = -(Lo[c] = BIG)}
    $c ~ /!$/ ? Y[c] : X[c]}}

function data(   r,c) {
  r = int(rand()*10^7)
  for(c=1; c<=NF; c++) {
    D[r][c] = $c
    if ($c != "?")
      for(c in Hi) { 
        Hi[c] = max($c, Hi[c])
        Lo[c] = min($c, Lo[c]) }}}  

function trim(s) {
  sub(/^[ \t\r]/,"",s)
  sub(/[ \t\r]$/,"",s)
  return s }

function coerce(x,  y) { y=x+1; return x==y ? y : trim(x) }
function max(x, y)     { return x >= y ? x  : y }
function min(x, y)     { return x <= y ? x  : y }
function abs(x)        { return x <  0 ? -x : x }

function dist(x,y,   d) {
   for(c in X) 
     d += (c in Lo ? numDist(c,x[c], y[c]) : symDist(c,x[c],y[c]))^P
   return (d/length(X)) ^ (1/P) }

function numDist(c, x, y) {
  if (x=="?" && y=="?") return 1
  x = norm(c,x)
  y = norm(c,y)
  x = x=="?" ? x : (y>.5 ? 0 : 1) 
  y = y=="?" ? y : (x>.5 ? 0 : 1) 
  return abs(x-y) }

function symDist(c, x, y) {
  if (x=="?" && y=="?") return 1
  return x != y }

function norm(c, x) {
  if (x=="?") return x
  if (c in Lo) return (x - Lo[x]) / (Hi[c] - Lo[c] + 1/BIG) 
  return x }

function poles(a,    d,far,r,r2,rows,some) {
  for(r in D) { some[r]; if (length(some) <= 20) break }
  far = -1
  for(r in rows)
    for(r2 in rows)
      if (r > r2) 
        if (d = dist(r,r2) > far) { far=d; a[1]=r; a[2]=r2 };
  far = -1  
  for(r in rows)
    if ((d = dist(r,a[1])+dist(r,a[2])) > far) {far=d; a[3] = r};
  far=-1
  for(r in rows)
    if ((d=dist(r,a[1])+dist(r,a[2])+dist(r,a[3])) > far) {far=d; a[4]=r} }
