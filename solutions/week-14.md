# Gợi ý tuần 14

## Đáp án tự kiểm tra

1. Clock được tiêm cho phép đi đến thời điểm biên ngay lập tức và tái hiện đúng mỗi lần. Sleep làm test chậm, vẫn chịu ảnh hưởng scheduling và không bảo đảm đồng hồ dừng đúng mốc.
2. Khi số lượng hoặc thứ tự tương tác là yêu cầu, như không tạo nhiều request refresh đồng thời hoặc không gửi lại thao tác ghi không an toàn. Không nên đóng băng chuỗi lời gọi riêng tư chỉ vì implementation hiện có làm như vậy.
3. `[]` nói “đã đọc thành công và không có task”. Biến lỗi mạng thành `[]` làm UI báo sai và có thể ghi đè cache có dữ liệu bằng tập rỗng.

## Gợi ý lab

- **W14-L1:** dùng `() => DateTime.utc(2026, 1, 1, 10)` trong test. Chuẩn bị bảng ba thời điểm để người review nhìn thấy điều kiện bằng giờ được xử lý thế nào.
- **W14-L2:** response 409 không phải lỗi retry mù quáng. Giữ draft, đọc bản mới và cho người dùng chọn xử lý theo quy tắc tuần 22. Đừng log nguyên request header.
- **W14-L3:** dùng factory nhận kiểu repository để tái dùng test contract. Integration cần reset dữ liệu demo giữa test để không bị ảnh hưởng bởi lần chạy trước.

## Ví dụ sửa lỗi

```dart
// Sai: che lỗi, làm trống UI/cache.
// try { return await api.fetchTasks(); } catch (_) { return []; }

// Một lựa chọn: giữ lỗi có ý nghĩa và stack trace.
Future<List<WorkTask>> fetchTasks() async {
  try {
    return await api.fetchTasks();
  } on TimeoutException catch (error, stack) {
    Error.throwWithStackTrace(NetworkFailure(error), stack);
  }
}
```

Đoạn minh họa nằm trong adapter; cần import `dart:async`, model `WorkTask`, dependency `api` và định nghĩa `NetworkFailure` của dự án. UI xử lý lỗi ứng dụng thay vì biết `TimeoutException`. Có thể dùng kiểu Result thay exception; phải chọn một contract nhất quán và không giấu lỗi không dự kiến.
