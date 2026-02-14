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

### Khalid – Test Coverage Analysis

What I analyzed:
- I ran an automated test coverage analysis using `pytest-cov` on the deck module.
- I reviewed the coverage report to identify any untested lines of code.
- The main file I focused on was `deck.py`.

1. Issue: One line in the deck module is not covered by automated tests.
   - Location: `deck.py` (line 88).
   - Problem: The coverage report shows 98% coverage, leaving one line untested.
   - Impact: This uncovered line could result in a small edge-case bug during gameplay if it behaves unexpectedly.
   - Suggested Fix: Add an additional unit test that specifically triggers and verifies this remaining line of code.

What I added:
- Installed `pytest` and `pytest-cov`.
- Generated a coverage report showing 98% coverage for `deck.py`.
- Verified that all 5 existing tests pass successfully.
  
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

### Rio Dumecquias – Cohesion and Coupling
What I analyzed:
- Files analyzed: `uno.py`, `controllers/lobby.py`, `deck.py`, `models/game_state.py`
- Reviewed the Class Diagram to confirm relationships between GameState, Deck, Card subclasses, and controller logic
- Focused on whether classes have a single responsibility (cohesion) and whether dependencies between components are minimal and properly layered (coupling).

Issues Found:

1. Issue: Lobby command module mixes multiple responsibilities
   - Location: `controllers/lobby.py`
   - Problem: This module handles command execution, lobby lifecycle management, shared state storage, and formatting logic in the same file. This reduces cohesion because one module performs several different roles instead of focusing on a single responsibility.
   - Impact: Harder to maintain as features grow. Increases risk that a change in formatting or state handling affects command behaviour.
   - Suggested Fix: Keep LobbyCog responsible only for handling commands and move lobby storage and lifecycle logic into a LobbyManager class.
  
2. Issue: Lobby lifecycle rules and storage are enforced across multiple command handlers instead of a single owner component.
   - Location: `controllers/lobby.py`: Line #50. (lobbies: Dict[int, Lobby] = {}
   - Problem: Lobby existence checks, permission rules, and phase checks, are implemented separately inside multiple commands. Each command directly accesses and modifies the shared global lobbies dictionary instead of keeping lifecycle responsibilities to a single manager.
   - Impact: Increased risk of inconsistent rule enforcement if one command is updated but others are not. Also repeats validation logic across commands and increases maintenance effort and potential for bugs.
   - Suggested Fix: Create a LobbyManager class that owns lobby storage and enforces all lifecycle rules into one place. Keep lobby.py focused only on handling Discord commands and calling the manager and remove direct access to global lobby state.

3. Issue:
   - Location: `models.game_state.py`
   - Problem: GameState currently manages several responsibilities including player management, phase transitions, deck interactions, and turn order/direction. While this works for the current scope, combining multiple responsibilities into one class reduces cohesion and makes the class more complex as gameplay rules expand.
   - Impact: Increases coupling to main part of system: changes to game rules or turn handling can affect several methods and components. Testing and maintenance will become difficult when adding features like new rules or penalties.
   - Suggested Fix: Improve GameState by separating some responsibilities into small helper components while keeping GameState as the main coordinator: 
   -    Create a TurnManager which handles the current player, direction, and advancing turns.
   -    Create a RuleEngine which validates move checks and special-cards.
---
