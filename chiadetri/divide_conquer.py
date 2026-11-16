"""Giải thuật 2: Chia để trị cho bài toán cặp điểm gần nhất.

Hai bản:
  - closest_pair_dc_nlog2n : sắp lại dải giữa theo y ở MỖI bước trộn
                             T(n) = 2T(n/2) + O(n log n)  ->  O(n log^2 n)
  - closest_pair_dc_nlogn  : các nửa trả về danh sách đã sắp theo y, trộn như merge sort
                             T(n) = 2T(n/2) + O(n)        ->  O(n log n)

Giao diện giống brute_force.py: nhận list (x, y), trả (d, (p1, p2)) hoặc None nếu n < 2.

Bộ đếm (tham số counter là một dict, truyền None thì không đếm và chạy nhanh):
  counter["dist"] : số lần tính khoảng cách
  counter["cmp"]  : số lần so sánh khi SẮP XẾP / TRỘN (gồm cả lần sắp theo x ban đầu)
"""
import math
from functools import cmp_to_key
from shared.brute_force import closest_pair_brute

BASE = 3  # n <= 3 thì vét cạn (cơ sở của quy nạp)


def _dist(p, q, counter):
    if counter is not None:
        counter["dist"] = counter.get("dist", 0) + 1
    return math.dist(p, q)


def _sort(items, key, counter):
    """Sắp xếp theo key. Khi cần đếm thì dùng cmp_to_key để đếm mỗi lần so sánh;
    khi counter là None dùng sort gốc của Python để đo thời gian cho công bằng."""
    if counter is None:
        return sorted(items, key=key)

    def cmp(a, b):
        counter["cmp"] = counter.get("cmp", 0) + 1
        ka, kb = key(a), key(b)
        return (ka > kb) - (ka < kb)

    return sorted(items, key=cmp_to_key(cmp))


def _scan_strip(strip, best, pair, counter):
    """strip đã sắp theo y. Với mỗi điểm chỉ so với các điểm phía trên trong vòng best theo y
    (chứng minh: tối đa 7 điểm). Trả về (best, pair) mới."""
    for i in range(len(strip)):
        j = i + 1
        while j < len(strip) and strip[j][1] - strip[i][1] < best:
            d = _dist(strip[i], strip[j], counter)
            if d < best:
                best, pair = d, (strip[i], strip[j])
            j += 1
    return best, pair


# ---------------------------------------------------------------- bản O(n log^2 n)
def _rec_nlog2n(px, counter):
    n = len(px)
    if n <= BASE:
        return closest_pair_brute(px, counter)

    mid = n // 2
    midx = px[mid][0]                       # đường chia x = midx
    dl, pl = _rec_nlog2n(px[:mid], counter)
    dr, pr = _rec_nlog2n(px[mid:], counter)
    best, pair = (dl, pl) if dl <= dr else (dr, pr)

    if best == 0:                           # đã có hai điểm trùng, không thể tốt hơn
        return best, pair

    strip = [p for p in px if abs(p[0] - midx) < best]
    strip = _sort(strip, lambda p: p[1], counter)   # <-- sắp lại theo y ở mỗi bước: O(n log n)
    return _scan_strip(strip, best, pair, counter)


def closest_pair_dc_nlog2n(points, counter=None):
    if len(points) < 2:
        return None
    px = _sort(points, lambda p: p, counter)        # sắp theo x một lần (theo (x, y))
    return _rec_nlog2n(px, counter)


# ---------------------------------------------------------------- bản O(n log n)
def _merge_by_y(a, b, counter):
    """Trộn hai danh sách đã sắp theo y thành một danh sách sắp theo y: O(n)."""
    out = []
    i = j = 0
    while i < len(a) and j < len(b):
        if counter is not None:
            counter["cmp"] = counter.get("cmp", 0) + 1   # mỗi vòng lặp = 1 lần so sánh
        if a[i][1] <= b[j][1]:
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return out


def _rec_nlogn(px, counter):
    """Trả về (best, pair, danh_sách_điểm_sắp_theo_y)."""
    n = len(px)
    if n <= BASE:
        best, pair = closest_pair_brute(px, counter)
        return best, pair, _sort(px, lambda p: p[1], counter)   # tối đa 3 phần tử

    mid = n // 2
    midx = px[mid][0]
    dl, pl, yl = _rec_nlogn(px[:mid], counter)
    dr, pr, yr = _rec_nlogn(px[mid:], counter)
    py = _merge_by_y(yl, yr, counter)       # <-- trộn O(n), không sắp lại
    best, pair = (dl, pl) if dl <= dr else (dr, pr)

    if best == 0:
        return best, pair, py

    strip = [p for p in py if abs(p[0] - midx) < best]      # giữ nguyên thứ tự y
    best, pair = _scan_strip(strip, best, pair, counter)
    return best, pair, py


def closest_pair_dc_nlogn(points, counter=None):
    if len(points) < 2:
        return None
    px = _sort(points, lambda p: p, counter)
    best, pair, _ = _rec_nlogn(px, counter)
    return best, pair
