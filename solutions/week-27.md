# Gợi ý và đáp án tuần 27

## Đáp án tự kiểm tra

1. Giá trị cấu hình được đưa vào client nên có thể bị phân tích từ binary/runtime. Bí mật đặc quyền phải ở hệ thống tin cậy phía server; client chỉ mang thông tin công khai hoặc thông tin phiên theo thiết kế auth.
2. Cài mới không đi qua dữ liệu và schema cũ. Migration, cấu hình lưu lại và pending outbox chỉ xuất hiện khi nâng cấp từ phiên bản trước.
3. Tối thiểu version/build number, commit SHA, môi trường, nền tảng, toolchain và dependency lockfile. Với crash cần thêm symbol/mapping tương ứng nếu quy trình build yêu cầu.

## Gợi ý lab

- **W27-L1:** tạo một `AppConfig` được khởi tạo duy nhất; không rải `String.fromEnvironment` khắp feature. Việc endpoint hợp lệ về cú pháp chưa chứng minh endpoint thuộc môi trường đúng: thêm allowlist hoặc kiểm tra cấu hình theo nhu cầu sản phẩm.
- **W27-L2:** giữ bước phân phối phụ thuộc bước kiểm tra. Nộp log của một lần thất bại có chủ ý và một lần thành công; che token và thông tin ký.
- **W27-L3:** giữ bản N cùng dữ liệu fixture có schema cũ. Không gỡ ứng dụng giữa hai lần cài nâng cấp vì có thể làm mất điều kiện cần kiểm tra.

## Ví dụ sửa lỗi

Lỗi: `API_BASE_URL` rỗng thì âm thầm dùng production. Khi cấu hình CI thiếu, test vô tình thao tác vào dữ liệu thật.

```dart
Uri parseEndpoint(String value) {
  if (value.trim().isEmpty) {
    throw StateError('Missing API_BASE_URL for this build');
  }
  final uri = Uri.parse(value);
  if (!uri.hasScheme || uri.host.isEmpty) {
    throw FormatException('Invalid API_BASE_URL');
  }
  return uri;
}
```

Test ba đầu vào: rỗng, không phải URL và URL của môi trường test. Với bản phân phối thật, quy tắc transport/host phải phù hợp môi trường; ví dụ local HTTP trong lab không đồng nghĩa cho phép HTTP tùy ý trong production.
