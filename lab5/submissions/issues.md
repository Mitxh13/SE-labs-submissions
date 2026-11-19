# Issues Found in `pos_system.py`

Baseline: Pylint **5.65/10**, Bandit **3 issues (1 Medium, 2 Low)**, Flake8 **12 issues**.
Final: Pylint **10.00/10**, Bandit **0**, Flake8 **0**.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| `eval()` on user input (B307 / W0123) | Security (Medium) | 27 | `apply_promo_code` runs `eval` on text typed by the user. Typing `__import__('os').system(...)` executes arbitrary commands. Remote/local code execution. | Replaced with a regex that only accepts `total <+ - * /> <number>`, mapped to `operator` functions. Anything else raises `ValueError`. |
| Mutable default argument (W0102) | Bug | 10 | `receipts=[]` is created once and shared across every call, so it grows forever and leaks state between bills. | Default changed to `None`; a new list is created inside the function. |
| Bare `except:` swallowing errors (W0702 / E722) | Bug | 16-17 | Hides every error (KeyError, TypeError...). Unknown items and bad quantities are silently priced at 0. | Removed the try/except. Explicit validation raises `ValueError` with a clear message. |
| Try / except / pass (B110, W0718) | Security (Low) / Quality | 31-34 | `update_stock` swallows all exceptions. Also the line `price_list[item] = price_list[item]` does nothing, so stock was never tracked. | Added a real `STOCK` dict; unknown items raise `ValueError`, handled by the caller. |
| Wrong output: negative quantity | Logic bug (no tool flags it) | 10-18, 49 | `("bottle", -4)` gives a total of **-630.00** and *reduces* sales. | Quantity must be an `int > 0`, else `ValueError`. |
| Wrong output: string quantity / negative tax | Logic bug (no tool flags it) | 14-19, 50 | `("pen", "2")` raises TypeError, which the bare except hides, so Bill 4 totals **0**. `tax_rate=-1` was also accepted. | Type check on quantity; `tax_rate` must be between 0 and 1. |
| Unknown item silently dropped | Logic bug (no tool flags it) | 14-17, 48 | "laptop" is not in the price list, so Bill 2 charges only for the bag. Customer undercharged without any warning. | Whole bill rejected with `Unknown item: laptop`. |
| Unclosed file / no encoding (R1732, W1514) | Quality / Resource leak | 37-39 | `open()` without `with` never closes the file; encoding left to platform default. | `with open(file, "a", encoding="utf-8")`. |
| Global statement + non-constant name (W0603, C0103) | Design | 7, 11 | Mutating module globals via `global` makes code hard to test and reason about. | State moved into a `STATE` dict that is mutated, not rebound. (A class would be the next step.) |
| Weak PRNG for receipt IDs (B311) | Security (Low) | 21 | `random.randint` can produce duplicate receipt numbers (only 9000 values). Not a real crypto risk here, but wrong tool. | Sequential receipt numbers (`#0001`, `#0002`...). |
| Unused imports `json`, `logging` (W0611 / F401) | Quality | 1, 3 | Dead imports. | Removed. |
| Unused variable `total` (W0612 / F841) | Quality | 26 | Assigned in `apply_promo_code` but never used (because of eval trick). | Removed with the eval fix. |
| Missing docstrings (C0114, C0116) | Style | 1, 10, 24, 29, 36, 41, 44 | No module or function documentation. | Added docstrings to the module and all functions. |
| `printSales` naming (C0103) | Style | 41 | camelCase, not PEP 8 snake_case. | Renamed `print_sales`. |
| Old-style `%` formatting (C0209) | Style | 21 | Could be f-string. | Converted to f-strings. |
| E302 / E305 blank lines | Style (Flake8) | 10, 24, 29, 36, 41, 44, 56 | Need 2 blank lines around functions. | Added. |
| E501 line too long (88 > 79) | Style (Flake8) | 21 | Receipt line exceeds 79 characters. | Wrapped. |
| `main()` runs on import | Design | 56 | Importing the module triggers the whole demo (and the `input()` prompt). | Added `if __name__ == "__main__":` guard. |
