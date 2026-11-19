"""So khớp 2 bản chia để trị với vét cạn (đáp án chuẩn). So KHOẢNG CÁCH, không so cặp điểm (có thể hòa)."""
import math
import random

from shared.brute_force import closest_pair_brute
from chiadetri.divide_conquer import closest_pair_dc_nlog2n, closest_pair_dc_nlogn

ALGOS = {"dc_nlog2n": closest_pair_dc_nlog2n, "dc_nlogn": closest_pair_dc_nlogn}


def check(points, label):
    ref = closest_pair_brute(list(points))
    for name, f in ALGOS.items():
        res = f(list(points))
        if ref is None:
            assert res is None, (name, label, res)
            continue
        assert res is not None, (name, label)
        d, (p, q) = res
        assert math.isclose(d, ref[0], abs_tol=1e-12), (name, label, d, ref[0])
        assert math.isclose(math.dist(p, q), d, abs_tol=1e-12), (name, label, "cặp sai")


from shared.generators import (gen_uniform, gen_integer_small, gen_collinear,
                               gen_same_x, gen_clustered, gen_thin_band)

GENS = [gen_uniform, gen_integer_small, gen_collinear, gen_same_x, gen_clustered, gen_thin_band]


def test_edges():
    check([], "rỗng")
    check([(1, 1)], "1 điểm")
    check([(0, 0), (3, 4)], "2 điểm")
    check([(0, 0), (1, 1), (5, 5)], "3 điểm")
    check([(2, 2), (2, 2)], "trùng")
    check([(0, 0), (5, 5), (5, 5), (9, 9)], "trùng ở giữa")
    check([(-3, -4), (-3, -4.5), (10, 10), (-10, 3)], "toạ độ âm")
    # hai điểm gần nhất nằm hai bên đường chia x = 0
    check([(-10, 0), (-0.1, 0), (0.1, 0), (10, 0), (-5, 7), (5, -7)], "cắt đường chia")
    # nhiều điểm nằm đúng trên đường chia
    check([(0, y) for y in range(10)] + [(-5, 3), (5, 8)], "trên đường chia")


def test_random():
    rng = random.Random(12345)
    for gen in GENS:
        for n in list(range(2, 40)) + [100, 300, 1000]:
            for _ in range(5):
                check(gen(n, rng), f"{gen.__name__} n={n}")


def test_counter_brute():
    for n in (2, 5, 50):
        c = {}
        closest_pair_brute([(i, i * i) for i in range(n)], c)
        assert c["dist"] == n * (n - 1) // 2


def test_counter_dc():
    """Đếm không được làm đổi kết quả. Trên dữ liệu dải mỏng (dải giữa chứa gần hết điểm ở mọi tầng),
    bản n log^2 n phải tốn nhiều so sánh hơn hẳn bản n log n, và tỉ lệ tăng theo n."""
    rng = random.Random(7)
    ratios = []
    for n in (1000, 4000, 16000):
        pts = gen_thin_band(n, rng)
        c1, c2 = {}, {}
        r1 = closest_pair_dc_nlog2n(pts, c1)
        r2 = closest_pair_dc_nlogn(pts, c2)
        assert r1[0] == closest_pair_dc_nlog2n(pts)[0]
        assert r2[0] == closest_pair_dc_nlogn(pts)[0]
        assert c1["cmp"] > 2 * c2["cmp"], (n, c1, c2)
        ratios.append(c1["cmp"] / c2["cmp"])
    assert ratios[0] < ratios[1] < ratios[2], ratios
    print("tỉ lệ cmp (n log^2 n / n log n) trên thin_band:", [round(r, 2) for r in ratios])


if __name__ == "__main__":
    test_edges()
    test_random()
    test_counter_brute()
    test_counter_dc()
    print("OK: tất cả test đều qua")
