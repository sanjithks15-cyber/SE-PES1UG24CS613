# Catch the Falling Objects Lab

This project is a single-topic Catch game using **Pygame**. It
introduces students to collision timing, a classic list-mutation
pitfall, boundary handling, spawn pacing, and temporary power-ups,
using a small, readable object-oriented codebase.

---

## What's Provided

A working Catch game with:

- A basket the player moves left and right along the bottom of the
  screen
- Objects that spawn at the top at random x positions and fall
  straight down at a fixed interval
- A running score, a miss counter, and a game-over state once too many
  objects are missed

It has **one deliberate bug** (with two distinct symptoms) and
**three features** left for you to build. You are expected to
**analyze**, **interact with an AI assistant**, and **complete/fix**
the game to make it fully functional and more interesting.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**

---

## Getting Started

### Setup

1. Make sure you have Python 3.10+ installed.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the game:

```bash
python main.py
```

**Controls:** Left/Right arrows to move the basket.

---

## Tasks to Complete

Each task must be completed using an iterative process involving LLM
suggestions and your critical code review.

### Task 1: Fix the falling-object collision bug

> The basket is supposed to catch an object only once it has actually
> fallen down to basket height. In the current build, `is_caught` (in
> `game/collision.py`) only checks whether the object's x position is
> within the basket's left/right edges - it never checks height at
> all. That means an object can score the instant it spawns at the top
> of the screen, as soon as the basket happens to be under its x
> position, however far away it still is. Separately, the loop in
> `update()` (in `game/game_engine.py`) that checks for catches removes
> objects from the same list it's iterating over - a classic Python
> mistake that can silently skip checking an object on a given frame
> when two catchable objects are next to each other in the list. Fix
> both: catches should require the object to actually be at basket
> height, and the catch-checking loop should not skip entries.

### Task 2: Improve basket control

> The basket can currently be moved half off either edge of the
> screen, since its boundary check doesn't account for its own width.
> Fix the boundary handling so the basket always stays fully on
> screen, and make sure movement feels smooth and responsive even when
> a direction key is held down continuously.

### Task 3: Implement controlled object spawning

> Improve the spawning system so objects appear at varied horizontal
> positions and at varied intervals, rather than a fixed interval with
> a plain random x each time. Make sure objects never spawn outside
> the playable area, avoid repeatedly spawning in the same spot, and
> cap how many objects can be on screen at once so the game never
> becomes unplayable.

### Task 4: Add a temporary basket speed boost

> Add a speed-boost mechanic the player can activate during play that
> temporarily increases the basket's movement speed. Show a clear
> indication while the boost is active, and have the basket
> automatically return to normal speed once it expires.

---

## Expected Behavior

- An object should only be caught once it has genuinely reached the
  basket - not the moment its x position happens to line up with the
  basket, however high up it still is.
- If two catchable objects are near each other, both should be
  credited - neither should be silently skipped.
- Holding Left or Right continuously should never let the basket move
  off either edge of the screen.
- Objects should spawn at varied positions and timing, never
  overwhelming the screen or repeating the same spot constantly.
- The speed boost should be clearly visible while active and wear off
  on its own.

---

## Folder Structure

```
catch-falling/
├── main.py
├── requirements.txt
├── game/
│   ├── game_engine.py
│   ├── basket.py
│   ├── falling_object.py
│   ├── collision.py
│   └── renderer.py
└── README.md
```

---

## Submission Checklist

Submission is only the following three things:

- [ ] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [ ] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [ ] The Chat/LLM used page link, with the complete chat history
