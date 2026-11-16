# Trạng thái kiểm chứng của bộ học liệu

## Đã kiểm tra khi đóng gói

- API Python: chạy server HTTP thật trong test với SQLite tạm; 19 test vượt qua, bao gồm quyền tài khoản, idempotency, cập nhật đồng thời, phân trang, token, validation và lỗi mô phỏng.
- Tài liệu: kiểm tra đủ 32 bài giảng, 32 phần đáp án, ba lab mỗi tuần (96 lab), và đường dẫn nội bộ.
- Starter: đọc và rà soát mã nguồn, đối chiếu quy tắc với bài giảng và hợp đồng API.

- Công cụ tiến độ trên máy cá nhân: 4 test kiểm tra nghiệm thu, bỏ chọn, gộp/thay thế và bảo toàn dữ liệu khi nhập tệp lỗi đã vượt qua.

## Giới hạn cần biết

Môi trường soạn tài liệu chưa có Dart/Flutter SDK, vì vậy chưa chạy `dart analyze`, `dart test`, `flutter analyze` hoặc `flutter test` trên starter. Đây là các lệnh kiểm tra đầu tiên bạn cần chạy theo README starter. Không coi kiểm tra tĩnh bằng đọc code là bằng chứng biên dịch thành công.

Bốn test bài tập Dart được cố ý skip để starter phân biệt phần ví dụ đã viết và bài người học cần hoàn thành. Xóa skip khi bắt đầu bài; test phải thất bại trước khi bạn viết phần TODO. Các code snippet trong bài là ví dụ giảng giải, một số cần đặt trong class hoặc bổ sung import/fixture như bài yêu cầu.

Các trang tài liệu chính thức là tài liệu tham khảo; phiên bản package hiện cài có thể khác ví dụ. Kiểm tra hướng dẫn migration thay vì hạ hoặc nâng phiên bản mù quáng. Các bài phát hành, thiết bị và phản hồi người dùng là việc học viên cần thực hiện, chưa được thực hiện thay trong bộ này.

Trang học lưu tiến độ trên trình duyệt đang dùng, không tự đồng bộ giữa thiết bị. Dùng xuất/nhập tiến độ để sao lưu; bản CSV trong project là phương án theo dõi độc lập. Giao diện trang học chưa được kiểm tra bằng trình duyệt tự động trong môi trường soạn này.
