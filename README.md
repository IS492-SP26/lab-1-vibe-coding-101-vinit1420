# Ping-Pong Game: Cursor vs Gemini CLI – Tool Comparison

## Overview
This repository documents a comparative experiment where the same Ping-Pong game was implemented using **Python and Pygame** with two AI-assisted development tools: **Cursor** and **Gemini CLI**.  
The goal was to evaluate both tools based on workflow experience and output quality while implementing the same core game requirements.

Both versions of the game include:
- Game environment setup (playing field, paddles, ball)
- Player input handling
- Ball movement and collision detection
- Score keeping

---

## Tools Used
- **Tool A:** Cursor  
- **Tool B:** Gemini CLI  
- **Language:** Python  
- **Framework:** Pygame  

---

## Implementation Summary
- **Cursor** started from an empty GitHub repository and generated a complete two-player Ping-Pong game with minimal intervention.
- **Gemini CLI** started from a local folder and required explicit approval before every code change, resulting in a more controlled but slower workflow.

Both implementations were smooth, playable, and successfully committed to GitHub.

---

## Comparison Table

| Criteria | Cursor | Gemini CLI |
|-------|--------|------------|
| Starting Point | Empty GitHub repo clone | Local folder |
| Time to First Playable Game | ~2 minutes | ~5 minutes |
| User Interactions | ~5 clicks | ~12–13 confirmations |
| Workflow Style | Automatic, large changes | Step-by-step, diff-based |
| Game Mode | 2-player local | 1-player vs CPU |
| Instructions Display | In-game window | Terminal |
| Score Limit | 10 points | 5 points |
| Gameplay Dynamics | Ball speed increases over time | Constant speed, CPU does not miss |
| Customization Support | Automatic application | Explicit approval required |
| Code Readability | Well-commented | Clean, fewer comments |
| Exit Handling | ESC key supported | Window close only |
| Version Control | GitHub commit supported | GitHub commit supported |

---

## Analysis

### Speed of Generation
Cursor significantly outperformed Gemini CLI in speed, producing a complete and polished game in roughly two minutes. Gemini CLI took longer due to its confirmation-driven workflow but still produced a working game efficiently.

### Code Quality
Both tools generated similarly structured code. However, Cursor included more inline comments, making the logic easier to understand and modify. Gemini CLI's code was clean but less documented.

### Ease of Use
Cursor offered a low-friction, rapid-prototyping experience with minimal oversight. Gemini CLI provided greater transparency by showing diffs and requiring confirmation for each change, which improved control but increased interaction cost.

### Debugging and Error Handling
No functional bugs were encountered in either version. A minor usability difference was that the Cursor version allowed exiting via the ESC key, while the Gemini version required manually closing the window. Gemini CLI's workflow would likely be more helpful for debugging larger projects.

### Flexibility and Customization
Both tools handled visual customization (green table, white borders, red paddles) correctly. Cursor added progressive difficulty by increasing ball speed, while Gemini produced a fixed-difficulty CPU opponent. Gemini CLI provided finer-grained control over changes, whereas Cursor favored automation.

---

## Conclusion
- **Best for rapid prototyping:** Cursor  
- **Best for controlled, production-grade development:** Gemini CLI  

Cursor is ideal for quickly turning ideas into working prototypes, while Gemini CLI is better suited for scenarios where precision, review, and controlled changes are critical.

---

## How to Run

### Cursor version (2-player, local)
```bash
cd Cursor
pip install -r requirements.txt   # or: pip install pygame
python ping_pong.py
# On Windows if 'python' isn't in PATH: py ping_pong.py
```

### Gemini CLI version (1-player vs CPU)
```bash
cd Gemini/ping_pong_game
pip install pygame
python main.py
```
