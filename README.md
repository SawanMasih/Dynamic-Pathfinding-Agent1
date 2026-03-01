# Dynamic Pathfinding Agent

## Project Overview
This project implements a **Dynamic Pathfinding Agent** that navigates a grid-based environment using:

- **A\*** Search  
- **Greedy Best First Search (GBFS)**

The environment supports dynamic obstacles that can appear while the agent is in motion, requiring **real-time path re-planning**.

---

## Features

- Dynamic grid sizing (user-defined rows × columns)  
- Random map generation with adjustable obstacle density  
- Interactive map editor to manually add/remove obstacles  
- Choose search algorithm: A* or Greedy Best-First Search  
- Choose heuristic: Manhattan Distance or Euclidean Distance  
- Dynamic obstacle handling with re-planning  
- GUI visualization (frontier, visited nodes, final path)  
- Metrics dashboard: nodes visited, path cost, execution time  

---

## Installation
pip install pygame

1. **Clone the repository:**

```bash
git clone https://github.com/SawanMasih/Dynamic-Pathfinding-Agent.git
cd Dynamic-Pathfinding-Agent