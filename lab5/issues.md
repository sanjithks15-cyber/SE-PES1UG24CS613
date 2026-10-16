# Static Analysis Issues — Campus Shuttle (`shuttle_system.py`)

Baseline: Pylint 6.25/10, Bandit 2 Low, Flake8 10 violations. Line numbers refer to the original file.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Bare `except: pass` hides errors (Bandit B110, Pylint W0702, Flake8 E722) | Bug / Security | 29-30 | Any error inside `underused_routes()` is silently swallowed. A route with the text trip `"full"` crashes `sum()`, and an empty route divides by zero; both are hidden, so those routes are silently skipped. | Removed the try/except. Check `route["trips"]` is non-empty before averaging, and validate trip data when it is logged so bad values never get stored. |
| Invalid trip data accepted (not flagged by any tool) | Bug | 49-50 | `-6` passengers and the string `"full"` are stored as valid trips, which corrupts averages (R2 average becomes -1.0) and `fleet.json`. | `add_trip_log` now rejects unknown routes and any count that is not a non-negative whole number (bools too) with a `ValueError`; `main` reports "Rejected trip". |
| Weak random for driver choice (Bandit B311) | Security (Low) | 35 | `random.choice` is a predictable pseudo-random generator, flagged for security-sensitive use. | Switched to `secrets.choice`. |
| Mutable default argument `logs=[]` (Pylint W0102) | Bug | 11 | The same list is shared by every call, so logs from different calls pile up in one hidden list. | Default `logs=None`, create a new list inside the function. |
| Unhandled `KeyError` on removed/unknown route (not flagged by any tool) | Bug | 17, 20, 57-58 | `main` deletes R3 and then asks for R3's average, so the program crashes with `KeyError: 'R3'`. Typing an unknown route at the prompt crashes it too. | Added `get_route()` that raises a clear `ValueError("Unknown route: ...")`; `main` catches it and prints the message. |
| Files opened without `with` / encoding; pointless `global` (Pylint R1732, W1514, W0603) | Bug / Quality | 37-43 | File handles are not reliably closed (the read handle is never closed), no encoding is given, and the function re-reads the file it just wrote and reassigns the global `routes` for no benefit. | `with open(..., encoding="utf-8")` plus `json.dump`; removed the reload and the `global` statement. |
| Function name `assignDriver` and unused argument (Pylint C0103, W0613) | Quality | 33-35 | Not snake_case; `route_id` is accepted but never used. | Renamed `assign_driver`; it now checks the route exists, so the argument is used. |
| `%` string formatting (Pylint C0209) | Style | 13 | Old-style formatting that Pylint suggests replacing. | Converted to an f-string. |
| Missing docstrings (Pylint C0114, C0116) | Style | 1, 11, 16, 19, 23, 33, 37, 45 | Module and 7 functions have no documentation. | Added a module docstring and a docstring for every function. |
| Loop over dict keys then indexing (Pylint C0206) | Style | (new code) | `for r in routes: routes[r]` | Iterate with `.items()`. |
| `main()` runs on import (not flagged by any tool) | Bug / Design | 60 | Importing the module runs the whole demo (and writes `fleet.json`) as a side effect. | Guarded with `if __name__ == "__main__":`. |
| Missing blank lines (Flake8 E302, E305) | Style | 11, 16, 19, 23, 33, 37, 45, 60 | PEP 8 requires two blank lines around top-level definitions. | Added the blank lines. |
| Line too long, 82 > 79 (Flake8 E501) | Style | 13 | Log line exceeds the limit. | Wrapped the statement. |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 6.25/10 | 10.00/10 |
| Bandit | 2 Low issues | 0 issues |
| Flake8 | 10 violations | 0 violations |
