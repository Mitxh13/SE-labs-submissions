# Reflection

> NOTE: the handout PDF I was given did not list the four reflection questions. These are the four standard ones for this lab. **Check them against your handout and rename/reorder if they differ.**

**1. Which issues were easiest and hardest to fix?**
Easiest were the mechanical ones: unused imports, blank lines, naming, docstrings. Flake8 and Pylint tell you the exact line and the fix is obvious. Hardest was `eval()`. Deleting it was not enough, because the feature (promo codes like `total * 0.9`) had to keep working. I had to design a safe replacement: a regex that accepts only `total <operator> <number>`, plus rejecting divide-by-zero. The bare `except` was also hard because removing it exposed real bugs I then had to handle properly.

**2. Did the tools report any false positives?**
Mostly no, but some were low value in context. Bandit B311 (`random` for receipt numbers) is not a real security risk in a shop receipt counter. It was still worth fixing, but for a different reason: random IDs from 1000-9999 can collide. Pylint's naming warning on `sales_total` is style rather than a bug. So tools can be technically right but not equally important, and severity needs human judgement.

**3. How would you integrate static analysis into a workflow?**
Run Flake8 and Pylint as a pre-commit hook so style problems never enter history. Run all three in CI (e.g. GitHub Actions) on every pull request and fail the build if Bandit finds Medium/High issues or the Pylint score drops below a threshold (e.g. 9.5). Keep a config file (`.pylintrc`, `setup.cfg`) so the team agrees on the rules.

**4. What tangible improvements did you see in quality, security and readability?**
Pylint went from 5.65 to 10.00, Bandit from 3 findings to 0, Flake8 from 12 to 0. More importantly, the program's behaviour changed for the better: a code-execution hole was closed, a -630 "sale" is rejected, unknown items are no longer silently free, and the log file is closed properly. Biggest lesson: **the tools did not catch the worst logic bugs** (negative quantity, string quantity, dropped items). I only found them by reading the program's output. Static analysis complements testing and review; it doesn't replace them.
