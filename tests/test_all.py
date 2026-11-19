"""Bộ kiểm thử chung: chạy MỌI giải thuật trong shared/registry.py trên cùng một bộ test.

Chạy từ thư mục gốc:   python -m tests.test_all
Giải thuật mới chỉ cần được khai báo trong shared/registry.py, không phải sửa file này.

Mỗi giải thuật được kiểm tra:
  1. Khoảng cách trả về bằng khoảng cách của vét cạn (so khoảng cách, không so cặp điểm vì có thể hòa).
  2. Tuân thủ luật giao diện: kiểu trả về, cặp điểm thuộc đầu vào, d khớp với cặp, None khi n < 2.
  3. Không sửa list đầu vào.
  4. Nhận counter (dict) mà kết quả không đổi, và counter["dist"] > 0 khi có đếm.
"""
import math
import random
import sys

from shared.generators import (gen_clustered, gen_collinear, gen_integer_small,
                               gen_same_x, gen_thin_band, gen_uniform)
from shared.registry import REFERENCE, load_algos

GENS = [gen_uniform, gen_integer_small, gen_collinear, gen_same_x, gen_clustered, gen_thin_band]
TOL = dict(rel_tol=1e-12, abs_tol=1e-12)


def check_contract(name, f, points, label, ref_d):
    """Chạy f trên points và kiểm tra mọi luật. ref_d = khoảng cách chuẩn (None nếu n < 2)."""
    where = f"[{name}] {label}"
    snapshot = list(points)

    res = f(points)
    assert points == snapshot, f"{where}: hàm đã sửa list đầu vào"

    if ref_d is None:
        assert res is None, f"{where}: n < 2 phải trả về None, nhận {res!r}"
        return
    assert res is not None, f"{where}: trả về None dù có >= 2 điểm"
    assert isinstance(res, tuple) and len(res) == 2, f"{where}: phải trả về (d, (p, q)), nhận {res!r}"
    d, pair = res
    assert isinstance(pair, tuple) and len(pair) == 2, f"{where}: cặp điểm phải là (p, q), nhận {pair!r}"
    p, q = pair
    assert p in points and q in points, f"{where}: cặp điểm không thuộc đầu vào"
    assert math.isclose(math.dist(p, q), d, **TOL), f"{where}: d={d} không khớp khoảng cách cặp trả về"
    assert math.isclose(d, ref_d, **TOL), f"{where}: d={d}, đáp án chuẩn={ref_d}"

    counter = {}
    res2 = f(points, counter)
    assert math.isclose(res2[0], ref_d, **TOL), f"{where}: bật counter làm đổi kết quả"
    assert isinstance(counter, dict) and counter.get("dist", 0) > 0, \
        f"{where}: counter không có khóa 'dist' > 0 sau khi đếm, nhận {counter}"


def run_case(algos, points, label):
    ref = algos[REFERENCE](list(points))
    ref_d = None if ref is None else ref[0]
    for name, f in algos.items():
        check_contract(name, f, points, label, ref_d)


def test_edges(algos):
    cases = {
        "rỗng": [], "1 điểm": [(1, 1)], "2 điểm": [(0, 0), (3, 4)], "3 điểm": [(0, 0), (1, 1), (5, 5)],
        "trùng": [(2, 2), (2, 2)], "trùng ở giữa": [(0, 0), (5, 5), (5, 5), (9, 9)],
        "toạ độ âm": [(-3, -4), (-3, -4.5), (10, 10), (-10, 3)],
        "cắt đường chia": [(-10, 0), (-0.1, 0), (0.1, 0), (10, 0), (-5, 7), (5, -7)],
        "trên đường chia": [(0, y) for y in range(10)] + [(-5, 3), (5, 8)],
        "tất cả trùng": [(4, 4)] * 20,
    }
    for label, pts in cases.items():
        run_case(algos, pts, label)


def test_random(algos):
    rng = random.Random(12345)
    for gen in GENS:
        for n in list(range(2, 40)) + [100, 300, 1000]:
            for _ in range(3):
                run_case(algos, gen(n, rng), f"{gen.__name__} n={n}")


def test_data_files(algos):
    """So khớp trên các file dữ liệu đo thật (n <= 2000). Bỏ qua nếu chưa chạy scripts.gen_data."""
    from shared.datasets import iter_datasets
    try:
        entries = list(iter_datasets(max_n=2000))
    except FileNotFoundError:
        print("  (bỏ qua test trên file dữ liệu: chưa có tests/data, chạy python -m scripts.gen_data)")
        return
    for entry, pts in entries:
        run_case(algos, pts, f"file {entry['file']}")


def main():
    algos, missing = load_algos()
    if REFERENCE not in algos:
        sys.exit(f"Không nạp được giải thuật chuẩn '{REFERENCE}': {missing}")
    print("Giải thuật được kiểm tra:", ", ".join(algos))
    for name, why in missing:
        print(f"  CHƯA NẠP ĐƯỢC {name}: {why}")

    for t in (test_edges, test_random, test_data_files):
        t(algos)
        print(f"  {t.__name__}: qua")
    print(f"OK: {len(algos)} giải thuật đều qua" + (f" ({len(missing)} chưa nạp)" if missing else ""))


if __name__ == "__main__":
    main()
