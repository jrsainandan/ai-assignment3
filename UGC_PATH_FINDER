# UGV Path Planner
### Obstacle-Aware Grid Navigation using A* Algorithm

---

## Overview

This project simulates an **Unmanned Ground Vehicle (UGV)** navigating a battlefield grid to find the **shortest path** from a start node to a goal node.

The environment contains randomly generated obstacles with varying densities.  
The system uses the **A\* (A-Star) algorithm** with an appropriate heuristic to compute an optimal path.

---

## Features

- Grid-based battlefield simulation  
- Random obstacle generation (low / medium / high density)  
- 8-directional movement (including diagonals)  
- A* algorithm with Octile heuristic  
- Path visualization using Matplotlib  
- Robust input validation (re-entry on invalid input)  
- Detailed Measures of Effectiveness (MOE)

---

## Algorithm Used

The system uses:

**A\* (A-Star Algorithm)**

- Combines actual cost `g(n)` and heuristic `h(n)`
- Uses **Octile distance** for 8-direction movement
- Ensures optimal pathfinding

---

## Project Structure
```
├── path_planner.py
├── README.md
├── requirements.txt
├── .gitignore
```
---

## Setup Instructions

### 1. Install dependencies
pip install matplotlib


---

##  Sample Input
- Enter grid size: 20
- Enter density (low/medium/high): medium
- Enter start (x y): 0 0
- Enter goal (x y): 19 19

## Output Metrics (MOE)

The program outputs:

- Path (sequence of coordinates)
- Path Cost  
- Nodes Expanded  
- Computation Time  
- Straight-Line Distance  
- Optimality Ratio  
- Direction Changes  
- Obstacle Density  
- Search Space Coverage  

---
## Conclusion

This project demonstrates how **A\*** combined with proper heuristics can efficiently solve real-world navigation problems such as UGV path planning in obstacle-rich environments.
