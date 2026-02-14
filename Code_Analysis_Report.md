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
---

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

### Adam Khan - Unit tests
What I analyzed:
- `models/game_state.py`
- Core game logic including player management, game start validation, draw behavior, and turn progression
- Error handling and state transitions

Issues Found (You can add more than 3):

1. Issue: No automated tests covering GameState validation logic
   - Location: `models/game_state.py`
   - Problem: Critical validation rules (e.g., minimum player requirement, duplicate players) were not automatically tested.
   - Impact: Future changes could unintentionally break core game rules without being detected.
   - Suggested Fix: Add unit tests validating game start conditions and duplicate player prevention.

2. Issue: Turn advancement logic lacked verification
   - Location: `draw_and_pass()` method
   - Problem: No tests ensured that drawing correctly advances the turn.
   - Impact: A regression could cause incorrect turn order without detection.
   - Suggested Fix: Add unit tests verifying turn transitions after draw actions.

3. Issue: Limited coverage of phase-based state behavior
   - Location: `GameState.start_game()` and `draw_and_pass()`
   - Problem: No tests ensured that the game remains in the correct phase during valid actions.
   - Impact: Incorrect phase transitions could break gameplay flow.
   - Suggested Fix: Add tests confirming phase remains PLAYING after valid draws.
  
What I added (if applicable):
- Unit tests validating that the game cannot start with fewer than 2 players 
- Unit tests preventing duplicate players from being added
- Unit tests verifying turn advancement after drawing
- Confirmed that all tests pass with the existing test suite
---
