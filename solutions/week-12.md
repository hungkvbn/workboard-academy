# Gợi ý tuần 12

## Đáp án tự kiểm tra

1. Task version thay đổi khi nội dung một task được cập nhật; dùng kiểm tra ghi trên bản cũ. Schema version thay đổi khi cấu trúc database thay đổi; dùng chọn migration. Không tăng schema version sau mỗi sửa task.
2. Đồng hồ thiết bị có thể sai hoặc lệch nhau; thao tác đến server muộn không nhất thiết là ý định mới hơn. Cần quy tắc server/version rõ ràng và giao diện giải quyết xung đột khi cần.
3. Không. Database local lưu/truy vấn trên thiết bị; đồng bộ là giao thức riêng phải thiết kế nguồn dữ liệu, hàng đợi, retry và xử lý xung đột.

## Gợi ý lab

- **W12-L1:** quy tắc hạn rỗng xếp cuối có thể viết `ORDER BY due_at_ms IS NULL, due_at_ms, id`; tie-break ID giúp kết quả có thứ tự rõ ràng khi hạn bằng nhau.
- **W12-L2:** kiểm tra milliseconds và UTC lúc serialize, không so chuỗi hiển thị theo ngôn ngữ của máy. Query luôn có owner; xóa cache A khi logout phải không xóa nhầm dữ liệu B nếu bạn đã thiết kế nhiều phân vùng.
- **W12-L3:** fixture v1 cần được tạo bằng schema cũ thực sự, không tạo v2 rồi đổi con số phiên bản. Với Drift dùng công cụ migration và test theo phiên bản đang cài.

## Ví dụ sửa lỗi

```sql
-- Ý tưởng query đúng: truyền owner và status qua bindings của adapter.
SELECT id, title, due_at_ms
FROM tasks
WHERE owner_id = ? AND status = ?
ORDER BY due_at_ms IS NULL, due_at_ms, id;

-- Migration v1 -> v2 cho schema scratch của bài:
ALTER TABLE tasks
ADD COLUMN is_pinned INTEGER NOT NULL DEFAULT 0
CHECK(is_pinned IN (0, 1));
```

Không dùng nội suy `WHERE title = '$input'`. Tiêu đề có dấu nháy làm lộ lỗi ngay cả khi không có ý định tấn công. Khi chạy migration trong framework, để framework điều phối version/transaction; không chạy câu `ALTER TABLE` mỗi lần mở app.
