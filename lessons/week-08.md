# Tuần 08 — HTTP, JSON và trạng thái dữ liệu từ server

**Mục tiêu:** thay danh sách trong bộ nhớ bằng dữ liệu API mà UI vẫn thể hiện được tải, rỗng và lỗi. **Tiên quyết:** `Future`, exception, widget lifecycle và form. Chạy [mock API](../mock_api/README.md), đọc [hợp đồng dữ liệu](../project/api-contract.md).

**15 giờ:** 3 giờ lý thuyết và thử request, 8 giờ cho ba lab, 3 giờ test/debug, 1 giờ demo. Tuần này chưa cần tự động refresh token hoặc offline; khi token demo hết hạn, đăng nhập lại theo README. Tuần 10 sẽ xây session đầy đủ.

## Bài giảng

### 1. Request và response là một hợp đồng

HTTP request có method, URL, header và có thể có body. `GET /tasks` đọc danh sách; `POST /tasks` tạo công việc. Response có status code và body. Một response 200 chứa danh sách rỗng vẫn là thành công, không phải lỗi. Ngược lại, kết nối bị từ chối không có status code để kiểm tra.

UI không nên phải biết URL, bearer token hoặc cách parse JSON. Tạo một lớp HTTP repository nhận client từ ngoài. Bắt đầu bằng `package:http`: thêm bằng `flutter pub add http`, rồi truyền `http.Client` vào lớp. Trong test thay client bằng `MockClient` của package hoặc một fake transport. Request mạng thật chỉ nằm ở bài kiểm thử tích hợp riêng.

### 2. JSON là dữ liệu chưa được tin cậy về kiểu

JSON hợp lệ về cú pháp chưa chắc hợp lệ về nghiệp vụ. `items` có thể thiếu, `title` có thể thành số, `status` có giá trị lạ. Đặt kiểm tra ở ranh giới dữ liệu để lỗi được phát hiện gần nguồn, thay vì một widget bất kỳ crash sau đó.

```dart
Map<String, dynamic> requireObject(Object? value) {
  if (value is! Map<String, dynamic>) {
    throw const FormatException('Cần một JSON object');
  }
  return value;
}

List<Map<String, dynamic>> parseItems(Object? decoded) {
  final envelope = requireObject(decoded);
  final items = envelope['items'];
  if (items is! List) {
    throw const FormatException('items phải là danh sách');
  }
  return items.map(requireObject).toList(growable: false);
}
```

Ở đây `dynamic` nằm ở ranh giới JSON, không lan ra toàn bộ ứng dụng. Sau kiểm tra envelope, chuyển từng object thành `WorkTask` và kiểm tra trường theo contract. Lưu `nextCursor` để tuần 11 làm phân trang; tuần này giới hạn một trang và ghi rõ giới hạn đó. Không gọi `jsonDecode` khi HTTP 204 vì body rỗng.

### 3. Async UI cần một trạng thái có nghĩa

Trước lần tải đầu, màn hình chưa có dữ liệu. Khi tải xong có thể có danh sách hoặc rỗng. Khi tải thất bại cần thông báo và nút thử lại. Hãy vẽ bốn trạng thái này trước khi viết widget. Nếu refresh khi đã có dữ liệu, quyết định giữ dữ liệu cũ hay hiện spinner; không vô tình giữ error cũ sau lần tải thành công.

Không tạo request mới vô điều kiện trong `build()`: Flutter có thể gọi build nhiều lần. Khởi tạo Future trong lifecycle thích hợp hoặc gọi từ controller; thao tác retry chủ động tạo lần tải mới. Nếu dùng `setState` sau `await`, kiểm tra `mounted` và bảo đảm kết quả vẫn thuộc lần tải hiện tại. `mounted` chỉ bảo vệ lifecycle, chưa giải quyết race giữa hai request trên cùng màn hình.

### 4. Cấu hình môi trường khác với bí mật

Android Emulator dùng `10.0.2.2` để truy máy host; `localhost` bên trong emulator trỏ về emulator. Flutter web chạy cùng máy có thể dùng `127.0.0.1`. Nhận base URL qua `String.fromEnvironment('API_BASE_URL')`, đọc hướng dẫn cấu hình HTTP debug trong README API. Giá trị `dart-define` được đưa vào ứng dụng; không coi đó là nơi cất khóa đặc quyền.

## Thực hành

### W08-L1 — Tự đọc hợp đồng qua HTTP

Chạy server, gọi `/health`, đăng nhập tài khoản demo và dùng access token gọi `/tasks`. Tạo ba task bằng POST, mỗi task có ID và idempotency key riêng. Lưu request mẫu đã che token và response fixture. Kiểm tra danh sách ban đầu rỗng rồi có ba task; gửi title rỗng phải nhận 400 với error envelope.

### W08-L2 — HTTP repository và màn hình danh sách

Viết `fetchTasks()` nhận cấu hình/client qua constructor, trả dữ liệu đã parse. Hiển thị loading, empty, data, error và retry. Thử `X-Debug-Delay-Ms: 1500`, rồi `X-Debug-Fail: 503`; bỏ header lỗi và nhấn thử lại phải phục hồi. Token không được ghi vào log. UI không tự đọc JSON key hoặc ghép URL.

### W08-L3 — Test boundary và lỗi

Dùng fake/MockClient cho bốn fixture: 200 có một task; 200 danh sách rỗng; 503 error; 200 nhưng `items` không phải list. Thêm trường hợp transport ném exception. Xác nhận repository phân biệt lỗi dữ liệu và lỗi HTTP, UI đều có cách hiển thị phù hợp. Ghi rõ các ví dụ test không cần chạy server.

## Nghiệm thu

- [ ] Có request mẫu và fixture đúng contract, không lưu access token.
- [ ] Bốn trạng thái UI được tái hiện có chủ đích.
- [ ] Retry sau 503 hiển thị dữ liệu mới và bỏ lỗi cũ.
- [ ] Không phát request mới chỉ vì widget rebuild.
- [ ] JSON sai cấu trúc không trở thành một danh sách rỗng giả.
- [ ] Unit test dùng fake transport, không phụ thuộc server đang bật.
- [ ] Base URL phù hợp thiết bị; ngoại lệ HTTP chỉ phục vụ debug/local.

## Tự kiểm tra

1. Vì sao HTTP 200 vẫn có thể khiến bước đọc dữ liệu thất bại?
2. Vì sao `mounted` chưa đủ ngăn kết quả request cũ ghi đè request mới?
3. Danh sách rỗng khác mất kết nối như thế nào về trải nghiệm và kiểu dữ liệu?

Đọc [Fetch data from the internet](https://docs.flutter.dev/cookbook/networking/fetch-data), [http package](https://pub.dev/packages/http) và [JSON serialization](https://docs.flutter.dev/data-and-backend/serialization/json). Sau khi làm, mở [gợi ý](../solutions/week-08.md).
