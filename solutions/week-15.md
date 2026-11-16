# Gợi ý tuần 15

## Đáp án tự kiểm tra

1. Trang đã tải chỉ là một phần tập dữ liệu. Count có thể đúng cho phần đó nhưng sai nếu gắn nhãn tổng. Cần nhãn giới hạn phạm vi hoặc khả năng tổng hợp phía server.
2. Khi thao tác thường thành công và phản hồi ngay có lợi ích rõ, đồng thời nhóm có thể xử lý rollback, conflict và nhiều thao tác liên tiếp. Với luồng rủi ro cao hoặc logic phục hồi chưa có, chờ server có thể phù hợp hơn.
3. “Ngày 01/01” cần múi giờ và quy tắc thời điểm kết thúc ngày; “01/01 lúc 10:00 UTC” là một thời điểm tuyệt đối. Chuyển tùy tiện ngày thành nửa đêm UTC có thể đổi ý nghĩa ở múi giờ người dùng.

## Gợi ý lab

- **W15-L1:** dùng `now = 2026-01-01T10:00:00Z`; `2026-01-01T17:00:00+07:00` là cùng thời điểm. Task done và chưa có hạn không quá hạn dù các điều kiện khác.
- **W15-L2:** chụp now một lần trước `.where`. Khi timer dùng cập nhật trạng thái thời gian, dọn timer theo lifecycle; không cần timer mỗi hàng.
- **W15-L3:** cách dễ kiểm chứng ban đầu là disable thao tác cùng task khi đang ghi và dùng task/version server trả về. Nếu chọn optimistic update, lưu bản trước và đánh dấu operation ID để rollback cũ không ghi đè thao tác mới.

## Ví dụ sửa lỗi

```dart
// Sai ý nghĩa nếu danh sách chỉ có một trang:
// Text('Tổng quá hạn: ${overdue.length}');

// Đúng với phạm vi dữ liệu đang có:
final snapshotTime = clock().toUtc();
final overdue = loadedTasks.where((task) => countsAsOverdue(
  status: task.status,
  dueAt: task.dueAt,
  now: snapshotTime,
)).toList(growable: false);
// Nhãn UI: "Quá hạn trong danh sách đã tải: ${overdue.length}".
```

Nếu `status` trong model là enum, truyền `.name` hoặc đổi hàm dùng enum; thống nhất theo model dự án. Đoạn này không tự tải toàn bộ dữ liệu, và nhãn không được hứa điều đó.
