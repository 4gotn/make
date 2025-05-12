# Tutorial: Using `bl.py` for Multi-Objective Reasoning & Active Learning

This tutorial explains how to use the `bl.py` script for finding "good" solutions in your data when you have multiple, possibly conflicting, goals. We'll also see how **active learning** helps achieve this by looking at very few examples. We'll use the `auto93.csv` dataset, which is about cars.

## 1. The Goal: Finding the "Best" Cars with Multiple Objectives

Imagine you're looking for a car. You probably don't want just *any* car. You want one that's good in several ways:
* Low weight (`Lbs-` in `auto93.csv`)
* Good acceleration (`Acc+`)
* High miles per gallon (`Mpg+`)

The challenge is that these goals often conflict. A super lightweight car might not be the fastest, and a fuel-efficient car might have slower acceleration. This is where **multi-objective reasoning** comes in: finding items that offer the best overall balance or trade-off across these different criteria.

The `bl.py` script helps with this by looking at how you've named your columns in the CSV file. A `-` at the end means "minimize this," and a `+` means "maximize this."

## 2. How `bl.py` Measures "Goodness": The `ydist` Function

To compare different cars, `bl.py` needs a single score that summarizes how well a car meets all your objectives. This is done by an **aggregation function** called `ydist`.

Here's how `ydist` works conceptually:
1.  **Normalization**: It takes values from different scales (like weight in pounds and MPG) and converts them to a common 0-to-1 scale.
2.  **Distance from Ideal**: For each of your goals (e.g., `Lbs-`, `Acc+`, `Mpg+`), it measures how far the car's normalized value is from the "perfect" score (0 for minimization goals like `Lbs-`, and 1 for maximization goals like `Acc+` and `Mpg+`).
3.  **Combined Score**: It then combines these individual "distances from ideal" into one overall `ydist` score. **A lower `ydist` is better**, indicating the car is closer to the ideal across all your stated objectives.

To see this in action, you can run `bl.py` with an example command that processes your data and shows these distances. The `eg-data` command will load a CSV and print statistics for each column, including objective columns which are the basis for `ydist`.

```bash
python bl.py --data -f data/auto93.csv
```

This command processes `auto93.csv` and shows, among other things, the characteristics of the objective columns (`y` columns) from which `ydist` is calculated. While it doesn't directly output the `ydist` for each row via cthis specific command, the script contains `eg-ydist` (run via `test/ydata.py`) that does show this.

## Illustrative Output (Conceptual, if `eg-ydist` were run, showing best and worst):

```
Clndrs  Volume  HpX  Model  origin  Lbs-  Acc+  Mpg+  ydist
------  ------  ---  -----  ------  ----  ----  ----  -----
4       90      48   80     2       2085  21.7  40    0.17
4       91      67   80     3       1850  13.8  40    0.17
4       86      65   80     3       2019  16.4  40    0.17
4       86      64   81     1       1875  16.4  40    0.18
...
8       429     198  70     1       4341  10.0  20    0.77
8       350     165  70     1       3693  11.5  20    0.77
8       455     225  70     1       4425  10.0  10    0.77
8       454     220  70     1       4354  9.0   10    0.79
```


## Active Learning: Smarter Searching, Fewer Labels with actLearn

Manually checking every single car in a large dataset (i.e., "labeling" it with its performance metrics) can be very time-consuming or expensive. Active learning is a technique to find the best items by looking at only a small, intelligently chosen subset of the data.

`bl.py` uses the `actLearn` function for this. Here's the core idea:

- **Tiny Start:** It begins by evaluating a very small number of randomly selected cars (e.g., 4 cars, controlled by the `-s` or `--start` flag).
- **Learn and Query:** Based on what it learns from these initial cars, it decides which unlabeled car would be most informative to evaluate next. It does this by:
 - Maintaining a small set of the `best` cars found so far and a `rest` set.
 - For new candidate cars, it calculates how `like`ly they are to belong to the i
   `best` set versus the `rest` set (using a simplified Naive Bayes approach).
 - It then uses an "acquisition strategy" (set by `-a` or `--acq`, e.g., `xploit` to focus on known good areas, `xplore` to investigate uncertain areas) to pick the next car to "label" (i.e., calculate its `ydist`).
Iterate: It repeats this process, adding the newly evaluated car to its knowledge, and refining its understanding of what makes a "good" car.
Stop: It continues until it has evaluated a pre-set small number of cars (e.g., 32 by default, controlled by `-S` or `--Stop`).

The goal of actLearn is to identify a high-quality set of cars using far fewer evaluations than if you checked every single one.

## Running an Active Learning Experiment:

You can simulate this process using the `--actLearn`
command-line flag (which, internally, calles the `eg__actLearn`` function)
and. This will run the active learning strategy and report on how well it performed.


```bash
python bl.py --actLearn -f data/auto93.csv -S 32
```

## Interpreting the Output from eg-actLearn:

The script will output an "object" (a summary of results). Key things to look for:

- win: A score (ideally close to 1.0) indicating how close the best car found by actLearn is to the true best car in the entire dataset (if it were known). A higher "win" means active learning did a good job.
- mu1: The ydist score of the best car found by actLearn.
lo0, mu0, hi0: These show the minimum, average, and maximum ydist if all cars were evaluated. This gives you a baseline to compare mu1 against.
- stop: The number of cars actLearn actually "labeled" or evaluated (e.g., 32).
- ms: The average time in milliseconds per run.

An example output might look like:

```
o{:win 0.87, :rows 398, :x 4, :y 3, :lo0 0.17, :mu0 0.56, :hi0 0.93, :mu1 0.22, :sd1 0.06, :ms 5, :stop 32, :name auto93}
```

This (hypothetical) output would mean that by only looking at 32 cars, actLearn found a car with a ydist of 0.22. This is 87% of the way from the average car's score (0.56) towards the best possible score in the dataset (0.17). This demonstrates finding a very good solution with minimal labeling effort.

##  Why "Bare Logic"?

bl.py is termed "bare logic" because it implements these AI concepts (data handling, normalization, distance metrics, a simplified Bayesian approach for active learning) from fundamental principles. It avoids large external machine learning libraries, which makes the code:

- Transparent: Easier to see how calculations are done.
- Lightweight: Minimal dependencies.
- Educational: Good for understanding the core mechanics.

## To Experiment Further:

- Use the -f flag with python bl.py [example_function] to specify your own CSV data file. For example, python bl.py --actLearn -f path/to/your/data.csv.
- Change the -s (start evaluations) and -S (total evaluations) flags to see how performance changes with more or fewer labels. E.g., python bl.py --actLearn -s 10 -S 50.
- Test different active learning strategies with the -a flag (e.g., python bl.py --actLearn -a xplore).
- Explore other eg-* functions by running python bl.py -h to see what else the script can do. (Note: The example functions are prefixed with eg_ in the code, so on the command line, you'd use --functionName).

By using bl.py and its command-line flags, you can perform sophisticated multi-objective reasoning and leverage active learning to find good solutions efficiently, even when data labeling is a constraint.

