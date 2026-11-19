"""Giải thuật 1: Vét cạn O(n^2) cho bài toán cặp điểm gần nhất.

Giao diện chung của nhóm:
  - points: list các tuple (x, y)
  - trả về (khoảng_cách, (điểm_1, điểm_2)), hoặc None nếu n < 2
  - counter: dict tùy chọn để đếm phép toán; counter["dist"] += 1 mỗi lần tính khoảng cách
"""
import math


def closest_pair_brute(points, counter=None):
    n = len(points)
    if n < 2:
        return None

    best = float("inf")
    pair = None
    for i in range(n):
        for j in range(i + 1, n):          # mỗi cặp (i, j) với i < j xét đúng 1 lần
            if counter is not None:
                counter["dist"] = counter.get("dist", 0) + 1
            d = math.dist(points[i], points[j])
            if d < best:
                best = d
                pair = (points[i], points[j])
    return best, pair
