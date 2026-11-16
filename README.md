# MinEuclid – Đề 12: Cặp điểm gần nhất

Bài tập lớn môn Phân tích và Thiết kế Thuật toán. Cho n điểm trên mặt phẳng, tìm hai điểm có khoảng cách Euclid nhỏ nhất.

Nhóm cài đặt 3 giải thuật bằng Python, kiểm thử tính đúng, rồi đo thực nghiệm so với lý thuyết:

| Giải thuật | Thời gian | Người làm |
|---|---|---|
| Vét cạn | O(n²) | A |
| Chia để trị, sắp lại theo y mỗi bước | O(n log² n) | A |
| Chia để trị, sắp theo y một lần | O(n log n) | A |
| Ngẫu nhiên, lưới băm | kỳ vọng O(n) | B |

## 1. Cấu trúc thư mục

```
MinEuclid/
├── shared/            # dùng chung cả nhóm
│   ├── brute_force.py     # vét cạn, cũng là đáp án chuẩn khi kiểm thử
│   ├── registry.py        # danh sách giải thuật + luật giao diện (thêm giải thuật ở đây)
│   ├── generators.py      # các hàm sinh dữ liệu gen_*(n, rng)
│   └── datasets.py        # đọc/ghi bộ dữ liệu đo (cho script đo)
├── chiadetri/         # phần của A
│   ├── divide_conquer.py  # 2 bản chia để trị
│   └── test_dc.py         # kiểm thử so khớp với vét cạn
├── luoibam/           # phần của B (lưới băm + kiểm thử của B)
├── tests/
│   ├── test_all.py        # bộ kiểm thử chung cho mọi giải thuật
│   └── data/              # dữ liệu đo do scripts/gen_data.py sinh, seed cố định
├── scripts/
│   └── gen_data.py        # sinh dữ liệu đo; (đo và vẽ đồ thị: chưa có)
└── results/           # CSV và đồ thị                       (chưa có)
```

## 2. Môi trường

- Python 3.8 trở lên (dùng `math.dist`). Phiên bản và cấu hình máy dùng khi đo: *(điền khi đo thực nghiệm)*
- Phần kiểm thử chỉ dùng thư viện chuẩn, không cần cài thêm.
- Vẽ đồ thị cần `matplotlib`: *(điền khi có script vẽ)*

## 3. Giao diện chung của các hàm

Mọi giải thuật dùng cùng một kiểu gọi:

```python
from shared.brute_force import closest_pair_brute
from chiadetri.divide_conquer import closest_pair_dc_nlog2n, closest_pair_dc_nlogn

points = [(0, 0), (5, 5), (1, 1), (9, 2)]     # list các tuple (x, y)
d, (p, q) = closest_pair_dc_nlogn(points)     # d = khoảng cách nhỏ nhất, (p, q) = cặp điểm
```

- Đầu vào: list các tuple `(x, y)`.
- Đầu ra: `(khoảng_cách, (điểm_1, điểm_2))`, hoặc `None` nếu có ít hơn 2 điểm.
- Khi có nhiều cặp cùng khoảng cách nhỏ nhất, các giải thuật có thể trả về cặp khác nhau. Vì vậy khi kiểm thử ta so **khoảng cách**, không so cặp điểm.

### Bộ đếm phép toán

Mỗi hàm nhận thêm tham số `counter=None`, là một dict. Truyền `{}` vào thì hàm đếm số lần thực hiện từng loại phép toán:

```python
counter = {}
closest_pair_dc_nlogn(points, counter)
print(counter)    # ví dụ {'cmp': 12, 'dist': 5}
```

| Khóa | Ý nghĩa | Giải thuật có đếm |
|---|---|---|
| `"dist"` | số lần tính khoảng cách | cả 3 |
| `"cmp"` | số lần so sánh khi sắp xếp hoặc trộn (gồm cả lần sắp theo x ban đầu) | 2 bản chia để trị |

Để `counter=None` thì hàm không đếm và chạy nhanh hơn. Vì vậy khi đo thời gian không truyền `counter`, còn khi đếm phép toán thì chạy riêng một lần có `counter`.

## 4. Cách chạy

Luôn chạy từ thư mục gốc `MinEuclid/`, theo dạng `python -m`:

```
python -m tests.test_all           # kiểm thử chung: mọi giải thuật trong shared/registry.py
python -m chiadetri.test_dc        # kiểm thử riêng của chia để trị (gồm kiểm tra bộ đếm cmp)
```

Kết quả mong đợi: dòng `OK: ... đều qua`.

Thêm giải thuật vào bộ kiểm thử chung: chỉ cần thêm một dòng `("tên", "module", "hàm")` vào `ALGO_SPECS` trong `shared/registry.py`. Luật giao diện mà giải thuật phải tuân theo được ghi ở đầu file đó và được `tests/test_all.py` kiểm tra tự động.

```
python -m scripts.gen_data           # sinh dữ liệu đo vào tests/data/ (khoảng 3 giây, 72 MB)
```

*(Các lệnh dưới đây điền khi script tương ứng có)*

```
python -m luoibam.test_correctness   # kiểm thử lưới băm (của B)
python -m scripts.<do>                # đo, xuất CSV vào results/
python -m scripts.<ve_do_thi>         # vẽ đồ thị từ CSV
```

### Dữ liệu đo

`scripts/gen_data.py` sinh 80 bộ dữ liệu: 2 kiểu × 8 mức n × 5 bộ mỗi mức.

- Kiểu: `uniform` (ngẫu nhiên đều) và `thin_band` (dải mỏng, trường hợp xấu nhất của chia để trị O(n log² n)).
- Mức n: 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000. Vét cạn chỉ nên chạy đến n = 10000.
- Seed cố định (xem `manifest.json` trong thư mục dữ liệu). Chạy lại script luôn ra đúng cùng dữ liệu, từng byte.
- Thư mục `tests/data/` nặng khoảng 72 MB nên được bỏ qua trong git (`.gitignore`); ai cần thì chạy script để tạo lại.

Đọc dữ liệu trong code (dùng cho script đo):

```python
from shared.datasets import iter_datasets
for entry, points in iter_datasets(kinds=["uniform"], max_n=10000):
    ...   # entry = {"kind", "n", "index", "seed", "file"}
```

Không chạy trực tiếp `python chiadetri/test_dc.py`, vì Python sẽ không tìm thấy thư mục `shared`.

## 5. Kiểm thử tính đúng

Vét cạn là đáp án chuẩn (đơn giản nhất nên ít sai nhất). Với mỗi bộ dữ liệu, chạy giải thuật cần kiểm tra rồi so khoảng cách với vét cạn bằng `math.isclose`, đồng thời kiểm tra cặp điểm trả về có khoảng cách đúng bằng giá trị báo.

Bộ kiểm thử gồm:
- Test biên: rỗng, 1 điểm, 2 điểm, 3 điểm, điểm trùng, toạ độ âm, cặp gần nhất cắt đường chia, nhiều điểm nằm đúng trên đường chia.
- Test ngẫu nhiên, seed cố định, n từ 2 đến 1000, 6 kiểu dữ liệu: đều, số nguyên nhỏ, thẳng hàng, cùng x, cụm, dải mỏng.
- Test bộ đếm: vét cạn đếm đúng n(n-1)/2 lần; bật bộ đếm không làm đổi kết quả.

Kiểm thử qua nghĩa là chưa tìm ra input nào làm code sai. Tính đúng cho mọi input được chứng minh trong báo cáo.

## 6. Thực nghiệm

*(Điền khi có số liệu: số mức n, số bộ dữ liệu mỗi mức, số lần chạy, cách chọn seed, cấu hình máy, ý nghĩa các cột CSV.)*

Lưu ý khi đọc kết quả: trên dữ liệu ngẫu nhiên thường, hai bản chia để trị có số phép so sánh gần bằng nhau. Bản O(n log² n) chỉ chậm hơn rõ rệt trên dữ liệu "dải mỏng" (x nằm trong một dải rất hẹp, y rải đều), nên bộ dữ liệu đo có kiểu này làm trường hợp xấu nhất.

## 7. Nguồn tham khảo và công cụ AI

- Có dùng Claude (Anthropic) để hỗ trợ viết khung code chia để trị, bộ kiểm thử và giải thích thuật toán. Các thành viên đã đọc, chạy lại và hiểu mã nguồn của phần mình phụ trách.
- *(Bổ sung giáo trình, bài viết, bài luyện tập CSES/SPOJ... đã dùng)*

## 8. Phân công

| Hạng mục | A | B |
|---|---|---|
| Giải thuật | Vét cạn, chia để trị (2 bản) | Lưới băm |
| Kiểm thử | Bộ so khớp chung | Kiểm thử lưới băm |
| Đo và vẽ | | Script đo, vẽ đồ thị, xuất CSV |
| Báo cáo | Mục 1–4 | Mục 5–8 |

*(Điền họ tên và mã số sinh viên của A và B.)*