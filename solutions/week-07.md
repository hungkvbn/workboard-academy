# Gợi ý và đáp án — Tuần 07

## Đáp án tự kiểm tra

1. Index diễn tả vị trí, không diễn tả task. Sau sort, vị trí 0 có thể chứa một task khác; state được nhận diện theo key 0 có thể đi theo vị trí sai.
2. `const` tạo cấu hình hằng và cho phép dùng lại instance khi phù hợp. Nó không bảo đảm cả subtree không bao giờ build lại do các phụ thuộc khác, cũng không sửa các điểm nghẽn dữ liệu hoặc render.
3. Không. Build, layout và paint là các giai đoạn khác nhau; framework có thể tái sử dụng phần không thay đổi. Cần đo nguyên nhân cụ thể.

## Gợi ý lab

- **W07-L1:** dùng một State có biến `_expanded` trong từng TaskRow. Đầu tiên thử không key; sau đó đặt `ValueKey(task.id)` ở chính widget con mà danh sách quản lý. Chụp cùng một chuỗi thao tác để so sánh.
- **W07-L2:** builder nhận index rồi lấy task từ danh sách kết quả. Nếu kết quả đổi thứ tự, đọc `findChildIndexCallback`; ánh xạ task ID sang index giúp Flutter nối child cũ với vị trí mới. State quan trọng vẫn nên có nguồn dữ liệu rõ ràng.
- **W07-L3:** mỗi lần chỉ thay một điều để thấy tác động. Ghi số lượng item và thao tác; không viết “nhanh hơn” nếu chỉ thấy ít log hơn.

## Sửa lỗi mẫu

Sai:

```dart
for (var i = 0; i < tasks.length; i++)
  TaskRow(key: ValueKey(i), task: tasks[i])
```

Sửa cho một danh sách widget con trực tiếp:

```dart
for (final task in tasks)
  TaskRow(key: ValueKey(task.id), task: task)
```

Nếu có Padding trực tiếp bao ngoài, key ổn định cần gắn vào Padding hoặc một wrapper phù hợp ở cấp đó. Không gắn cùng key cho nhiều siblings. Với builder, chỉ đổi dòng key chưa đủ cho mọi yêu cầu giữ local state qua reorder; kiểm tra callback ánh xạ index và bài test hành vi.
