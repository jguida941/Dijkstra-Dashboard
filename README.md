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