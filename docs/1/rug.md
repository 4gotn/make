# 🔍 DRY vs RUG: What's the Real Difference?

## 📊 Side-by-Side Comparison

| Concept           | **DRY** – *Don't Repeat Yourself*                            | **RUG** – *Repeat Until Good*                                  |
|-------------------|--------------------------------------------------------------|------------------------------------------------------------------|
| **Philosophy**     | Eliminate all duplication ASAP                               | Duplicate first; abstract later when patterns are clear          |
| **When to abstract?** | As soon as code looks similar                           | Only after the pain of duplication is obvious                    |
| **Typical outcome** | Early abstraction, may lead to brittle or overbuilt code    | Delayed abstraction, based on real-world use                     |
| **Risk**           | Premature abstraction that doesn’t generalize well           | Some up-front duplication, but avoids poor design                |
| **Guiding rule**   | “If you see repetition, refactor”                            | “If the duplication hurts, then refactor”                        |
| **Use case fit**   | Best for mature, stable systems                              | Best during prototyping or early development                     |
| **Mental model**   | *Structure-first*                                            | *Evidence-first*                                                 |

---

## 🎯 Key Insight

> **DRY** assumes you already know the right abstraction.  
> **RUG** helps you *discover* the right abstraction through repetition.

---

## 🧪 Example

### DRY (Too Early Abstraction)

```python
def filter_items(items, predicate):
    return [x for x in items if predicate(x)]
````

Works great—until you need more context in the predicate (e.g., index, external state). Now it's brittle.

---

### RUG (Wait and See)

```python
# First use
[x for x in items if x.age > 30]

# Second use
[x for x in items if x.name.startswith("A")]

# Later... pattern is clear → now abstract
```

You wait until abstraction is **obvious and helpful**, not just "dry."

---

## ✅ Bottom Line

* **Use DRY** when patterns are proven and stable.
* **Use RUG** when you’re still exploring solutions or iterating quickly.

> **RUG = Delay abstraction until the repetition hurts.**


