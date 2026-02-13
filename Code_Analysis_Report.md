# Code Analysis Report – Task 5

## Findings

### <Name> – <Perspective Chosen>
What I analyzed:
- Files / commands / features reviewed

Issues Found (You can add more than 3):

1. Issue:
   - Location:
   - Problem:
   - Impact:
   - Suggested Fix:

2. Issue:
   - Location:
   - Problem:
   - Impact:
   - Suggested Fix:

3. Issue:
   - Location:
   - Problem:
   - Impact:
   - Suggested Fix:
  
What I added (if applicable):
- Added tests for valid, invalid, and edge case inputs.
- Verified tests pass.

### Alen Salaka – Cyclomatic Complexity
What I analyzed:
- I ran an automated cyclomatic complexity analysis across our entire Python codebase.
- I reviewed the highest-complexity methods and treated them as high bug risks.
- The main files I focused on were `models/game_state.py`, `controllers/lobby.py`, `deck.py`, and `uno.py`.

1. Issue: Under `GameState`, the `play` method handles too many decisions.
   - Location: `models/game_state.py` under `GameState.play`.
   - Problem: Performs too many checks and handles many special cases in one method, resulting in grade C and cyclomatic complexity = 11.
   - Impact: Difficult to understand, maintain and test.
   - Suggested Fix: Split into various helper functions.

2. Issue: Under `lobby.py`, the `format_card` function handles too many separate cases.
   - Location: `controllers/lobby.py` under `format_card`.
   - Problem: Many types to check, resulting in grade B and cyclomatic complexity = 10.
   - Impact: Easy to forget a case.
   - Suggested Fix: Use a `match` block in the function and add tests to confirm the outputs for each card type.

3. Issue: `_apply_effects_and_advance` handles too many card outcomes in one place.
   - Location: `models/game_state.py` under `GameState._apply_effects_and_advance`.
   - Problem: It applies all card effects and advances turns in one function, resulting in grade B and cyclomatic complexity = 9.
   - Impact: Easy to introduce bugs related to turns and effects.
   - Suggested Fix: Split into various per-card handlers and create tests for each of those effects.
---
