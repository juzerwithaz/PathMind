from flask import Flask, render_template, request, jsonify
from collections import deque
import heapq, time, sys

sys.setrecursionlimit(2000)

app = Flask(__name__)

# ── Constants ──────────────────────────────────────────────────────────────────

DIRS_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIRS_8 = DIRS_4 + [(-1, -1), (-1, 1), (1, -1), (1, 1)]

# Grid cell types: 0=empty, 1=wall, 2=sand, 3=water, 4=forest
TERRAIN_COST = {0: 1, 2: 3, 3: 5, 4: 8}


# ── Helpers ────────────────────────────────────────────────────────────────────

def get_neighbors(grid, r, c, diag=False, portals=None):
    """Yield valid neighbor coordinates, optionally with diagonal & portal support."""
    R, C = len(grid), len(grid[0])
    for dr, dc in (DIRS_8 if diag else DIRS_4):
        nr, nc = r + dr, c + dc
        if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] != 1:
            # Prevent diagonal corner-cutting through walls
            if abs(dr) + abs(dc) == 2:
                if grid[r + dr][c] == 1 or grid[r][c + dc] == 1:
                    continue
            yield (nr, nc)
    # Portal teleportation
    if portals:
        key = f"{r},{c}"
        if key in portals:
            pr, pc = portals[key]
            if 0 <= pr < R and 0 <= pc < C and grid[pr][pc] != 1:
                yield (pr, pc)


def move_cost(grid, r1, c1, r2, c2):
    """Cost to move from (r1,c1) to (r2,c2)."""
    base = TERRAIN_COST.get(grid[r2][c2], 1)
    d = abs(r2 - r1) + abs(c2 - c1)
    if d == 2:          # diagonal move
        return base * 1.414
    if d > 2:           # portal jump (flat cost)
        return 1.0
    return float(base)  # cardinal move


def heuristic(a, b, diag=False):
    """Manhattan (cardinal) or Chebyshev (diagonal) heuristic."""
    dr, dc = abs(a[0] - b[0]), abs(a[1] - b[1])
    if diag:
        return max(dr, dc) + 0.414 * min(dr, dc)
    return dr + dc


def reconstruct(parent, start, end):
    if end not in parent:
        return []
    path, cur = [], end
    while cur is not None:
        path.append(list(cur))
        cur = parent[cur]
    path.reverse()
    return path if path and path[0] == list(start) else []


# ── Search Algorithms ──────────────────────────────────────────────────────────

def bfs(grid, s, e, diag=False, portals=None):
    """Breadth-First Search — Queue (FIFO). Optimal for unweighted graphs."""
    queue = deque([s])
    parent = {s: None}
    order = []
    while queue:
        u = queue.popleft()
        order.append(list(u))
        if u == e:
            break
        for v in get_neighbors(grid, *u, diag=diag, portals=portals):
            if v not in parent:
                parent[v] = u
                queue.append(v)
    return order, reconstruct(parent, s, e)


def dfs(grid, s, e, diag=False, portals=None):
    """Depth-First Search — Stack (LIFO). Not guaranteed optimal."""
    stack = [s]
    parent = {s: None}
    order = []
    seen = set()
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u)
        order.append(list(u))
        if u == e:
            break
        for v in get_neighbors(grid, *u, diag=diag, portals=portals):
            if v not in parent:
                parent[v] = u
                stack.append(v)
    return order, reconstruct(parent, s, e)


def ucs(grid, s, e, diag=False, portals=None):
    """Uniform Cost Search — Priority Queue (min-heap). Dijkstra on grid."""
    heap = [(0, s)]
    dist = {s: 0}
    parent = {s: None}
    order = []
    seen = set()
    while heap:
        g, u = heapq.heappop(heap)
        if u in seen:
            continue
        seen.add(u)
        order.append(list(u))
        if u == e:
            break
        for v in get_neighbors(grid, *u, diag=diag, portals=portals):
            nc = g + move_cost(grid, u[0], u[1], v[0], v[1])
            if v not in dist or nc < dist[v]:
                dist[v] = nc
                parent[v] = u
                heapq.heappush(heap, (nc, v))
    return order, reconstruct(parent, s, e)


def dls(grid, s, e, limit, diag=False, portals=None):
    """Depth-Limited Search — DFS with a hard depth cutoff."""
    parent = {s: None}
    order = []
    seen = set()

    def recurse(u, depth):
        if depth > limit:
            return False
        seen.add(u)
        order.append(list(u))
        if u == e:
            return True
        for v in get_neighbors(grid, *u, diag=diag, portals=portals):
            if v not in seen:
                parent[v] = u
                if recurse(v, depth + 1):
                    return True
        return False

    recurse(s, 0)
    return order, reconstruct(parent, s, e)


def astar(grid, s, e, diag=False, portals=None):
    """A* Search — Priority Queue with f(n) = g(n) + h(n). Optimal."""
    heap = [(heuristic(s, e, diag), 0, s)]
    g = {s: 0}
    parent = {s: None}
    order = []
    seen = set()
    while heap:
        _, cost, u = heapq.heappop(heap)
        if u in seen:
            continue
        seen.add(u)
        order.append(list(u))
        if u == e:
            break
        for v in get_neighbors(grid, *u, diag=diag, portals=portals):
            nc = cost + move_cost(grid, u[0], u[1], v[0], v[1])
            if v not in g or nc < g[v]:
                g[v] = nc
                parent[v] = u
                heapq.heappush(heap, (nc + heuristic(v, e, diag), nc, v))
    return order, reconstruct(parent, s, e)


def greedy(grid, s, e, diag=False, portals=None):
    """Greedy Best-First — Priority Queue using h(n) only. Not optimal."""
    heap = [(heuristic(s, e, diag), s)]
    parent = {s: None}
    order = []
    seen = set()
    while heap:
        _, u = heapq.heappop(heap)
        if u in seen:
            continue
        seen.add(u)
        order.append(list(u))
        if u == e:
            break
        for v in get_neighbors(grid, *u, diag=diag, portals=portals):
            if v not in parent:
                parent[v] = u
                heapq.heappush(heap, (heuristic(v, e, diag), v))
    return order, reconstruct(parent, s, e)


# ── Route helpers ──────────────────────────────────────────────────────────────

ALGOS = {
    'bfs': bfs,
    'dfs': dfs,
    'ucs': ucs,
    'astar': astar,
    'greedy': greedy,
}


def _run(algo, grid, s, e, limit, diag, portals):
    """Run a single algorithm with unified interface."""
    if algo == 'dls':
        return dls(grid, s, e, limit, diag=diag, portals=portals)
    return ALGOS[algo](grid, s, e, diag=diag, portals=portals)


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/solve', methods=['POST'])
def solve():
    data = request.json
    grid   = data['grid']
    start  = tuple(data['start'])
    end    = tuple(data['end'])
    algo   = data['algorithm']
    limit  = int(data.get('limit', 25))
    diag   = bool(data.get('diagonal', False))
    portals = data.get('portals', {})
    waypoints = [tuple(w) for w in data.get('waypoints', [])]

    if algo not in ALGOS and algo != 'dls':
        return jsonify({'error': f'Unknown algorithm: {algo}'}), 400

    # Chain pathfinding through waypoints: start → w1 → w2 → … → end
    points = [start] + waypoints + [end]
    all_visited, all_path = [], []
    total_ms = 0

    for i in range(len(points) - 1):
        s, e = points[i], points[i + 1]
        t0 = time.perf_counter()
        try:
            visited, path = _run(algo, grid, s, e, limit, diag, portals)
        except RecursionError:
            return jsonify({'error': 'Recursion limit hit — reduce depth limit'}), 400
        total_ms += (time.perf_counter() - t0) * 1000

        all_visited.extend(visited)
        if path:
            # Merge path segments, avoiding duplicate junction nodes
            all_path = (all_path[:-1] if all_path else []) + path
        else:
            all_path = []
            break

    return jsonify({
        'visited': all_visited,
        'path': all_path,
        'stats': {
            'nodesExplored': len(all_visited),
            'pathLength':    len(all_path) - 1 if all_path else 0,
            'timeMs':        round(total_ms, 3),
            'found':         len(all_path) > 0,
            'optimal':       algo in ('bfs', 'ucs', 'astar'),
        }
    })


@app.route('/api/benchmark', methods=['POST'])
def benchmark():
    """Run all algorithms on the same grid and return comparative stats."""
    data = request.json
    grid    = data['grid']
    start   = tuple(data['start'])
    end     = tuple(data['end'])
    diag    = bool(data.get('diagonal', False))
    portals = data.get('portals', {})
    limit   = int(data.get('limit', 50))

    results = {}
    for algo in ['bfs', 'dfs', 'ucs', 'dls', 'astar', 'greedy']:
        t0 = time.perf_counter()
        try:
            visited, path = _run(algo, grid, start, end, limit, diag, portals)
            elapsed = (time.perf_counter() - t0) * 1000
            results[algo] = {
                'nodesExplored': len(visited),
                'pathLength':    len(path) - 1 if path else 0,
                'timeMs':        round(elapsed, 3),
                'found':         len(path) > 0,
                'optimal':       algo in ('bfs', 'ucs', 'astar'),
            }
        except RecursionError:
            results[algo] = {
                'nodesExplored': 0, 'pathLength': 0,
                'timeMs': 0, 'found': False, 'optimal': False,
                'error': 'Recursion limit',
            }
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=False, port=5000)