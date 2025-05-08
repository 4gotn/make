# Install the Software

To demonstrate the message of this book, we use the `BareLogic` tool. 

## What to Instakk First
 

|essential         | what|notes |
|:------------------:|:-----|:--|
| &#x2714;| bash  | e.g. inside VSCode, or in googlecode, or on a terminal in Linux or Mac, or the WSL for windows |
| &#x2714;| a good code editor | e.g.  vscode, or nvim (but consider the merits of something very lightweight like micro) | 
| &#x2714;| Python| version 3.13 (or later) |
| &#x2714;| Git |
| &#x2714;| Gawk | or awk, version 5 or later |
| &#x274C;| htop | or some other cpu minitor|
| &#x274C;| plylint | or some other static linter  |
| &#x274C;| docco | or some other simple documentation generator |

## Install code and data sets

Now you need some code and sample data sets


0. In a new directory, chack out our test data
   ```
   mkdir newDir # call it anything you like
   cd newDir
   git clone http://github.com/timm/moot
   # do not change directories. Goto step 1
   ```

1. Go to [https://github.com/timm/barelogic](https://github.com/timm/barelogic) and click the **Fork** button.

2. Clone your fork to your local machine:
    ```
    git clone https://github.com/YOUR_USERNAME/barelogic.git
    cd barelogic
    ```

3. Fetch all branches and check out the `v0.5` branch:
    ```
    git fetch origin
    git checkout -b v0.5 origin/v0.5
    ```

4. Create a new branch for your changes.
    ```
    git checkout -b my-feature
    ```
5. Test your install (see below)

6. Now you can start working. Make your edits in this directory. Frequently, push your changes to your on-line repo
    ```
    git add . # add waht ever is new
    git commit -m "Describe your changes"
    git push origin my-feature
    ```

## Test your install

### Are you running Python3?

```bash
python3 --version
```

You should see `Python 3.13` (or higher).

### Is your data in the right place?

```bash
cd barelogic/src
make stats
```

If this works, you should see something like this:

```bash
    x      y   rows
------ ------ ------
     3      1    197 ../../moot/optimize/config/wc+rs-3d-c4-obj1.csv
     3      1    197 ../../moot/optimize/config/wc+sol-3d-c4-obj1.csv
     3      1    197 ../../moot/optimize/config/wc+wc-3d-c4-obj1.csv
...
```

If this test fails, check you have installed gawk  and that the data is in the right place; i.e. from the src directory, ../../moot/optimize

### Is your active learner working?

```bash
cd barelogic/src
python3 -B bl.py --quick | column -s, -t
```
This will run an experiments. 30 times it will run the active learner using 8,16,20,30,40 samples, then statistically compare
the results. Best results will be marked with an `a`; second best `b`. and so on.

```bash
#['rows'   'lo'     'x'   'y'   'ms'   'b4'        40          20          16          8           'name']
[398       '0.17'   4     3     5      'c 0.56 '   'a 0.17 '   'a 0.21 '   'a 0.24 '   'b 0.26 '   'auto93']
```

Notice that everything is "a" from 16 samples and up. This is to say that there was no win here above 16 sampples.

### Is your tree learner working?

```bash
cd barelogic/src
python3 -B bl.py --tree
```

This test does the active learning (with 32 samples) then builds a tree from the labeled data. 

```bash
auto93.csv
o{:mu1 0.556 :mu2 0.265 :sd1 0.162 :sd2 0.064}
 d2h  win    n
---- ---- ----
0.50   -4   32
0.43   13   27    Volume <= 350
0.39   25   19    |  Model >  80
0.30   45    2    |  |  origin == 2 ;
0.36   31   13    |  |  origin == 3
0.29   49    2    |  |  |  Volume <= 85 ;
0.37   28   11    |  |  |  Volume >  85
0.36   31    7    |  |  |  |  Volume <= 91
0.36   31    5    |  |  |  |  |  Model >  81 ;
0.36   30    2    |  |  |  |  |  Model <= 81 ;
0.39   23    4    |  |  |  |  Volume >  91
0.39   24    2    |  |  |  |  |  Volume <= 107 ;
0.40   21    2    |  |  |  |  |  Volume >  107 ;
0.52   -8    4    |  |  origin == 1
0.44   12    2    |  |  |  Volume >  232 ;
0.60  -28    2    |  |  |  Volume <= 232 ;
0.55  -15    8    |  Model <= 80
0.52   -8    6    |  |  Volume <= 119
0.43   13    3    |  |  |  Clndrs >  3 ;
0.60  -28    3    |  |  |  Clndrs <= 3 ;
0.64  -38    2    |  |  Volume >  119 ;
0.86  -92    5    Volume >  350
0.84  -88    2    |  Volume <= 440 ;
0.87  -95    3    |  Volume >  440 ;
```

Here:

- `n` is the number of rows in each branch; 
- `;` denotes a leaf; 
- `d2h` is the distance of the mean score of the rows in each branch to an optimal zero point (so lower numbers are better)
- `win` normalizes d2h as `100 - 100 \* int(1 - (d2h-min)/(mu-min))` (so higher numbers are better and 100 is best).

### Is your tree learner working, on all data sets?

```bash
cd barelogic/src
time make trees
```

This will run the active learner (with 32 samples), then the tree learner, on all data sets.  On my machine (with 10 coy cores) this takes under a minute.
The thing to check here is that there are no crashes.

### How good are those trees?

This final test will launch 250 Python processes. So shut down everytime else you are doing before trying this. And it freezes your computer, just do a reboot.

```bash
cd barelogic/src
time make aftersReport
```
This takes  five minutes to run n my 10 core machine. 
If it works, then it prints a little report showing how good are the trees learned from 2,30,40,50 samples (selected
by active learning) at selecting for good examples in the unlabeled space.

```bash
samples 10 30 50  70  90
------- -- -- -- --- ---
     50 67 94 98 100 100
     40 70 91 97 100 100
     30 71 89 96 100 100
     20 72 86 95 100 100
```

This report says that (say) after 20 samples, these trees select for examples in the unlabeled space that are 95% (median) of the way to optimal. Which is pretty amazing. 

## Pull requests

If you do something really cool, or if you fix a bug in my code, I will ask you for a pull request

- On GitHub, go to your fork and click **"Compare & pull request"**.
- Set the pull request’s base to `timm/barelogic`, branch `v0.5`, and compare it with `YOUR_USERNAME/my-feature`.
- Add a descriptive title and message, then click **"Create pull request"**.

