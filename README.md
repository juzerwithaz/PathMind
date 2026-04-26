# AlgoMind 🧠

> **Visualize. Compare. Understand.**
> An interactive algorithm visualizer for pathfinding and sorting — built to make the *why* behind algorithms actually click.

🔗 **[Live Demo → path-mind-eight.vercel.app](https://path-mind-eight.vercel.app/)**

---

## What is AlgoMind?

AlgoMind is a web-based algorithm visualizer built as a DAA (Design and Analysis of Algorithms) project. Instead of staring at pseudocode and Big-O notation, you can **watch algorithms think** — step by step, on real grids and live arrays.

It has two modules: **PathMind**, which visualizes graph traversal and pathfinding on an interactive grid, and **Sorting**, which visualizes and benchmarks classic sorting algorithms on real arrays.

The core idea behind AlgoMind is simple — there is no single best algorithm. Every choice is a trade-off between speed, memory, accuracy, and context. AlgoMind makes those trade-offs *visible*, not just readable.

---

## PathMind — Pathfinding Visualizer

PathMind lets you draw walls, place weighted terrain, set a start and end point, and watch algorithms find their way through.

### Algorithms

**Breadth-First Search (BFS)** explores outward evenly in all directions and guarantees the shortest path on unweighted grids. This is the same logic LinkedIn uses to find your 1st and 2nd-degree connections, or how peer-to-peer networks locate the nearest node.

**Depth-First Search (DFS)** plunges as deep as possible before backtracking. It won't find the shortest path, but it's memory-efficient — making it useful for web crawlers mapping domain links or operating systems checking for deadlocks.

**Uniform Cost Search (UCS)** accounts for variable terrain costs and always finds the optimal path by cumulative cost. This is how GPS systems factor in toll booths and traffic delays to find your best route.

**Depth-Limited Search (DLS)** is a variant of DFS with a hard depth cap, useful for bounded search in large state spaces where you want to limit how far the algorithm looks.

**A\* Search** combines actual path cost with a heuristic estimate of remaining distance, making it both optimal and efficient. It's the backbone of Google Maps, robotics navigation, and most real-world pathfinding systems.

**Greedy Best-First Search** ignores path cost entirely and rushes straight toward the target using only a heuristic. It's fast but not always accurate — exactly what real-time game AI uses for enemy movement, where computing a perfect path for 100 enemies would crash the CPU.

### Features

PathMind supports **weighted terrain** — Sand (×3 cost), Water (×5 cost), and Forest (×8 cost) — so you can simulate real-world routing scenarios beyond simple wall-and-path grids.

**Compare Mode** lets you run up to 6 algorithms simultaneously on the same grid and watch how differently they explore. **Step-by-Step Mode** lets you move forward and backward through every single decision an algorithm makes, so nothing is a black box.

The **Heatmap Overlay** colors the grid based on how heavily each cell was explored, giving you an instant read on algorithm efficiency. **Maze Presets** let you generate complex environments instantly — Recursive Division, Prim's, Kruskal's, Cave Automata, Spiral, and Random walls are all built in.

You can also place **Waypoints** for multi-stop pathfinding and **Portals** for teleportation nodes. The **Benchmark Mode** auto-runs every algorithm and ranks them by execution time, nodes explored, and final path length. A **10-step guided Challenges mode** walks you through pathfinding concepts from scratch, and you can **Export, Import, and Screenshot** your grid setups to save or share them.

---

## Sorting Visualizer

The Sorting module visualizes six classic sorting algorithms on a live bar array, with full control over speed, size, and step granularity.

### Algorithms

**Merge Sort** runs in O(N log N) and is the gold standard for *stability* — it preserves the original order of equal elements. This matters in real systems like e-commerce platforms where you sort by price and then by rating and expect both to hold. It's also used for external sorting, where datasets are too large for RAM and must be processed in chunks on disk. The trade-off is memory — it requires O(N) extra space.

**Quick Sort** also runs in O(N log N) on average but sorts *in-place*, meaning it needs almost no extra memory. Its tight cache locality makes it faster than Merge Sort in practice on most real-world data, which is why it's the default sorting function in C, C++, and Java for primitive types. Game engines use it to sort polygons back-to-front for rendering. The trade-off is instability and a worst-case of O(N²) on bad pivot choices.

**Heap Sort** guarantees O(N log N) in all cases and uses O(1) space, making it the most memory-efficient of the fast sorts. It's used in priority queue implementations and OS scheduling systems where worst-case guarantees matter more than average-case speed.

**Insertion Sort** is O(N²) in general but exceptionally fast on nearly-sorted data. Modern hybrid algorithms like Python's Timsort actually switch to Insertion Sort for small chunks because the overhead of recursive algorithms isn't worth it at small sizes. It's also ideal for inserting live sensor data into an already-sorted dataset.

**Selection Sort** and **Bubble Sort** are O(N²) algorithms included as educational baselines. They're rarely used in production, but watching them compared against Merge or Quick Sort makes it immediately clear *why* better algorithms exist.

### Features

**Compare Mode / Auto Race** runs all six algorithms on the same array simultaneously so you can see the speed difference in real time. **Manual Step Mode** lets you move through every swap and comparison one at a time. **Benchmark Mode** ranks all algorithms by actual execution time on the same dataset. You can adjust array size and animation speed on the fly, and each algorithm comes with an **Analysis Panel** showing its complexity, stability, and real-world context.

---

## Tech Stack

AlgoMind is built with HTML, CSS, and Vanilla JavaScript on the frontend. The backend routing is handled by Flask (Python), and the app is deployed on Vercel.

---

## Getting Started Locally

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/algomind.git
cd algomind

# Install dependencies
pip install flask

# Run the app
python app.py

# Open in browser at http://localhost:5000
```

---

## Team

Built by **Sarthak**, **Juzer**, and **Animesh** as a DAA course project at **SRM Institute of Science and Technology**.

---

## License

MIT License — free to fork, extend, and build on.
