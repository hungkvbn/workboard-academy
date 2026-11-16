# Gợi ý tuần 09

Chỉ đọc sau khi đã thử từng lab và ghi lại vấn đề đang mắc.

## Đáp án tự kiểm tra

1. `read` không đăng ký cập nhật. Đọc filter bằng `read` trong render có thể hiển thị giá trị cũ cho tới khi widget tình cờ rebuild vì nguyên nhân khác. Dùng `watch` cho dữ liệu quyết định UI, `read` cho lệnh trong callback.
2. Giữ state trong widget khi nó thuộc tương tác cục bộ và có cùng vòng đời với widget: focus, controller nhập liệu, trạng thái mở rộng tạm thời. Có nhiều người dùng state hoặc cần giữ qua navigation là tín hiệu xem lại owner, không phải quy tắc tự động đưa tất cả lên global.
3. Lần đầu thất bại không có dữ liệu để hiển thị. Refresh thất bại có thể vẫn hiển thị bản cũ kèm thông báo và thử lại. Chọn rõ chính sách để test không dựa vào hành vi tình cờ.

## Gợi ý lab

- **W09-L1:** tạo bảng `state | owner | readers | reset`. `selectedStatus` là nguồn; `visibleTasks` và `doneCount` là kết quả tính toán. Kiểm tra số count sau sửa trạng thái công việc.
- **W09-L2:** nối fake trước backend. Đếm số lần gọi repository; một rebuild vì theme không được tăng số lần gọi tải dữ liệu. Chỉ thay policy refresh khi bạn có lý do và sửa test tương ứng.
- **W09-L3:** override provider repository, không override tất cả controller vì như vậy bạn bỏ qua chính logic cần test. Container phải được dọn sau test.

## Ví dụ sửa lỗi

```dart
// Sai: UI không đăng ký thay đổi.
final selected = ref.read(taskFilterProvider);

// Đúng trong phần dựng UI:
final selected = ref.watch(taskFilterProvider);

// Đúng trong callback của nút:
onPressed: () => ref.read(taskFilterProvider.notifier).select('done'),
```

Đây là các đoạn thay thế theo ngữ cảnh, không đặt hai khai báo `selected` trong cùng một scope. Test cần thay filter bằng notifier rồi xác nhận giao diện đổi mà không gọi `setState` thủ công ở widget cha.
