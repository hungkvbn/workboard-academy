# Gợi ý và đáp án — Tuần 21

## Đáp án tự kiểm tra

1. Dữ liệu chưa đồng bộ có thể chỉ tồn tại trên thiết bị. Xóa nó làm mất nội dung người dùng, trong khi cache server thường có thể tải lại. UI và chính sách lưu trữ phải phân biệt hai loại.
2. Nó tránh công việc được cập nhật nhưng không có thao tác cần gửi, hoặc outbox tồn tại trong khi cập nhật local thất bại. Hai bước liên quan được commit hoặc rollback cùng nhau.
3. `taskId` định danh thực thể bền vững. `operationId` định danh một ý định thay đổi cụ thể và được dùng lại khi retry chính thao tác đó. Chỉnh sửa mới cần operation ID mới.

## Gợi ý lab

- **W21-L1:** giữ trường domain/server riêng với metadata local. Truy vấn UI phải có điều kiện `ownerId`; đừng chỉ lọc sau khi đã đưa dữ liệu của mọi người vào widget.
- **W21-L2:** đặt thao tác ghi công việc và ghi outbox trong cùng `db.transaction`. Với xóa, ẩn bản ghi khỏi danh sách bình thường nhưng giữ ID, owner và base version cần thiết.
- **W21-L3:** trạng thái phiên gồm token và danh tính chủ sở hữu; worker đồng bộ cũng phải kiểm tra nó. Test lỗi khi A còn pending rồi B đăng nhập sẽ chỉ ra các dependency đang sống quá lâu.

## Ví dụ sửa lỗi

Sai về tính nguyên tử:

```dart
await saveTaskLocally(task);
await appendOutbox(operation);
```

Hướng sửa, với các hàm DAO đã được bạn hiện thực trên cùng database:

```dart
await db.transaction(() async {
  await saveTaskLocally(task);
  await appendOutbox(operation);
});
```

Test cố ý làm `appendOutbox` ném lỗi, rồi đọc lại dữ liệu: task mới không được tồn tại hoặc task cũ phải giữ giá trị trước transaction. Đừng gọi HTTP bên trong transaction dài; transaction này chỉ bảo vệ ghi local. Thành công local và xác nhận server là hai sự kiện riêng biệt.
