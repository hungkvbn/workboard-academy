# Gợi ý và đáp án — Tuần 02

## Đáp án tự kiểm tra

1. Map thích hợp cho tra cứu bằng ID; List thích hợp khi thứ tự và vị trí là phần của thao tác. Có thể giữ Map làm kho rồi tạo List để lọc/sắp xếp cho UI.
2. Cả không truyền tham số lẫn truyền null đều đi vào nhánh giữ giá trị cũ. Có thể dùng một cờ `clearDueAt`, một wrapper biểu diễn thay đổi, sentinel riêng hoặc các phương thức riêng `withDueAt`/`withoutDueAt`. Chọn cách đơn giản và viết test.
3. Generics giữ quan hệ kiểu giữa đầu vào và đầu ra. Analyzer phát hiện lỗi sớm; người dùng hàm không phải ép kiểu mỗi lần.

## Gợi ý lab

- **W02-L1:** chỉ cần một cách sao chép dễ hiểu. Không thêm code generation trước khi hiểu chính xác giá trị nào được giữ lại và giá trị nào được đổi.
- **W02-L2:** chia comparator thành các trường hợp cả hai null, chỉ bên trái null, chỉ bên phải null, rồi mới so ngày và ID. `toLowerCase` đáp ứng yêu cầu bài học; chưa giải quyết tìm kiếm theo ngôn ngữ hoặc bỏ dấu.
- **W02-L3:** đưa map thành trường private `_byId`. Cân nhắc `List.unmodifiable(_byId.values)`; các đối tượng bên trong cũng phải bất biến để tránh lỗ hổng thay đổi ngầm.

## Sửa lỗi mẫu

Sai:

```dart
List<int> ordered(List<int> source) {
  source.sort();
  return source;
}
```

Caller có thể đang dùng `source` theo thứ tự cũ. Sửa:

```dart
List<int> ordered(List<int> source) {
  final result = List<int>.of(source);
  result.sort();
  return result;
}
```

Test phải kiểm tra cả kết quả lẫn nguồn, ví dụ đầu vào `[2, 1]`, đầu ra `[1, 2]`, nguồn vẫn `[2, 1]`. Chỉ kiểm tra đầu ra sẽ bỏ sót tác dụng phụ.
