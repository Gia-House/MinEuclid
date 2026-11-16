"""Danh sách đăng ký giải thuật: nơi DUY NHẤT cần sửa khi thêm một giải thuật mới.

LUẬT GIAO DIỆN (mọi giải thuật phải tuân theo, test_all.py kiểm tra tự động):
  - Gọi:  f(points)  hoặc  f(points, counter)
        points  : list các tuple (x, y); hàm KHÔNG được sửa list này
        counter : None hoặc dict; nếu là dict thì hàm cộng dồn số phép toán vào đó
                  ("dist" = số lần tính khoảng cách, "cmp" = số lần so sánh khi sắp xếp/trộn)
  - Trả về: (d, (p, q)) với d = khoảng cách nhỏ nhất, p và q là hai điểm LẤY TỪ points,
            và d phải đúng bằng khoảng cách giữa p và q.
            Trả về None nếu có ít hơn 2 điểm.
  - Giải thuật ngẫu nhiên (lưới băm) có thêm tham số seed=None là được, test gọi không truyền seed.

CÁCH THÊM GIẢI THUẬT (ví dụ B thêm lưới băm): thêm một dòng vào ALGO_SPECS bên dưới, dạng
        ("tên_hiển_thị", "đường.dẫn.module", "tên_hàm")
"""
import importlib

ALGO_SPECS = [
    ("brute",     "shared.brute_force",      "closest_pair_brute"),
    ("dc_nlog2n", "chiadetri.divide_conquer", "closest_pair_dc_nlog2n"),
    ("dc_nlogn",  "chiadetri.divide_conquer", "closest_pair_dc_nlogn"),
    # B bỏ dấu # ở dòng dưới khi luoibam/ đã có file và hàm đã nhận tham số counter:
    # ("grid",    "luoibam.closest_pair_grid", "closest_pair_grid"),
]

REFERENCE = "brute"      # đáp án chuẩn khi so khớp


def load_algos():
    """Trả về (algos, missing): algos = {tên: hàm}, missing = [(tên, lý do)] cho cái chưa import được."""
    algos, missing = {}, []
    for name, module, attr in ALGO_SPECS:
        try:
            algos[name] = getattr(importlib.import_module(module), attr)
        except (ImportError, AttributeError) as e:
            missing.append((name, f"{type(e).__name__}: {e}"))
    return algos, missing
