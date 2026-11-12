"""Cặp điểm gần nhất bằng giải thuật ngẫu nhiên dùng lưới băm (Rabin).

Quy ước giao diện chung:
    - Điểm là tuple (x, y).
    - Hàm nhận list các điểm, trả về (khoảng_cách, (điểm_1, điểm_2)).
    - Nếu n < 2 thì trả về None.
"""
import math
import random


def cell(p, delta):
    """Ô chứa điểm p khi lưới có cạnh delta. Dùng floor để đúng với toạ độ âm."""
    return (math.floor(p[0] / delta), math.floor(p[1] / delta))


def build_grid(points, delta):
    """Xây lưới băm: khoá là ô (cx, cy), giá trị là danh sách điểm trong ô."""
    grid = {}
    for p in points:
        grid.setdefault(cell(p, delta), []).append(p)
    return grid


def closest_pair_grid(points, seed=None):
    n = len(points)
    if n < 2:
        return None

    # Xáo trộn một BẢN SAO để không làm đổi dữ liệu đầu vào.
    pts = list(points)
    random.Random(seed).shuffle(pts)

    # Hai điểm đầu: khởi tạo delta và lưới.
    delta = math.dist(pts[0], pts[1])
    best = (pts[0], pts[1])
    if delta == 0:                      # điểm trùng nhau: không thể nhỏ hơn 0
        return 0.0, best
    grid = build_grid(pts[:2], delta)

    # Pseudocode: i = 3..n (đánh số từ 1)  <=>  Python: i = 2..n-1 (đánh số từ 0)
    for i in range(2, n):
        p = pts[i]
        cx, cy = cell(p, delta)

        # Tìm điểm gần p nhất trong 9 ô lân cận.
        dmin = math.inf
        cand = None
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for q in grid.get((cx + dx, cy + dy), ()):
                    d = math.dist(p, q)
                    if d < dmin:
                        dmin = d
                        cand = (p, q)

        if dmin < delta:                # tìm được cặp gần hơn -> xây lại lưới
            delta = dmin
            best = cand
            if delta == 0:
                return 0.0, best
            grid = build_grid(pts[:i + 1], delta)
        else:                           # delta giữ nguyên -> chỉ chèn điểm mới
            grid.setdefault((cx, cy), []).append(p)

    return delta, best


def closest_pair_brute(points):
    """Vét cạn O(n^2), dùng để đối chiếu tính đúng."""
    n = len(points)
    if n < 2:
        return None
    best_d = math.inf
    best = None
    for i in range(n):
        for j in range(i + 1, n):
            d = math.dist(points[i], points[j])
            if d < best_d:
                best_d = d
                best = (points[i], points[j])
    return best_d, best