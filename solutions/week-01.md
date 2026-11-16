# Gợi ý và đáp án — Tuần 01

Chỉ mở sau khi đã chạy thử và ghi lại chỗ bị vướng. Đây là lời giải cho khái niệm và lỗi mẫu, không phải toàn bộ WorkBoard.

## Đáp án tự kiểm tra

1. `var` suy luận `name` là `String` từ giá trị ban đầu. Nó không thay đổi kiểu tĩnh sang `int` ở lần gán sau. Nếu cố ý chứa nhiều loại dữ liệu, cần thiết kế kiểu phù hợp và kiểm tra trước khi dùng.
2. Không. `final` ngăn gán tham chiếu khác; `list.add('A')` vẫn hợp lệ. Có thể dùng hằng hoặc danh sách không cho thay đổi khi mô hình yêu cầu.
3. Test có thể cố định thời gian, lặp lại và kiểm tra sát ranh giới. Hàm không âm thầm đổi kết quả theo lúc chạy.

## Gợi ý lab

- **W01-L1:** chuẩn hóa một lần rồi dùng cùng giá trị cho mọi kiểm tra. Test 120 chữ cộng hai khoảng trắng ở ngoài để bắt lỗi kiểm tra trước khi trim.
- **W01-L2:** xử lý các trường hợp loại trừ trước. Sau đó dùng `dueAt.isBefore(now)`; đừng dùng phép trừ ngày nguyên nếu yêu cầu là thời điểm.
- **W01-L3:** đặt nhập/xuất trong `bin/`, logic trong `lib/`. `DateTime.tryParse` giúp phân biệt ngày parse được với chuỗi không parse được. Nếu yêu cầu định dạng nghiêm ngặt, phải kiểm tra định dạng riêng.

## Sửa lỗi mẫu

Sai:

```dart
bool overdue(DateTime? dueAt, DateTime now) =>
    dueAt!.difference(now).inDays <= 0;
```

Có hai vấn đề: null gây lỗi; số ngày bị làm tròn nên nhiều thời điểm tương lai vẫn thành 0. Một phiên bản đúng cho quy tắc bài học:

```dart
bool isOverdue({
  DateTime? dueAt,
  required DateTime now,
  required bool isDone,
}) {
  if (isDone || dueAt == null) return false;
  return dueAt.isBefore(now);
}
```

Hãy tự viết test cho `dueAt == now`, một giây trước, một giây sau, null và trạng thái done. Nếu một bản sửa không giải thích được từng trường hợp, bạn chưa hoàn thành bài.
