# Gợi ý và đáp án — Tuần 06

## Đáp án tự kiểm tra

1. Mở route diễn ra ngay nhưng kết quả chỉ có sau khi route đóng. Future diễn tả khoảng chờ này và kết quả tùy chọn được trả bởi pop.
2. Khi widget cần thích ứng với phần không gian cha cấp, chẳng hạn một panel cạnh sidebar. Chiều rộng màn hình có thể lớn nhưng panel vẫn hẹp.
3. Ảnh không cho biết nhãn semantics, thứ tự focus, trải nghiệm bàn phím hay phản ứng với cỡ chữ lớn. Cần thử hành vi, không chỉ nhìn hình.

## Gợi ý lab

- **W06-L1:** truyền ID hoặc dữ liệu cần thiết, đừng truyền cả State của màn hình trước. Sau await kiểm tra context còn mounted trước khi điều hướng hoặc hiện thông báo.
- **W06-L2:** lưu selected ID ở State chung cho hai bố cục. Nếu ID bị xóa thì chủ động bỏ lựa chọn; tránh giữ một bản sao task cũ không được cập nhật.
- **W06-L3:** nếu bật trình đọc màn hình, thao tác chạm có thể khác thường: chạm để chọn và chạm hai lần để kích hoạt. Ghi lại nhãn mà máy đọc, không chỉ tên bạn nghĩ nó sẽ đọc.

## Sửa lỗi mẫu

Sai:

```dart
final result = await Navigator.push<String>(context, route);
ScaffoldMessenger.of(context).showSnackBar(
  SnackBar(content: Text(result!)),
);
```

Người dùng có thể Hủy hoặc widget chứa context có thể đã bị dispose. Sửa theo ngữ cảnh `route` là `Route<String>`:

```dart
final result = await Navigator.push<String>(context, route);
if (!context.mounted || result == null) return;
ScaffoldMessenger.of(context).showSnackBar(
  SnackBar(content: Text(result)),
);
```

Đừng dùng thông báo này thay cho việc cập nhật dữ liệu thật. Hãy test Hủy, Lưu và đóng toàn bộ luồng trước khi kết quả về.
