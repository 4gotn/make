# The Great Secret




Let me introduce you to Menzies's forth law:

> Menzies's 4th Law: For SE, the best thing to do with most data is to throw it away. 



(Here I am I am talking about regression, classification and optimization problems. 
Generative tasks may require models with billions of variables learned from 100s of gigabytes of data.)

Give a table of data, pruning rows and columns results in better
models. 
Numerous AI researchers 
report the existence of a small number of 
_key_ variables that
determine the behavior of the rest of the model. When
such keys are present, then the problem of controlling an
entire model simplifies to just the problem of controlling
the keys.

Keys have been discovered in AI many times and called
many different names such as  _principle components, variable subset selection, narrows,
master variables, and backdoors_. 

<img align=right src="../img/pca.png">

As far back as 1902, Pearson reported that underlying data sets with many dimensions
were a handful of _princple componets_ that capture the overall direction of the data.
Pearson's formalism is heavily mathematical but we can see his effect in an intuative way as follows.
To capture the "direction" of data:

- Draw one line between two distant points _A,B_ 
- Draw a second
line at right-angles to that first line.
- Draw every other point at the _x,y_ position where it falls  [^xy].

[^xy]: Let _A,B_ be our two distance points.
Let _A,B_ be separated by distance _c_. Let a point P have  a distance _a,b_ to the points _A,B_.
The cosine rule says
\\(P_x=\frac{a^2 + c^c - b^2}{2c}\\) and Pythagoras says \\(P_y=(a^2-x^2)^{0.5}\\).

<img align=right src="../img/fastmap.png">

Then
we can see 
In the 1960s, Amarel
observed that search problems contain _narrows); i.e. tiny sets
of variable settings that must be used in any solution [11 ].
Amarel’s work defined macros that encode paths between
the narrows in the search space, effectively permitting a
search engine to leap quickly from one narrow to another.

In later work, data mining researchers in the 1990s
explored and examined what happens when a data miner
deliberately ignores some of the variables in the training
data. Kohavi and John report trials of data sets where up
to 80% of the variables can be ignored without degrading classification accuracy [13]. Note the similarity with
Amarel’s work: it is more important to reason about a small
set of important variables than about all the variables.

At the same time, researchers in constraint satisfaction
found “random search with retries” was a very effective
strategy. Crawford and Baker reported that such searches
took less time than a complete search to find more solutions
using just a small number of retries [ 12]. Their ISAMP
“iterative sampler” makes random choices within a model
until it gets “stuck”; i.e. until further choices do not
satisfy expectations. When “stuck”, ISAMP does not waste
time fiddling with current choices (as was done by older
chronological backtracking algorithms). Instead, ISAMP
logs what decisions were made before getting “stuck”. It
then performs a “retry”; i.e. resets and starts again, this
time making other random choices to explore.

Crawford and Baker explain the success of this strange
approach by assuming models contain a small set of master
variables that set the remaining variables (and this paper
calls such master variables keys). Rigorously searching
through all variable settings is not recommended when
master variables are present, since only a small number of
those settings actually matter. Further, when the master
variables are spread thinly over the entire model, it makes
no sense to carefully explore all parts of the model since
much time will be wasted “walking” between the far-flung
master variables. For such models, if the reasoning gets
stuck in one region, then the best thing to do is to leap at
random to some distant part of the model.

A similar conclusion comes from the work of Williams et
al. [10]. They found that if a randomized search is repeated
many times, that a small number of variable settings were
shared by all solutions. They also found that if they set
those variables before conducting the rest of the search,
then formerly exponential runtimes collapsed to low-order
polynomial time. They called these shared variables the
backdoor to reducing computational complexity.

More recent work on _semi-supervised learning_ showed that 
it was not necessary to reason over all the data.
Semi-supervised learning relies on several key assumptions about the data to effectively leverage both labeled and unlabeled data. These assumptions include the continuity assumption (or smoothness assumption), the cluster assumption, and the manifold assumption: 

1. Continuity/Smoothness Assumption: This assumption states that data points that are close together in the input space are more likely to have the same label. In essence, if two data points are near each other, they are also likely to belong to the same class. 

2. Cluster Assumption: This assumption suggests that the data can be grouped into distinct clusters, and data points within the same cluster are likely to have the same label. Decision boundaries are often placed between these high-density clusters. 

3. Manifold Assumption: This assumption posits that the data lies on a lower-dimensional manifold within the high-dimensional input space. This means that the data is structured in a way that distances and densities can be meaningfully measured within this lower-dimensional space. 

Readers familiar with the manifold assumption [73] and the
Johnson-Lindenstrauss lemma [74] will be nodding sagely at this
point– but the reductions seen in, say, SE data are startling. For example,
Chen, Kocaguneli, Tu, Peters, and Xu et al. found they could predict
for Github issue close time, effort estimation, and defect prediction,
even after ignoring labels for 80%, 91%, 97%, 98%, 100% (respectively)
of their project data labels [65],[70],[71],[72],[75]. Data sets
with thousands of rows can be modeled with just a few dozen samples
[76]– perhaps because of 
large amounts of repeated
structures [78] in the data from SE projects or
power laws [77].

my stuff with tables of data
