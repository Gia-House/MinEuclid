"""Các bộ sinh dữ liệu dùng chung (kiểm thử và sinh dữ liệu đo).

Mọi hàm có cùng dạng: gen_xxx(n, rng) -> list các tuple (x, y), với rng là random.Random(seed).
Truyền cùng seed thì luôn ra cùng dữ liệu.
"""


def gen_uniform(n, rng):
    """Điểm ngẫu nhiên đều trong hình vuông [-1000, 1000]^2 (trường hợp thường)."""
    return [(rng.uniform(-1e3, 1e3), rng.uniform(-1e3, 1e3)) for _ in range(n)]


def gen_integer_small(n, rng):
    """Toạ độ nguyên nhỏ: rất nhiều điểm trùng và nhiều cặp hòa."""
    return [(rng.randint(-5, 5), rng.randint(-5, 5)) for _ in range(n)]


def gen_clustered(n, rng):
    """Điểm dồn thành 5 cụm."""
    centers = [(rng.uniform(-1e3, 1e3), rng.uniform(-1e3, 1e3)) for _ in range(5)]
    return [(c[0] + rng.gauss(0, 1), c[1] + rng.gauss(0, 1))
            for c in (rng.choice(centers) for _ in range(n))]


def gen_collinear(n, rng):
    """Tất cả điểm thẳng hàng theo trục x (y = 0)."""
    return [(rng.uniform(-1e3, 1e3), 0.0) for _ in range(n)]


def gen_same_x(n, rng):
    """Tất cả điểm cùng x (thẳng hàng theo trục y)."""
    return [(7.0, rng.uniform(-1e3, 1e3)) for _ in range(n)]


def gen_thin_band(n, rng):
    """Dải mỏng: x nằm trong [0, 1e-9], y rải đều trong [0, 1].
    Dải giữa của chia để trị chứa gần hết điểm ở mọi tầng đệ quy, và thứ tự theo x không liên quan
    đến thứ tự theo y, nên đây là trường hợp xấu nhất của bản O(n log^2 n)."""
    return [(rng.uniform(0, 1e-9), rng.uniform(0, 1)) for _ in range(n)]
