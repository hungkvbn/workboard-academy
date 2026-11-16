# Gợi ý và đáp án — Tuần 24

## Đáp án tự kiểm tra

1. Heap có thể chứa cache hợp lệ hoặc bộ nhớ chờ GC; runtime cũng có hành vi cấp phát riêng. Cần quan sát xu hướng và đường tham chiếu của đối tượng đáng lẽ hết vòng đời, trong cùng kịch bản lặp lại.
2. `async` hỗ trợ biểu diễn công việc bất đồng bộ. Phần CPU chạy đồng bộ trước/giữa các điểm chờ vẫn chiếm isolate hiện tại; parse lớn không tự chuyển sang nơi khác.
3. Tạo isolate, gửi dữ liệu và nhận kết quả có overhead. Main isolate rảnh hơn để xử lý UI dù tổng thời gian hoàn tất phép tính dài hơn. Đánh giá hai chỉ số riêng.

## Gợi ý lab

- **W24-L1:** ghi rõ màn hình nào tạo listener và nơi hủy. Nếu subscription do repository chia sẻ sở hữu, widget không nên tùy tiện đóng toàn bộ stream cho người dùng khác.
- **W24-L2:** sinh fixture một lần, dùng cùng chuỗi cho hai cách. Không tính thời gian sinh dữ liệu vào một bên nhưng bỏ qua ở bên còn lại. Kiểm tra kết quả parse trước khi kết luận tốc độ.
- **W24-L3:** pagination hoặc parse từng phần có thể xử lý nguyên nhân payload quá lớn. Bỏ qua kết quả cũ không đồng nghĩa đã hủy phép tính; ghi rõ ứng dụng có bảo đảm nào và chi phí còn lại.

## Ví dụ sửa lỗi

Sai: mỗi lần mở màn hình tạo một subscription mới nhưng không giữ handle để hủy; callback tiếp tục tham chiếu State sau khi đóng.

Hướng sửa với State sở hữu subscription:

```dart
StreamSubscription<List<WorkTask>>? subscription;

@override
void dispose() {
  final active = subscription;
  if (active != null) {
    unawaited(active.cancel());
  }
  super.dispose();
}
```

Cần import `dart:async`. Với nguồn có cleanup bất đồng bộ có thể thất bại, bổ sung xử lý lỗi phù hợp thay vì mặc nhiên bỏ qua; ví dụ minh họa tập trung vào quyền sở hữu handle. Việc `cancel()` không thể được `await` trực tiếp trong `dispose()` đồng bộ. Kiểm tra hành vi nguồn stream và không dựa vào `mounted` như cơ chế giải phóng tài nguyên.
