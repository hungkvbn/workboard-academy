# Gợi ý và đáp án — Tuần 20

## Đáp án tự kiểm tra

1. CI chỉ kiểm tra những quy tắc đã được mã hóa và môi trường đã cấu hình. Có thể thiếu test cho mất mạng, quyền tài khoản hoặc nâng cấp dữ liệu; test cũng có thể khẳng định sai yêu cầu.
2. Không. Giá trị dùng trong client có thể tồn tại trong bản build hoặc hành vi runtime. `--dart-define` hữu ích cho cấu hình môi trường, không phải kho bí mật cho khóa đặc quyền server.
3. Khi cần thiết bị/emulator, backend, dữ liệu riêng hoặc thời gian chạy dài. Giữ phản hồi unit/widget nhanh, đồng thời bảo đảm integration test vẫn chạy theo chính sách trước khi phát hành hoặc tích hợp thay đổi có rủi ro.

## Gợi ý lab

- **W20-L1:** thử script bằng cách cố ý tạo lỗi có kiểm soát trong nhánh riêng. Đảm bảo shell trả exit code thất bại; tránh lệnh che lỗi như `|| true` ở kiểm tra bắt buộc.
- **W20-L2:** không tạo “review bên ngoài” giả. Tự review vẫn có giá trị khi được ghi đúng; mục tiêu tiếp theo là nhận phản hồi thật từ người khác.
- **W20-L3:** tìm cả cấu hình mẫu, log debug và code gửi thông tin tới dịch vụ đo lỗi. Secret đã bị commit cần thu hồi/đổi tại nhà cung cấp; xóa dòng khỏi phiên bản hiện tại chưa vô hiệu hóa secret cũ.

## Ví dụ sửa lỗi

Sai:

```dart
debugPrint('HTTP headers: $headers, response: $body');
```

Với header bearer và body chứa dữ liệu người dùng, log này làm lộ thông tin không cần thiết. Thay bằng log có cấu trúc và tập trường cho phép:

```dart
debugPrint('operation=list_tasks status=$statusCode request=$requestId');
```

`requestId` phải không chứa token hoặc dữ liệu nhận dạng nhạy cảm. Kiểm tra thêm cách log được gửi, thời gian lưu và quyền truy cập. Không chỉ sửa một dòng rồi giả định tất cả lớp logging đã an toàn.
