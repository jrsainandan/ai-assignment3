#  Dynamic Obstacle Environments using D* Lite Algorithm

---

## Overview

This project simulates an **Unmanned Ground Vehicle (UGV)** navigating a grid-based battlefield environment.  

The objective is to compute an **optimal path** from a user-defined start node to a goal node while avoiding obstacles.

Unlike static environments, this system handles **dynamic obstacles**, where the environment can change during execution.

---

## Algorithm Used

The implementation uses:

**D* Lite Algorithm**

- Incremental path planning algorithm  

- Efficient for dynamic environments  

- Updates only affected nodes when obstacles change  

- Avoids recomputing paths from scratch  

---

## Features

- Grid-based environment simulation  

- Random obstacle generation with controlled density  

- Guaranteed path existence using BFS validation  

- Dynamic obstacle updates during navigation  

- 8-directional movement (including diagonals)  

- Visualization using Matplotlib  

- Performance metrics (MOE)  

---

##  Project Structure

```

├── D*_Lite_Algo.py├── README.md

```



---

## 📦 Requirements

Install dependencies:

1. pip install matplotlib

---



##  Sample Input

. Enter grid size: 15  . Enter density(low/medium/high): medium . Enter start(x y): 0 0 . Enter goal(x y): 14 14



---## Measures of Effectiveness (MOE)The system evaluates performance using:- **Path Cost** → total traversal cost - **Steps** → number of nodes in path - **Computation Time** → execution time - **Optimality Ratio** → path cost vs straight-line distance - **Direction Changes** → smoothness of path



##  Conclusion

This project demonstrates how **D* Lite** efficiently handles dynamic path planning by updating paths incrementally, making it suitable for real-world autonomous navigation problems such as UGV movement in changing environments.
