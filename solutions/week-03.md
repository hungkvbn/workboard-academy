# Gợi ý và đáp án — Tuần 03

## Đáp án tự kiểm tra

1. Không. `async` thay đổi cách trả kết quả và cho phép dùng `await`; tác vụ đồng bộ dài vẫn chạy trên isolate hiện tại. Cần đo rồi cân nhắc isolate cho công việc CPU phù hợp.
2. Nếu không `await`, lời gọi trả future trước khi lỗi xảy ra. Phạm vi `try` đã kết thúc. Dùng `await save()` bên trong `try`; nếu cố ý chạy độc lập phải có chiến lược xử lý lỗi và vòng đời rõ ràng.
3. Future có một lần hoàn thành; Stream phù hợp với chuỗi cập nhật, sự kiện hoặc dữ liệu đến từng phần theo thời gian.

## Gợi ý lab

- **W03-L1:** đặt thao tác parse/serialize thành hàm thuần để unit test riêng. Chỉ bắt trường hợp file không tồn tại để tạo danh sách rỗng; đừng bắt toàn bộ exception rồi bỏ qua. Test file hỏng cần kiểm tra nội dung gốc vẫn còn.
- **W03-L2:** `Completer` cho phép chủ động gọi `complete`/`completeError`. Không dùng độ trễ thật để chứng minh race condition vì test sẽ chậm và phụ thuộc lịch chạy.
- **W03-L3:** giữ giá trị `StreamSubscription` do `listen` trả về. `await subscription.cancel()` rồi mới khẳng định ngừng nhận sự kiện; đóng controller khi không còn bên phát.

## Sửa lỗi mẫu

Sai:

```dart
Future<void> persist() async {
  try {
    writeTasks();
    print('Đã lưu');
  } catch (error) {
    print('Lưu thất bại');
  }
}
```

Sửa trong cùng ngữ cảnh có hàm `writeTasks` trả `Future<void>`:

```dart
Future<void> persist() async {
  try {
    await writeTasks();
    print('Đã lưu');
  } catch (error) {
    print('Lưu thất bại');
    rethrow;
  }
}
```

`rethrow` giữ lỗi để caller quyết định dừng hay thử lại. Trong ứng dụng thực, UI có thể chuyển lỗi thành trạng thái hiển thị; không nhất thiết vừa log vừa ném ở mọi tầng. Hãy chọn nơi chịu trách nhiệm, tránh báo lỗi trùng.
