# Tuần 10 — Đăng nhập, phiên làm việc và phân quyền

**Đích đến:** WorkBoard nhận biết đúng người đang dùng, phục hồi phiên có kiểm soát và không để dữ liệu tài khoản trước hiện sang tài khoản sau. **Tiên quyết:** provider bất đồng bộ tuần 09; HTTP và mã lỗi tuần 08. Mock chỉ phục vụ học tại máy cá nhân, không phải dịch vụ xác thực production.

## 1. Bài giảng

### Authentication khác authorization

Authentication trả lời “bạn là ai”; authorization trả lời “bạn được phép làm gì”. Ẩn nút sửa trên màn hình chỉ thay đổi UX, không chặn người dùng gửi request trực tiếp. Backend phải kiểm tra quyền trên từng tài nguyên. Khi người A yêu cầu ID của B, server phải từ chối hoặc trả không tìm thấy theo chính sách; client không được tự cấp quyền chỉ vì đã đăng nhập.

Token là thông tin xác thực mang quyền. Không in token vào log, không commit vào Git và không giả định `.env` được đóng gói trong app là nơi giữ bí mật. Với sản phẩm thật, cách lưu phiên phải theo cơ chế được SDK và nền tảng hỗ trợ; một file cấu hình trong APK không giữ được khóa đặc quyền bí mật.

### Mô hình phiên làm việc

Khi app khởi động, chưa biết có phiên hợp lệ hay không. Nếu coi trạng thái đó là đã đăng xuất, màn hình đăng nhập sẽ nháy lên rồi bị thay thế. Mô hình tối thiểu gồm `checking`, `signedOut`, `signedIn`; trạng thái phục hồi lỗi cần có hướng xử lý. Ví dụ kiểu dữ liệu Dart:

```dart
sealed class SessionState {
  const SessionState();
}
final class CheckingSession extends SessionState {
  const CheckingSession();
}
final class SignedOut extends SessionState {
  const SignedOut();
}
final class SignedIn extends SessionState {
  const SignedIn(this.userId);
  final String userId;
}
```

State hiển thị chỉ cần user ID, không cần chứa token công khai cho mọi widget. Một thành phần quản lý phiên cung cấp token cho lớp HTTP và thông báo thay đổi trạng thái đăng nhập.

### Refresh và nhiều request cùng lỗi

Access token có thể hết hạn. Nếu năm request cùng nhận 401 và mỗi request tự refresh, bạn tạo năm cuộc đua. Dùng một thao tác refresh đang chạy được chia sẻ, rồi thử lại request theo chính sách giới hạn. Không refresh vô hạn; 401 sau lần thử lại cần đưa phiên về trạng thái yêu cầu đăng nhập. Không coi mọi 403 hoặc lỗi mạng là hết phiên.

Retry một request ghi có thể tạo tác dụng lặp. Từ tuần này, mỗi thao tác tạo công việc có ID ổn định và `Idempotency-Key` ổn định cho các lần thử lại cùng thao tác. Không sinh key mới ở từng lần retry. Chi tiết phía server nằm trong [hợp đồng API](../project/api-contract.md).

### Đổi tài khoản là thay miền dữ liệu

Khi đăng xuất, bỏ state và cache gắn người dùng cũ; ngăn request còn chạy ghi kết quả vào phiên mới. Dữ liệu offline sau này phải được phân vùng theo `ownerId`. Việc chỉ xóa token trong khi vẫn giữ provider danh sách có thể làm lộ công việc người trước trên cùng thiết bị.

## 2. Ba bài thực hành

### W10-L1 — Luồng đăng nhập và khởi động

Gọi `POST /auth/login` với `learner1@example.test`, mật khẩu `learn1234`. Đọc `accessToken`, `refreshToken`, `user`; thêm logout cục bộ và màn hình checking. Sai mật khẩu phải giữ form, hiện lỗi dễ hiểu và cho nhập lại. Không ghi mật khẩu vào bằng chứng nộp bài ngoài dữ liệu demo này.

### W10-L2 — Phiên lỗi và refresh có giới hạn

Dùng fake HTTP để ba request cùng nhận 401. Kỳ vọng chỉ một lần gọi `/auth/refresh`, cả ba request xử lý kết quả theo phiên mới. Tạo trường hợp refresh thất bại; app về signed-out, không quay vòng request. Với timeout thông thường, giữ phiên và cho thử lại thao tác.

### W10-L3 — Hai tài khoản, một thiết bị

Tạo task A bằng tài khoản thứ nhất. Đăng nhập `learner2@example.test` cùng mật khẩu demo; thử đọc/sửa task A trực tiếp qua API theo endpoint được hỗ trợ. Đầu ra phải là từ chối hoặc không tìm thấy theo contract. Thêm test response của A đến sau khi B đăng nhập không xuất hiện trên UI của B.

## 3. Nghiệm thu và tự kiểm tra

- [ ] Checking có UI riêng, không nháy màn hình đăng nhập sai trạng thái.
- [ ] Sai thông tin đăng nhập không làm app crash.
- [ ] Request dữ liệu đính bearer token theo contract.
- [ ] Nhiều 401 đồng thời chỉ tạo một refresh đang chạy.
- [ ] Retry có giới hạn, không refresh với mọi loại lỗi.
- [ ] Dữ liệu và response của tài khoản cũ không lọt sang tài khoản mới.
- [ ] Bằng chứng kiểm tra quyền gồm request trực tiếp, không chỉ ảnh nút bị ẩn.

**Ba câu hỏi:** Vì sao giấu nút không phải phân quyền? Vì sao 401 và timeout cần xử lý khác nhau? Khi đổi tài khoản, ngoài token còn phải xử lý gì?

**15 giờ:** 3 giờ mô hình phiên; 8 giờ lab; 3 giờ test lỗi và quyền; 1 giờ demo hai tài khoản. **Nộp:** sơ đồ trạng thái phiên, test refresh và báo cáo quyền không chứa token thật.

Đọc [Supabase Flutter auth](https://supabase.com/docs/reference/dart/auth-signinwithpassword), [row-level security](https://supabase.com/docs/guides/database/postgres/row-level-security), [gợi ý](../solutions/week-10.md). SDK thật có vòng đời riêng: đọc tài liệu khi thay mock, không sao chép cơ chế refresh demo một cách máy móc.
