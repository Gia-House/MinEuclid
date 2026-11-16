"""Đọc/ghi bộ dữ liệu đo (dùng cho script sinh dữ liệu và script đo của B).

Định dạng file: mỗi dòng một điểm "x y" (số thực, ghi bằng repr nên đọc lại ra đúng giá trị cũ).
Thư mục dữ liệu có thêm manifest.json liệt kê mọi bộ: kind, n, index, seed, file.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "tests", "data")


def write_points(path, points):
    with open(path, "w", encoding="utf-8") as f:
        for x, y in points:
            f.write(f"{x!r} {y!r}\n")


def read_points(path):
    with open(path, encoding="utf-8") as f:
        return [tuple(map(float, line.split())) for line in f if line.strip()]


def load_manifest(root=DATA_DIR):
    with open(os.path.join(root, "manifest.json"), encoding="utf-8") as f:
        return json.load(f)


def iter_datasets(root=DATA_DIR, kinds=None, max_n=None):
    """Duyệt các bộ dữ liệu theo manifest. Trả về (entry, points) với
    entry = {"kind", "n", "index", "seed", "file"}.
    kinds: chỉ lấy các kind này; max_n: bỏ các bộ có n lớn hơn (ví dụ vét cạn chỉ chạy tới 10000)."""
    for entry in load_manifest(root)["datasets"]:
        if kinds is not None and entry["kind"] not in kinds:
            continue
        if max_n is not None and entry["n"] > max_n:
            continue
        yield entry, read_points(os.path.join(root, entry["file"]))
