"""Kiểm thử tính đúng: so khoảng cách của giải thuật lưới với vét cạn.

Chạy:  python test_correctness.py
Chỉ so KHOẢNG CÁCH (không so cặp điểm), vì có thể có nhiều cặp bằng nhau.
"""
import math
import random

from closet_pair_grid import closest_pair_grid, closest_pair_brute


# ---------- các bộ sinh dữ liệu ----------
def gen_uniform(n, rng):
    return [(rng.uniform(-100, 100), rng.uniform(-100, 100)) for _ in range(n)]


def gen_integer_small(n, rng):
    """Toạ độ nguyên nhỏ -> nhiều điểm trùng và nhiều cặp hoà."""
    return [(rng.randint(-5, 5), rng.randint(-5, 5)) for _ in range(n)]


def gen_clustered(n, rng):
    centers = [(rng.uniform(-100, 100), rng.uniform(-100, 100)) for _ in range(3)]
    pts = []
    for _ in range(n):
        cx, cy = rng.choice(centers)
        pts.append((cx + rng.gauss(0, 0.5), cy + rng.gauss(0, 0.5)))
    return pts


def gen_collinear(n, rng):
    return [(rng.uniform(-100, 100), 7.0) for _ in range(n)]


def gen_same_x(n, rng):
    return [(3.0, rng.uniform(-100, 100)) for _ in range(n)]


GENERATORS = {
    "uniform": gen_uniform,
    "integer_small": gen_integer_small,
    "clustered": gen_clustered,
    "collinear": gen_collinear,
    "same_x": gen_same_x,
}


# ---------- test ----------
def check(points, seed):
    d_grid, pair = closest_pair_grid(points, seed=seed)
    d_brute, _ = closest_pair_brute(points)
    assert math.isclose(d_grid, d_brute, rel_tol=1e-9, abs_tol=1e-12), (
        f"SAI: grid={d_grid}, brute={d_brute}, points={points}"
    )
    # cặp trả về phải có khoảng cách đúng bằng giá trị trả về
    assert math.isclose(math.dist(*pair), d_grid, rel_tol=1e-9, abs_tol=1e-12), (
        f"Cặp trả về không khớp khoảng cách: {pair} vs {d_grid}"
    )


def test_edge_cases():
    assert closest_pair_grid([]) is None
    assert closest_pair_grid([(1, 2)]) is None
    d, _ = closest_pair_grid([(0, 0), (3, 4)])
    assert d == 5.0
    d, _ = closest_pair_grid([(1, 1), (5, 5), (1, 1)])   # điểm trùng
    assert d == 0.0
    d, _ = closest_pair_grid([(-1, -1), (-1.5, -1.5), (10, 10)])  # toạ độ âm
    assert math.isclose(d, math.dist((-1, -1), (-1.5, -1.5)))
    print("Edge cases: OK")


def test_random(trials_per_gen=2000):
    rng = random.Random(12345)
    for name, gen in GENERATORS.items():
        for t in range(trials_per_gen):
            n = rng.randint(2, 50)
            pts = gen(n, rng)
            check(pts, seed=t)
        print(f"Random [{name}]: {trials_per_gen} test OK")


if __name__ == "__main__":
    test_edge_cases()
    test_random()
    print("TẤT CẢ TEST ĐỀU ĐÚNG")