# Gợi ý và đáp án — Tuần 17

## Đáp án tự kiểm tra

1. `now` được truyền vào khiến kết quả chỉ phụ thuộc dữ liệu đầu vào. Test có thể giữ thời điểm cố định và kiểm tra chính xác ranh giới, không bị thay đổi theo lúc chạy.
2. Khi tương tác là yêu cầu quan trọng: nhấn lưu hai lần chỉ tạo một request đang xử lý, hoặc retry tối đa theo chính sách. Kiểm tra mọi chi tiết gọi hàm làm test dễ vỡ khi refactor dù hành vi người dùng không thay đổi.
3. Test có thể chạy qua toàn bộ dòng code nhưng chỉ dùng công việc `todo`, bỏ sót `done`; hoặc không kiểm tra ranh giới bằng đúng `now`. Coverage cho biết nơi code đã chạy, không chứng minh mọi quy tắc đúng.

## Gợi ý lab

- **W17-L1:** viết bảng trước. Với quy ước bài học, chỉ công việc chưa hoàn thành có hạn trước `now` là quá hạn. Tìm kiếm `"REVIEW"` phải khớp tiêu đề `"Review PR"`; quy định rõ cách xử lý khoảng trắng của truy vấn.
- **W17-L2:** lưu một callback hoặc kết quả cấu hình trong fake. Dùng `Completer<List<WorkTask>>` để test tự quyết định lúc request hoàn tất; sau đó đóng đối tượng state/container nếu thư viện yêu cầu.
- **W17-L3:** đừng chỉ chụp kết quả xanh. PR cần ghi thay đổi sai nào đã làm test đỏ, tên test và vì sao lỗi ảnh hưởng người dùng.

## Ví dụ sửa lỗi

Sai:

```dart
bool overdue(DateTime? dueAt, DateTime now) =>
    dueAt != null && !dueAt.isAfter(now);
```

Hàm này coi hạn bằng hiện tại là quá hạn. Với yêu cầu của bài, sửa thành:

```dart
bool overdue(DateTime? dueAt, DateTime now) =>
    dueAt != null && dueAt.isBefore(now);
```

Test phải đặt `dueAt` và `now` cùng một instant, mong đợi `false`; thêm một ca trước đúng một microsecond, mong đợi `true`. Phần kiểm tra trạng thái `done` vẫn thuộc hàm nghiệp vụ đầy đủ. Không thay đổi yêu cầu sản phẩm chỉ để phù hợp với code hiện tại.
