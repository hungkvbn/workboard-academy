# Flutter starter — bắt đầu ở tuần 04

Ví dụ này có màn hình rỗng, form thêm tiêu đề và danh sách lưu trong bộ nhớ. **Đóng tiến trình ứng dụng sẽ mất dữ liệu.** Chưa có model đầy đủ, sửa/xóa, đăng nhập, API, Riverpod, SQLite hay đồng bộ; đó là phần bạn xây qua các bài học.

## Tạo project trên máy của bạn

Cài Flutter stable và chạy `flutter doctor`. Chọn Android hoặc web để bắt đầu. Build iOS cần macOS và Xcode; chưa có Mac thì hoàn thành track Android, không ghi rằng đã kiểm thử iOS.

Bộ starter chỉ chứa source, pubspec, cấu hình analyzer và test. Thư mục nền tảng được tạo bằng Flutter SDK trên máy học viên để phù hợp SDK đang dùng. Làm theo thứ tự này để tránh công cụ tạo project ghi đè code starter:

1. Chọn một thư mục làm việc **nằm ngoài thư mục starter này**.
2. Tạo project mới (đổi tên nếu đường dẫn đã tồn tại):

```bash
flutter create --project-name workboard_app --platforms=android,ios,web workboard_app
```

3. Dùng trình quản lý file hoặc IDE sao chép `lib/`, `test/`, `pubspec.yaml` và `analysis_options.yaml` từ starter này vào project mới. Thay `lib/main.dart`, `test/widget_test.dart` và hai file cấu hình được tạo sẵn bằng các file của starter. Không sao chép vào project đang có công việc riêng của bạn.
4. Từ terminal trong project mới, chạy:

```bash
flutter pub get
flutter analyze
flutter test
flutter devices
flutter run
```

`flutter run` có thể yêu cầu chọn thiết bị. Với web đã được cấu hình: `flutter run -d chrome`. Với Android, khởi động emulator hoặc kết nối thiết bị trước. Không cần build mọi nền tảng ở tuần 04.

## Kiểm tra lần đầu

- Thấy tiêu đề WorkBoard và trạng thái chưa có công việc.
- Bấm nút thêm, nhập `  Học Dart  `, bấm Lưu: danh sách hiện `Học Dart`.
- Nhập toàn khoảng trắng: form hiện lỗi, không tạo dòng mới.
- Bấm Hủy: không tạo công việc.
- Chạy `flutter test`: ba smoke/widget test cần xanh. Các test này chỉ kiểm tra phạm vi starter, không chứng minh ứng dụng đã sẵn sàng phát hành.

## Bạn sẽ xây tiếp những gì?

| Tuần | Công việc tiếp theo |
|---|---|
| 04–05 | Thay `List<String>` bằng `WorkTask`; thêm trạng thái, chi tiết, sửa/xóa và validation |
| 06–07 | Navigation, responsive, chữ lớn, accessibility, stable keys và đo rebuild |
| 08–12 | API, trạng thái loading/empty/error, Riverpod, authentication, tìm kiếm và phân trang |
| 13–20 | Repository, dependency injection, test, CI và review |
| 21–24 | Drift, outbox, đồng bộ, conflict và hiệu năng |
| 25–32 | Tích hợp nền tảng, beta, vận hành và phản hồi người dùng |

Tự đưa model từ Dart starter vào project Flutter ở thời điểm bài yêu cầu. Không import bằng đường dẫn tuyệt đối trên máy. Nếu tách thành package dùng chung sau này, ghi quyết định và cách dependency được resolve vào README của bạn.

## Chú ý khi nối mock API ở tuần 08

Địa chỉ API phụ thuộc thiết bị: trình duyệt trên máy chạy server dùng `http://127.0.0.1:8765`; Android emulator thường truy cập máy host qua `http://10.0.2.2:8765`. Thiết bị vật lý cần mạng và địa chỉ phù hợp. Đọc `../../mock_api/README.md` trước khi đổi bind address hoặc cấu hình cleartext cho môi trường phát triển. Backend mock không được dùng làm backend production.

Ví dụ đã giải quyết hai chi tiết lifecycle để bạn đọc: dispose `TextEditingController` và kiểm tra `mounted` sau khi chờ dialog. `FormState!` trong `_submit` dựa trên invariant rằng form đang được gắn vào dialog; không dùng dấu `!` để che lỗi null ở các luồng dữ liệu chưa được xác nhận.

Độ dài title dùng `String.length` từ 1 đến 120 sau trim, giống Dart starter. Chưa cần cài thêm state-management package ở tuần 04: hiểu state cục bộ trước, thêm Riverpod ở tuần 09.

Tài liệu: [Cài Flutter](https://docs.flutter.dev/install), [Flutter learning pathway](https://docs.flutter.dev/learn/pathway), [Widget testing](https://docs.flutter.dev/testing/overview).
