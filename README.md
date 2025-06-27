# Dijkstra Path Visualizer

A PyQt6-based visualization tool for Dijkstra's shortest path algorithm. This application provides an interactive and animated visualization of the pathfinding process.

## Features

- Interactive graph visualization
- Animated pathfinding process
- Node and edge highlighting
- Start and target node selection
- Reset functionality

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

- Select start and target nodes from the dropdown menus
- Click "Run Visualization" to start the pathfinding process
- Click "Reset" to clear the visualization

## Project Structure

```
.
├── main.py                 # Application entry point
├── main_window.py          # Main window setup
├── ui/
│   ├── graph_view.py       # Graph visualization
│   ├── graph_node.py       # Node representation
│   ├── graph_edge.py       # Edge representation
│   └── controls_panel.py   # Control widgets
├── core/
│   └── dijkstra.py         # Algorithm implementation
└── requirements.txt        # Dependencies
```

# # Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)

**Copyright (c) 2025 Justin Guida**

This work is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International License**.

You are free to:

**Share** — copy and redistribute the material in any medium or format  
**Adapt** — remix, transform, and build upon the material  

Under the following terms:

 **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made. Credit must include:
- Name: *Justin Guida*
- Year: *2025*
- GitHub: [https://github.com/jguida941](https://github.com/jguida941)

 **NonCommercial** — You may not use the material for **commercial purposes** without **explicit written permission** from the author.

Additional terms:

- **You may not sell**, rebrand, or redistribute this work for profit.  
- Educational institutions and students may freely use, adapt, and build upon this work **for non-commercial academic use**, including course materials and presentations.
- Derivative works must also credit the original author clearly.

---

To view the full license, visit:  
[https://creativecommons.org/licenses/by-nc/4.0](https://creativecommons.org/licenses/by-nc/4.0)
