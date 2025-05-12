# The Great Secret




Let me introduce you to Menzies's forth law:

> Menzies's 4th Law: For SE, the best thing to do with most data is to throw it away. 



(Here I am I am talking about regression, classification and optimization problems. 
Generative tasks may require models with billions of variables learned from 100s of gigabytes of data.)

Give a table of data, pruning rows and columns results in better
models. Readers familiar with the manifold assumption [73] and the
Johnson-Lindenstrauss lemma [74] will be nodding sagely at this
point– but the reductions seen in SE data are startling. For example,
Chen, Kocaguneli, Tu, Peters, and Xu et al. found they could predict
for Github issue close time, effort estimation, and defect prediction,
even after ignoring labels for 80%, 91%, 97%, 98%, 100% (respectively)
of their project data labels [65],[70],[71],[72],[75]. Data sets
with thousands of rows can be modeled with just a few dozen samples
[76]– perhaps because of power laws [77] or large amounts of repeated
structures [78] in the data from SE projects. So we really need to
study why:

Its a repeated result:

- PCA, 1901
- Narrows: Amarel 1960s
- Prototypes: Chen 1975 
- Frames: Minsky, 1975
- Min environments: DeKleer, 1986
- Saturation: Horgan & Mathur: 1980
- Homogenous propagation: Michael: 1981
- Master variables: Crawford & Baker, 1995
- Clumps, Druzdel, 1997
- Feature subset section, Kohavi, 1997, 
- Back doors, Williams, 2002 
- Semi-supervised learning
- Active learning: many people (2000+)

add examples:

my stuff with tables of data
