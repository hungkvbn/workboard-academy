# Gợi ý tuần 10

## Đáp án tự kiểm tra

1. Client nằm trong quyền kiểm soát của người dùng. Họ có thể tự gửi HTTP request mà không đi qua nút. Backend cần xác minh cả danh tính và quyền trên đối tượng được yêu cầu.
2. 401 liên quan thông tin xác thực không còn hợp lệ theo contract; timeout có thể do đường truyền và không chứng minh token sai. Đăng xuất trên mọi timeout gây mất trải nghiệm và không giải quyết lỗi mạng.
3. Phải reset state/cache theo user, vô hiệu hóa kết quả request cũ và xử lý tác vụ offline đúng owner. Không chuyển hàng đợi chưa đồng bộ của A sang B.

## Gợi ý lab

- **W10-L1:** không đưa token vào `SignedIn` nếu widget chỉ cần user ID. Repository phiên giữ bí mật và API adapter sử dụng nó. Test cold start riêng với test đăng nhập tương tác.
- **W10-L2:** dùng `Future` dùng chung cho refresh đang chạy; tạo nó trước khi các caller khác truy cập, dọn trong `finally`. Mỗi request chỉ thử lại một lần sau refresh. Đặt bằng chứng `refreshCalls == 1` trong test fake, không chỉ xem log.
- **W10-L3:** lưu số thế hệ phiên. Khi đăng xuất/đổi user, tăng số; chỉ áp dụng kết quả nếu user và thế hệ vẫn khớp. Backend vẫn phải kiểm tra quyền; kỹ thuật client này chỉ bảo vệ state khỏi response muộn.

## Ví dụ sửa lỗi

```dart
// Trong controller phiên/danh sách; đây là phần kiểm tra response muộn.
final userAtStart = currentUserId;
final generationAtStart = sessionGeneration;
final tasks = await repository.fetchTasks();
if (userAtStart != currentUserId ||
    generationAtStart != sessionGeneration) {
  return;
}
applyTasks(tasks);
```

`currentUserId`, `sessionGeneration`, `repository` và `applyTasks` là thành viên controller của bạn. Không thay kiểm tra này bằng `mounted` duy nhất: widget có thể vẫn mounted trong khi tài khoản đã thay đổi. Tạo fake giữ response A bằng `Completer`, đổi sang B, rồi hoàn thành response A để chứng minh nó bị bỏ qua.
