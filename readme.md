# CS-171 Checkers Project
Current Version: 1.1.0.11052019
# 10/28/2019
Fixed a bug in **python** shell that Board parameter should be (col,row) instead of (row,col) 
# 10/29/2019
Fixed java copy constructor
# 10/30/2019
Fixed **cpp/java** undo function causing the wrong attributes of checkers. <br>
Fixed **cpp/java** undo black counter and white counter.<br>
Fixed **java** undo function (equal problem)<br>
Make counters in **cpp/java/python** more stable.<br>
# 11/05/2019
Added a new feature (**cpp/java/python**): "self play mode" which can be used to debug more efficiently.
# 11/14/2019
This update is about Poor AI:
1. Added support for 3.6.8
2. Fix some problem that causes Poor AI crashing in some rare cases.

# 11/30/2019
Added the Good AI.

# 12/05/2019
Blocked some invalid moves.

# 10/28/2026
Updated for OpenLab's default **Python 3.10** (no `module load` needed):
1. Rebuilt Poor AI, Average AI, and Good AI as Python 3.10 `.pyc` files (the old ones only loaded on Python 3.5/3.6). Their behavior is unchanged: the rebuilt code was checked to be bytecode-identical to the originals. Removed the duplicate `*_368` sample folders (the same AIs built for Python 3.6.8).
2. Rewrote the student manual: Python 3.10, connecting to OpenLab with VS Code Remote-SSH (UCI VPN required off campus), Python and C++ only, and corrected run commands. Java is no longer supported: removed the Java shell (`src/checkers-java`) and the java option in `submission.py`. `GeneralStudentManual.md` now points to the student manual for SSH setup.
3. The referee (`GameLogic.py` used by `AI_Runner.py`, and the Python shell's copy) now only accepts moves returned by `get_all_possible_moves`. Skipping an available capture, stopping a multi-jump early, single-square "moves", and malformed moves now count as an invalid move (a loss) instead of being accepted or crashing the referee.
4. `Move.from_str` parses move text instead of running it through `eval()`, so an AI's output can no longer run code in the referee.
5. Removed leftover developer files (`cmake-build-debug`, `.DS_Store`, Python 3.6 caches).
