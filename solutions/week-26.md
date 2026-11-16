# Gợi ý và đáp án tuần 26

## Đáp án tự kiểm tra

1. Payload có thể cũ, bị sửa trong một luồng không tin cậy hoặc chứa dữ liệu thuộc tài khoản đã đăng xuất. Dùng ID để truy vấn lại nguồn dữ liệu với quyền hiện tại; cache cũng phải phân vùng theo tài khoản.
2. Chưa khôi phục xong không có nghĩa chưa đăng nhập. Gộp hai trạng thái gây redirect thừa, mất đích đến và nhấp nháy giao diện.
3. Không. Domain thật phải được kiểm soát và cấu hình file liên kết/xác minh tương ứng; package/application identity cũng phải khớp. Route parser thành công chỉ chứng minh một phần.

## Gợi ý lab

- **W26-L1:** viết một bảng gồm auth state, URI đầu vào, route kết quả. Test logic quyết định trước khi nối vào router. Giới hạn đích chờ ở route nội bộ hợp lệ.
- **W26-L2:** tạo ánh xạ ổn định giữa task ID và notification ID. Adapter nhận thời điểm cụ thể, giữ clock có thể thay thế trong test. Kiểm tra chính sách OS thực tế thay vì dựa vào việc timer Dart còn chạy.
- **W26-L3:** lưu khóa sự kiện đã xử lý hoặc dùng điều hướng thay thế có tính idempotent. Không loại bỏ mọi link cùng ID mãi mãi: người dùng vẫn có thể chủ động mở lại sau đó.

## Ví dụ sửa lỗi

Lỗi: mọi trạng thái không phải `signedIn` đều chuyển sang login.

```dart
String? redirectForSession(SessionState session, String currentPath) {
  if (session == SessionState.restoring) return null;
  if (session == SessionState.signedOut && currentPath != '/login') {
    return '/login';
  }
  return null;
}
```

Đây là phần quyết định đơn giản; trong app thực tế cần một màn chờ khôi phục và logic đích chờ. Test phải chứng minh `restoring → signedIn` không làm mất `/tasks/t-1`, còn `restoring → signedOut → signedIn` quay lại đích đã xác minh. Đừng lưu URL ngoài tùy ý vào tham số `returnTo` rồi điều hướng không kiểm tra.
