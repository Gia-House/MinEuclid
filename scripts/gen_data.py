"""Sinh bộ dữ liệu đo thực nghiệm vào tests/data/ (seed cố định, chạy lại ra đúng cùng dữ liệu).

Chạy từ thư mục gốc:  python -m scripts.gen_data
Tuỳ chọn:             --out <thư mục>   --max-n <n lớn nhất>

Mỗi mức kích thước n có SETS_PER_SIZE bộ cho mỗi kind:
  uniform   : ngẫu nhiên đều (trường hợp thường)
  thin_band : dải mỏng (trường hợp xấu nhất của chia để trị O(n log^2 n))
Muốn thêm kiểu dữ liệu (ví dụ trường hợp xấu của lưới băm): thêm một dòng vào KINDS.
"""
import argparse
import json
import os
import random
import time

from shared.datasets import DATA_DIR, write_points
from shared.generators import gen_thin_band, gen_uniform

SIZES = [500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]   # 8 mức
SETS_PER_SIZE = 5
BASE_SEED = 20261115
KINDS = {                      # tên kind -> (số hiệu để tạo seed, hàm sinh)
    "uniform": (0, gen_uniform),
    "thin_band": (1, gen_thin_band),
}


def make_seed(kind_id, n, index):
    """Seed duy nhất cho mỗi (kind, n, index): cố định, không phụ thuộc thứ tự sinh."""
    return BASE_SEED + kind_id * 10**8 + n * 10 + index


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=DATA_DIR)
    ap.add_argument("--max-n", type=int, default=None, help="bỏ các mức n lớn hơn giá trị này")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    sizes = [n for n in SIZES if args.max_n is None or n <= args.max_n]
    datasets = []
    t0 = time.perf_counter()
    for kind, (kind_id, gen) in KINDS.items():
        for n in sizes:
            for index in range(SETS_PER_SIZE):
                seed = make_seed(kind_id, n, index)
                points = gen(n, random.Random(seed))
                fname = f"{kind}_n{n}_{index}.txt"
                write_points(os.path.join(args.out, fname), points)
                datasets.append({"kind": kind, "n": n, "index": index, "seed": seed, "file": fname})

    manifest = {"base_seed": BASE_SEED, "sizes": sizes, "sets_per_size": SETS_PER_SIZE,
                "kinds": list(KINDS), "datasets": datasets}
    with open(os.path.join(args.out, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1)

    print(f"Đã sinh {len(datasets)} bộ dữ liệu ({len(KINDS)} kind x {len(sizes)} mức n x "
          f"{SETS_PER_SIZE} bộ) vào {args.out} trong {time.perf_counter() - t0:.1f}s")


if __name__ == "__main__":
    main()
