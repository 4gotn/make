# Why read this book?

This book is about talking a second look at SE and AI 
to find (and exploit) the inherent simplicity that exists "under the hood".

But why do that?  Why seek such alternatives? Shouldn't "Big AI," with its massive
datasets and CPU-intensive methods, be the undisputed champion? Not
necessarily.

Consider software project effort estimation. In some studies, older,
simpler methods like Support Vector Machines (combined with very basic 1970s-style simple text mining)
have outperformed complex Large Language Models (LLMs),
running significantly faster and producing
[more accurate results](refs.html#tawosi2023)
Astonishingly, a significant portion of research on these large
models doesn't even benchmark them against these more straightforward
alternatives.[^1] My own experiences have shown that lightweight
AI approaches can sometimes be orders of magnitude faster than their
heavyweight counterparts, 
[delivering comparable, if not superior, insights](../refs.html#majumder2018).

[^1]: I recently asked the authors
of a major literature review on the 
[use of large language models in SE](../refs.html#hou2024) "how many of those papers compared their methods
to standard approaches?". Shockingly, out of 229 papers,
only 13 (5%) papers compared their approach to non-neural baselines.

There are pressing reasons to champion these "Small AI" approaches:

1.  **Engineering Elegance & Cost:** There's an inherent satisfaction
in achieving more with less.  If everyone else can do it for $100,
I want to be able to do it for one cent. As shown in the rest of
this book, such large scale reductions are both possible and
astonished Smile to implement.

2.  **Innovation Speed:** When data analysis is expensive and slow,
iterative discovery suffers.
[Interactive exploration,
crucial for refining ideas, is lost](../refs.html#fisher2012). Waiting hours for cloud
computations only to realize a minor tweak is needed reminds me of
the frustratingly slow batch processing of the 1960s.

3.  **Sustainability:** The energy footprint of "Big AI" is alarming.
Projections show data center energy requirements doubling, with
some AI applications already consuming petajoules annually. 
Such exponential growth is [simply unsustainable](../refs.html#strubell2018).

4.  **Explainability & Trust:** Simpler systems are inherently
easier to understand, explain, and audit. Living in a world where
critical decisions are made by opaque systems that we cannot question
or verify is a disquieting prospect.

5.  **Customization & Skill Development:** Tailoring complex AI
models is a Herculean task. Fine-tuning often involves navigating
a bewildering array of "magic parameters," requiring 
[numerous slow experiments](../refs.html#nair2018). 
This "configuration crisis" means we often
underutilize our systems because their 
[complexity is a barrier](../refs.html#xu2015).
Furthermore, the steeper the learning curve, the slower we train
people to use these tools effectively.

6.  **Scientific Integrity:** The harder and more expensive it is
to run experiments, the more challenging reproducibility becomes.
This directly impacts the 
[trustworthiness of scientific findings](../refs.html#hutson2018).
History warns us about relying on inadequately scrutinized 
systems, as seen in failures like the Space Shuttle Columbia disaster,
where an initial "safe" assessment of an ice strike had catastrophic
consequences (the craft burned up on re-entry, 
[killing the entire crew](../refs.html#columbia2004).

7.  **The Power of Baselines:** I firmly believe in the necessity
of simple baseline systems. If a complex model is proposed, it
*must* demonstrate significant improvement over a simpler alternative
to justify its complexity and cost. More often than not, in the
process of building these baselines, I find the simpler approach
is not just a benchmark, 
[but the preferred solution](../refs.html#fu2017).

The exciting truth is that effective, simpler alternatives exist.
We can dramatically streamline AI techniques like active learning
and clustering. The crucial "signal" AI needs often resides in a
small fraction of the total data. The future, I argue, lies in
focusing on this "small data" with intelligent, nimble AI, rather
than attempting to boil the ocean with every query.


