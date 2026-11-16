# Tuần 26 — Deep link, điều hướng và nhắc việc

**Mục tiêu:** mở đúng công việc từ liên kết hoặc thông báo trong cả lần khởi động mới và khi ứng dụng đã mở. **Tiên quyết:** route, auth, repository và permission adapter đã có. **Thời lượng:** 3 giờ học, 8 giờ lab, 3 giờ kiểm thử, 1 giờ review; 5 giờ thêm để nghiên cứu push notification nếu muốn.

## Bài giảng

### 1. Đích đến có danh tính, không chỉ có màn hình

Route `/tasks/t-123` mô tả danh tính tài nguyên. Giao diện lấy dữ liệu theo ID và quyền của người đang đăng nhập; không tin một object tùy ý nhét vào link. Nếu công việc bị xóa, hiển thị trạng thái không còn tồn tại. Nếu không có quyền, backend phải từ chối, kể cả khi người dùng tự sửa URL.

Chuẩn hóa link ở biên hệ thống trước khi đưa vào điều hướng. Ví dụ chỉ chấp nhận scheme và host của ứng dụng, cùng đường dẫn đúng dạng:

```dart
String? taskIdFromUri(Uri uri) {
  if (uri.scheme != 'https' || uri.host != 'workboard.example') {
    return null;
  }
  final parts = uri.pathSegments;
  if (parts.length != 2 || parts.first != 'tasks') return null;
  return parts[1].isEmpty ? null : parts[1];
}
```

`workboard.example` là tên minh họa; App Links/Universal Links thật cần domain bạn kiểm soát và các file xác minh. Khi chưa có domain, dùng route nội bộ hoặc cơ chế thử nghiệm cục bộ; ghi rõ mức đã kiểm chứng.

### 2. Cold start và warm start

Cold start là link đến khi tiến trình chưa chạy; warm start là link đến khi ứng dụng đang sống. Cả hai phải đi qua cùng một hàm xử lý đích đến. Nếu hai nguồn sự kiện cùng báo link khởi động, cần tránh push cùng một màn hình hai lần.

Auth thường chưa sẵn sàng ngay khi app khởi động. Mô hình hóa ba trạng thái: đang khôi phục phiên, chưa đăng nhập và đã đăng nhập. Chờ khôi phục phiên trước khi redirect. Với người chưa đăng nhập, giữ một đích chờ hợp lệ; đăng nhập xong mới mở đích đó. Chỉ chấp nhận đường dẫn nội bộ đã kiểm tra, tránh redirect đến URL ngoài tùy ý.

### 3. Thông báo là lời mời mở dữ liệu hiện tại

Payload nên chứa ID công việc, không chứa nội dung bí mật hoặc giả định dữ liệu vẫn còn mới. Khi người dùng nhấn thông báo, chạy lại kiểm tra quyền và tải dữ liệu hiện tại. Thông báo đã lên lịch cũng có thể trở nên lỗi thời khi hạn hoàn thành đổi hoặc công việc đã xong.

Trong phần bắt buộc, dùng thông báo cục bộ: thiết bị tự lên lịch. Push là phần mở rộng, cần dịch vụ gửi từ server và quản lý token thiết bị. Không giả lập push bằng timer trong Dart rồi tuyên bố đã chạy khi ứng dụng bị đóng.

### 4. Thời gian cần ngữ nghĩa rõ ràng

WorkBoard lưu thời điểm tuyệt đối bằng UTC, còn UI hiển thị theo múi giờ người dùng. “Nhắc lúc 9 giờ ngày mai” là yêu cầu theo lịch địa phương; cần chuyển đúng trước khi lưu và lên lịch. Không chỉ cộng 24 giờ cho mọi quy tắc lịch. Với bài cơ bản, chọn một thời điểm cụ thể và hiển thị lại để người dùng xác nhận.

## Ba bài thực hành

### W26-L1 — Link vào công việc

Tạo bộ dữ liệu t-1 thuộc user A, t-2 thuộc user B và ID không tồn tại. Mở từng route khi đã đăng nhập, chưa đăng nhập và lúc đang khôi phục phiên. Đầu ra phải là đúng chi tiết, màn đăng nhập rồi chi tiết, hoặc trạng thái không truy cập được; không lộ dữ liệu B.

### W26-L2 — Nhắc việc cục bộ

Lên lịch nhắc một công việc sau vài phút trên thiết bị. Sửa thời điểm, hoàn thành công việc rồi kiểm tra lịch cũ được cập nhật hoặc hủy theo chính sách đã viết. Bọc dịch vụ thông báo để test không phụ thuộc đồng hồ thật.

### W26-L3 — Ma trận khởi động

Viết test cho cold/warm start, link trùng, payload thiếu ID, logout rồi nhấn thông báo cũ và nhấn lúc offline. Với offline, dùng dữ liệu cache đúng tài khoản nếu có, hoặc thông báo cần kết nối; không hiển thị cache tài khoản trước.

## Nghiệm thu và bằng chứng

- [ ] Link hợp lệ mở đúng ID, không chỉ mở trang danh sách.
- [ ] Khôi phục phiên không làm màn hình đăng nhập nhấp nháy hoặc redirect vòng lặp.
- [ ] Đích chờ được xử lý một lần sau đăng nhập.
- [ ] ID không tồn tại và không có quyền có trạng thái UI phù hợp.
- [ ] Thông báo cũ không mở dữ liệu riêng của tài khoản khác.
- [ ] Sửa/hủy nhắc việc không để lại thông báo trùng.
- [ ] Có bảng kết quả cold/warm start, loại thiết bị và múi giờ thử nghiệm.

Nộp video một cold start, một warm start, test route parser và tài liệu payload. Đánh dấu riêng phần App Links thật và phần route thử nghiệm.

## Tự kiểm tra

1. Vì sao không dùng nội dung trong notification payload làm nguồn dữ liệu chuẩn?
2. Tại sao auth cần trạng thái “đang khôi phục”?
3. Domain minh họa có đủ để xác nhận Universal Links hoạt động không?

Đọc [Flutter deep linking](https://docs.flutter.dev/ui/navigation/deep-linking), [go_router](https://pub.dev/packages/go_router), [Android App Links](https://developer.android.com/training/app-links) và [Apple User Notifications](https://developer.apple.com/documentation/usernotifications). [Gợi ý tuần 26](../solutions/week-26.md).
