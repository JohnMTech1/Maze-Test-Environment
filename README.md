Popperian-Expectations Maze Benchmark

A maze environment for evaluating a Popperian-Expectations
agent against learning-free and learning baselines under non-stationary,
partially-observable hazards. The Popperian Expectations agent forms, uses, and falsifies causal
expectations about the world. The other agents are
controls that share the same world, perception, and forward-simulation primitives
but differ in their decision algorithm.

---

## Requirements

- **Python 3.12+** 
- **pygame 2.6+** 

```bash
pip install pygame
```

Headless runs need no display; the harness sets the dummy SDL video/audio drivers
automatically.

```bash
# Linux / macOS
export SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy
```

---

## Quick start


```bash
# interactive window
MazeCode ACSOS 2026.py

# watch a specific agent solve mazes in a window
MazeCode ACSOS 2026.py mcts
MazeCode ACSOS 2026.py astar

# Headless paired benchmark: 500 seeds, every mode, one CSV row per run
MazeCode ACSOS 2026.py --compare all 500

# Headless quick aggregate table for one mode
MazeCode ACSOS 2026.py --bench popperian 9000
```

---

All agents share the identical world, the identical directional field-of-view
perception, and (where they simulate) the identical forward-simulation
primitives.


## Command-line interface

The first argument selects a sub-command. With no arguments, an interactive
window opens with the default `popperian` agent.

### `--compare` — paired per-run benchmark (primary experiment)

```
MazeCode ACSOS 2026.py --compare [mode|all] [n_attempts] [ticks] [csv]
```

```bash
MazeCode ACSOS 2026.py --compare popperian 500            # 500 PE runs
MazeCode ACSOS 2026.py --compare all 500                  # all 6 modes × 500 seeds
MazeCode ACSOS 2026.py --compare mcts 100 9000 mcts.csv   # 100 MCTS runs → mcts.csv
```



Opens a window. Controls:

| Key | Action |
|-----|--------|
| **WASD / Arrows** | Move (manual play) |
| **TAB** | Toggle agent mode (let the selected agent drive) |
| **R** | New maze |
| **ESC** | Quit |

In agent mode the run auto-restarts on win/death/timeout. A side panel shows
reused expectations and an "imagination" panel visualizes the internal-model
rollout.

---



