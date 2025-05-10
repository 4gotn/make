### 🧶 RUG (Repeat Until Good) Refactor Readiness Checklist

| ✅ Question                                                  | 🔍 What it Reveals                                                                 |
|-------------------------------------------------------------|------------------------------------------------------------------------------------|
| Have I duplicated this logic more than twice?               | Once = fine. Twice = maybe. Three+ = abstraction might help.                      |
| Are the duplicates really doing the same thing?             | Superficial similarity doesn’t mean they’re the same.                             |
| Do I understand the context and variation across use cases? | Prevents premature, brittle abstractions.                                         |
| Would refactoring make the code *clearer*, not just shorter?| Good abstractions improve readability, not just reduce LOC.                       |
| Is the duplication causing maintenance pain?                | Fixing bugs in multiple places = strong signal to abstract.                       |
| Will this abstraction be easy to test and reuse?            | If testing or usage becomes harder, abstraction might be premature.              |
| Is the code stable enough that this pattern won’t change?   | Avoid abstracting evolving logic too early.                                       |
| Do I have time budgeted for refactoring now?                | Don’t block shipping just for structural purity—especially near deadlines.        |
| Will the team understand and benefit from the abstraction?  | Clever but confusing abstractions hurt collaboration and maintainability.         |

> **Rule of Thumb**: "Repeat until it hurts. Then refactor."
