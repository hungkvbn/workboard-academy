# Tuần 27 — Cấu hình, ký ứng dụng và phát hành beta

**Mục tiêu:** tạo một bản beta có thể truy nguồn tới commit, chạy kiểm tra trước build và phân phối có hướng dẫn. **Tiên quyết:** các luồng cốt lõi đã qua test, có thiết bị Android. **15 giờ:** 3 giờ học, 8 giờ lab, 3 giờ kiểm tra bản build, 1 giờ review. Có Mac/Xcode thì thực hiện thêm nhánh iOS trong quỹ mở rộng.

## Bài giảng

### 1. Cấu hình thay đổi theo môi trường

Môi trường phát triển, thử nghiệm và production thường khác endpoint, định danh ứng dụng, thông tin quan sát và cờ tính năng. Truyền cấu hình vào ứng dụng từ một nơi duy nhất, kiểm tra giá trị ngay lúc khởi động. Ví dụ:

```dart
const apiBase = String.fromEnvironment('API_BASE_URL');

Uri requireApiBase() {
  final uri = Uri.tryParse(apiBase);
  if (uri == null || !uri.hasScheme || uri.host.isEmpty) {
    throw StateError('API_BASE_URL is missing or invalid');
  }
  return uri;
}
```

`--dart-define` là cơ chế cấu hình, không phải két bí mật. Giá trị đóng gói trong ứng dụng có thể bị trích xuất. Khóa quản trị hoặc `service_role` không được nằm trong client. Với môi trường thật, backend chịu trách nhiệm giữ bí mật và kiểm tra quyền.

Mock API của khóa học chỉ phục vụ luyện tập cục bộ; mật khẩu demo và endpoint debug không phù hợp để đưa lên Internet. Bản beta dùng mock phải ghi rõ cách kết nối trong mạng thử nghiệm. Muốn người ngoài mạng sử dụng độc lập, thay bằng backend thật có auth, phân quyền và cấu hình triển khai phù hợp.

### 2. Danh tính phát hành và ký mã

Application ID/bundle ID xác định ứng dụng; version hiển thị và build number giúp phân biệt phiên bản. Chữ ký cho nền tảng biết ai phát hành bản nâng cấp. Giữ an toàn khóa ký và tuân theo cơ chế quản lý khóa của kênh phân phối đang dùng.

Không đưa khóa, mật khẩu ký hoặc token dịch vụ vào repository. Trong CI, dùng secret storage và quyền tối thiểu. Thực hành backup/recovery theo công cụ bạn chọn; tài liệu phát hành phải cho biết ai sở hữu khóa và cách khôi phục mà không ghi bí mật vào tài liệu.

### 3. Pipeline tạo bằng chứng có thể lặp lại

Một pipeline tối thiểu: lấy đúng revision, cài dependency theo lockfile, format/analyze, chạy test phù hợp, build và lưu artifact. Build thành công chưa chứng minh runtime đúng. Cần smoke test trên artifact vừa tạo: cài mới, đăng nhập, tạo công việc, khởi động lại và đăng xuất.

Gắn commit SHA, version, thời điểm build và loại môi trường vào báo cáo. Điều này giúp truy lỗi về đúng source thay vì đoán xem người dùng đang chạy bản nào. Giữ dependency lockfile cho ứng dụng và ghi phiên bản Flutter đã dùng.

### 4. Phân phối theo phạm vi nhỏ

Bắt đầu bằng nhóm thử nghiệm nhỏ. Người dùng cần biết cách cài, tài khoản thử, dữ liệu nên dùng, giới hạn và cách gửi lỗi. Tài khoản store và yêu cầu duyệt phụ thuộc kênh; nếu chưa có, có thể nộp Android artifact cài trực tiếp cho thử nghiệm cùng hướng dẫn phù hợp. Không tuyên bố đã lên store chỉ vì tạo được file build.

## Ba bài thực hành

### W27-L1 — Hai cấu hình rõ ràng

Tạo cấu hình development và beta với nhãn môi trường nhìn được ở màn chẩn đoán. Cho cấu hình thiếu endpoint: ứng dụng phải báo lỗi rõ trước khi thực hiện request, không tự gọi một địa chỉ ngầm định nguy hiểm.

### W27-L2 — Build có nguồn gốc

Tạo pipeline chạy kiểm tra rồi tạo artifact. Lưu commit SHA, lockfile, version/build number và kết quả test. Cố ý làm một unit test thất bại để chứng minh pipeline chặn bước xuất bản; sau đó sửa và build lại.

### W27-L3 — Thử nâng cấp

Cài bản N, tạo dữ liệu cục bộ, cài bản N+1 đúng danh tính/chữ ký và kiểm tra dữ liệu còn dùng được. Chạy smoke test trên bản release/beta đã đóng gói. Nếu chỉ chạy Android, nộp thêm kế hoạch kiểm tra iOS và ghi chưa thực thi.

## Nghiệm thu và bằng chứng

- [ ] Không có khóa quản trị, token hoặc mật khẩu ký trong source và artifact cấu hình công khai.
- [ ] Bản beta hiển thị version và môi trường để chẩn đoán.
- [ ] Pipeline thất bại khi test quan trọng thất bại.
- [ ] Có thể truy artifact về commit và phiên bản toolchain.
- [ ] Bản nâng cấp giữ dữ liệu đúng chính sách migration.
- [ ] Người khác làm theo README và cài được trên nền tảng đã kiểm chứng.
- [ ] Phạm vi sử dụng mock local hoặc backend thật được ghi chính xác.

Nộp [checklist phát hành](../templates/release.md), log pipeline đã loại bí mật và kết quả smoke test.

## Tự kiểm tra

1. Vì sao `--dart-define` không bảo vệ khóa quản trị?
2. Vì sao phải kiểm tra nâng cấp bên cạnh cài mới?
3. Một artifact cần thông tin gì để truy nguồn lỗi?

Đọc [Flutter deployment](https://docs.flutter.dev/deployment), [Android release](https://docs.flutter.dev/deployment/android) và [iOS release](https://docs.flutter.dev/deployment/ios). [Gợi ý tuần 27](../solutions/week-27.md).
