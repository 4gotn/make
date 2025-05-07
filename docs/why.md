#  About this Book

Many, many 
people
assume that  Big AI (e.g. Large Language Models, or
LLMs) are the inevitable and best future path for Artificial
Intelligence.  

This book invites you to question that assumption.

To be clear: I use big AI, a lot,     for solo and tactical tasks
such as condensing my written arguments. But for
strategic tasks that might be critiqued externally, I need other
tools that are faster, simpler, and whose reasoning can be explained
and audited.  So while I do not want to replace big AI,  I want to
ensure we are   also supporting and exploring alternatives.

In software engineering (SE), there is very
little exploration of alternatives
to LLMs. A recent systematic review found 
only 5% of hundreds of SE LLM papers 
[considered alternatives](refs.html#hou2024). 
This a major methodological
mistake that ignores simpler and faster methods.  For instance, UCL
researchers found 
[SVM+TF-IDF methods outperform](refs.html#tawosi2023) standard
"Big AI" for effort estimation (100 times faster, with greater
accuracy) .

In SE, one  reason for asking if not LLM, then what?" is that
software   often exhibits "funneling": i.e. despite internal
complexity, software
[behavior converges to few outcomes](refs.html#menzies2007a), 
enabling
[simpler reasoning](refs.html#lustosa2025).  Funneling  explains how my "BareLogic"  active
learner can build
   models using  very little data
for (e.g.)  63   SE multi-objective optimization tasks from the
[MOOT repository](refs.html#menziesmoot).  
These   tasks are quite diverse and include
software process decisions, optimizing configuration parameters,
and tuning learners for better analytics. Successful MOOT modeling
results in better advice for project managers, better control of
software options, and enhanced analytics from learners that are
better tuned to the local data.

MOOT includes 100,000s of examples with up to  a thousand settings.
Each example is labelled with up to five effects. In practice,
obtaining  labels is  slow, expensive and error-prone. Hence the
 [task of active learners](refs.html#settles2009)
  like BareLogic is to find the best example(s),
after requesting the   least number of labels .  To do this,
 BareLogic labels  `N=4` rest examples, then it:

- Scores and sorts labeled examples by "distance to heaven" (where
"heaven" is the ideal target for optimization, e.g., weight=0, mpg=max)
- Splits the sort into `sqrt(𝑁)` `best` and `𝑁−sqrt(𝑁)` `rest` examples.
- Trains a two-class Bayes classifier on the `best` and `rest` sets.
- Finds the unlabeled example `X` that is most likely `best` via   
  `argmax(x):log(like(best|X)) - log(log(rest|X))`
- Labels `X`, then increments `N`.
- If `X` &lt; `Stop` labeled examples.

BareLogic was written for teaching purposes as a simple demonstrator
of   active learning. But in a result consistent with "funneling",
this
  quick-and-dirty tool achieves near optimal results using   a
  handful of labels.
As shown by  the histogram, right-hand-side of this figure, across 63
tasks:
-  eight labels yielded 62% of the optimal result; 
- 16 labels reached nearly 80%,   
- 32 labels approached 90% optimality, 
- 64 labels barely improves on 32 labels, 
- etc.

<center>
<img src="img/63.png">
<b>
Figure: 20 runs of BareLogic on 63 multi-objective tasks. <br>  
Histogram shows mean <tt>(1 − (most − b4.min)/(b4.mu − b4.min))</tt>.   
<tt>Most</tt>
is the best example returned by BareLogic.   
 <tt>b4</tt> are the untreated
examples.   
<tt>min</tt> is the optimal example closest to heaven.</b>
</center>

The lesson here is that achieving state-of-the-art results can ne
achieved with smarter questioning, not planetary-scale computation.
Active learning addresses many common  LLM concerns such as slow
training times, excessive energy needs, esoteric hardware requirements,
testability, reproducibility, and  explainability.

- The above figure  was created without billions of parameters. 
Active learners
need no vast pre-existing knowledge or massive datasets, avoiding
the colossal energy and specialized hardware demands of large-scale
AI.  
- Further, unlike LLMs where testing is slow and often irreproducible,
BareLogic's Bayesian active learning is fast (e.g., for 63 tasks
and 20 repeated trials, this figure was  generated in three minutes on
a standard   laptop).  
- Most importantly, active learning  fosters
human-AI partnership. 
  - Unlike opaque LLMs, BareLogic's results are
explainable via small labeled sets (e.g., `N=32`).
Whenever a label is required, humans can understand
and guide the reasoning. 
  - The resulting tiny regression tree models offer
concise, effective, and generalizable insights.

Active learning provides a compelling alternative to sheer scale in AI.

- Its ability to deliver rapid, efficient, and transparent results fundamentally
questions the "bigger is better" assumption dominating current thinking
about AI. 
- It tell us that intelligence requires more than just size.
- I am not the only one proposing weight loss for AI. 
  - The success of 
[LLM distillation](refs.html#Zeming2024) (shrinking huge models for specific purposes) shows that
giant models are not always necessary. 
  - Active learning pushes this idea even
further, showing that leaner, smarter modeling can achieve great results. 
  - So
why not, before we build the behemoth, try something smaller and faster?



## About the author:

Tim Menzies is a ACM Fellow, an IEEE Fellow, a Professor of Computer
Science at NC State University. He specializing in data-driven,
explainable, and minimal AI for software engineering. He serves on
the editorial board of IEEE Transactions on SE and as Editor-in-Chief
of the Automated Software Engineering journal. More info:
http://timm.fyi.









































