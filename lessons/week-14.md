# Tuần 14 — Dependency injection, fake và mô hình lỗi

**Đích đến:** tạo tình huống khó một cách chủ động và đưa lỗi từ hạ tầng thành hành vi rõ ràng trên UI. **Tiên quyết:** repository tuần 13, test fake và các trạng thái API.

## 1. Bài giảng

### Dependency injection là truyền thứ cần dùng

Nếu class tự tạo HTTP client, clock và bộ sinh ID bên trong, test không kiểm soát được chúng. Dependency injection đơn giản là nhận các phụ thuộc đó qua constructor hoặc composition point. Riverpod có thể ghép đồ thị dependency, nhưng nguyên tắc tồn tại ngay cả khi chỉ dùng constructor Dart.

Clock là ví dụ thường bị bỏ quên. Logic “quá hạn” gọi `DateTime.now()` trực tiếp sẽ đổi kết quả theo lúc chạy test. Nhận một hàm lấy giờ giúp kiểm tra thời điểm trước, đúng và sau hạn bằng cùng dữ liệu. Chỉ trừu tượng hóa thứ ảnh hưởng hành vi cần kiểm soát, không tạo interface cho mọi giá trị.

```dart
typedef Clock = DateTime Function();

bool isOverdue({
  required DateTime? dueAt,
  required bool isDone,
  required Clock clock,
}) {
  return !isDone && dueAt != null && dueAt.isBefore(clock().toUtc());
}
```

Hàm này định nghĩa “quá hạn” là trước thời điểm hiện tại; đúng bằng thời điểm hiện tại chưa quá hạn. Đó là quyết định nghiệp vụ cần ghi, không để phép so sánh tình cờ quyết định.

### Fake và mock phục vụ câu hỏi khác nhau

Fake là implementation giản lược có hành vi, như repository giữ task trong memory. Mock thường cấu hình câu trả lời và kiểm tra lời gọi. Fake phù hợp test nhiều trạng thái; mock hữu ích khi tương tác cụ thể chính là yêu cầu, chẳng hạn chỉ refresh một lần. Test xác minh mọi lời gọi nội bộ dễ vỡ khi refactor dù hành vi không đổi.

Fake phải được kiểm tra với contract chung. Nếu fake luôn update thành công nhưng remote từ chối version cũ, controller có thể “đạt test” mà hỏng khi chạy thật. Không cần fake mô phỏng toàn bộ backend; cần nói rõ giới hạn và giữ integration test cho ranh giới quan trọng.

### Lỗi kỹ thuật và lỗi người dùng có thể xử lý

Socket exception, JSON sai và HTTP 409 không nên trở thành cùng chuỗi “Có lỗi”. Phân loại tối thiểu: validation, unauthenticated, forbidden/not-found theo contract, conflict, network, server và unexpected. UI cần hành động phù hợp: sửa dữ liệu, đăng nhập lại, tải bản mới, thử lại hoặc báo lỗi.

Giữ thông tin chẩn đoán như stack trace ở tầng logging phù hợp nhưng tránh token và dữ liệu nhạy cảm. Thông báo cho người dùng không nên là toàn bộ stack trace. Không nuốt lỗi bằng danh sách rỗng, vì danh sách rỗng là một kết quả hợp lệ khác hẳn không tải được.

### Cancellation không phải lỗi cần báo động

Người dùng đổi tìm kiếm hoặc đóng màn hình là hành động bình thường. Nếu request cũ bị hủy, không nên hiện banner lỗi toàn app. Phân biệt lỗi còn liên quan đến ý định hiện tại với kết quả của thao tác đã bị thay thế.

## 2. Ba bài thực hành

### W14-L1 — Tiêm clock và ID

Tách bộ sinh ID và clock ra khỏi phần tạo task. Fake clock cố định ở `2026-01-01T10:00:00Z`, bộ sinh ID trả `task-demo-001`. Đầu ra draft có ID dự đoán được; test quá hạn với thời điểm 09:59, 10:00, 10:01 và `null`. Không dùng clock client để tự cấp version server.

### W14-L2 — Bảng ánh xạ lỗi

Viết bảng HTTP/transport → lỗi ứng dụng → UI → hành động tiếp theo. Triển khai ít nhất lỗi mạng, validation và conflict. Fake tạo mỗi trường hợp; xác nhận retry không có ở lỗi cần sửa đầu vào và conflict không bị báo là thành công.

### W14-L3 — Contract test cho hai implementation

Chạy cùng nhóm test trên in-memory repository và adapter nối mock API cho các hành vi hỗ trợ chung: tạo, đọc, sửa version mới và từ chối version cũ. Đánh dấu rõ test local không mạng và integration test cần server. Không ép những capability chưa hỗ trợ vào contract giả.

## 3. Nghiệm thu và tự kiểm tra

- [ ] Test thời gian dùng clock cố định, không phụ thuộc giờ máy.
- [ ] ID của thao tác retry không bị sinh lại ngoài ý muốn.
- [ ] Lỗi mạng không bị chuyển thành danh sách rỗng.
- [ ] Conflict có hành vi riêng, giữ lại ý định sửa của người dùng.
- [ ] Fake và remote tuân theo contract được kiểm tra chung.
- [ ] Lỗi hiển thị không chứa token hoặc stack trace thô.
- [ ] Việc hủy request cũ không hiện lỗi cho truy vấn mới.

**Ba câu hỏi:** Vì sao tiêm clock hữu ích hơn sleep trong test? Khi nào xác minh lời gọi là test có ý nghĩa? Vì sao trả `[]` trong `catch` nguy hiểm?

**15 giờ:** 3 giờ thiết kế lỗi; 8 giờ lab; 3 giờ test; 1 giờ demo bảng lỗi. **Nộp:** bảng lỗi, fake, contract tests và test clock.

Đọc [Flutter testing architecture](https://docs.flutter.dev/app-architecture/case-study/testing), [Dart exceptions](https://dart.dev/language/error-handling), [gợi ý](../solutions/week-14.md).
