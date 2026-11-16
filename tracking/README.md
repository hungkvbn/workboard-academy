# Theo dõi tiến độ trên nhiều máy

`workboard-progress.json` dùng cùng định dạng với nút **Xuất tiến độ** trên trang học. Đây là tệp nên commit để mang tiến độ giữa các máy. Tệp khởi đầu để trống; tiến độ đã lưu trong trình duyệt của bạn không bị đọc hoặc thay thế tự động.

## Chỉ dùng giao diện

Cuối buổi học, xuất JSON từ trang học và lưu vào `tracking/workboard-progress.json`, rồi commit/push. Trên máy tiếp theo, pull và nhập tệp này vào trang học.

Chọn **Gộp** nếu muốn giữ các phần hoàn thành trên cả hai máy. Chọn **Thay thế bằng tệp** nếu tệp Git là bản chuẩn và bạn muốn giữ cả những ô đã bỏ chọn. Có thể xuất bản hiện tại để sao lưu trước khi thay thế. Tránh học đồng thời hai nơi rồi ghi đè tiến độ mà chưa đối chiếu.

## Dùng terminal nếu tiện

Tại thư mục gốc project, dùng Python 3.10+ (Windows có thể thay `python3` bằng `py -3`):

```bash
python3 tools/progress.py status
python3 tools/progress.py done W01-L1
python3 tools/progress.py done W01-L2
python3 tools/progress.py done W01-L3
python3 tools/progress.py accept 1
```

Chỉ xác nhận nghiệm thu sau khi đã thực sự đạt các điều kiện trong bài. Bỏ đánh dấu bằng `undo W01-L1`; bỏ nghiệm thu bằng `unaccept 1`.

Nhập tệp vừa tải từ trang học:

```bash
python3 tools/progress.py import /duong-dan/workboard-progress.json
```

Thay `/duong-dan/...` bằng đường dẫn thật. Mặc định gộp các lab đã hoàn thành. Thêm `--replace` để lấy trạng thái chính xác từ tệp, bao gồm bỏ chọn. Tệp không hợp lệ bị từ chối trước khi thay đổi dữ liệu hiện có.

```bash
python3 tools/progress.py export workboard-progress.json
```

Sau đó nhập tệp xuất này vào trang học. `progress.csv` và `backlog.csv` là bảng ghi thủ công độc lập; chúng không tự cập nhật khi sửa JSON. Nên chọn JSON làm nguồn tiến độ chính và dùng nhật ký/commit làm bằng chứng.

Xem quy trình Git đầy đủ trong [hướng dẫn nhiều máy](../project/git-and-multi-device.md).
