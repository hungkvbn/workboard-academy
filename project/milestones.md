# Tám milestone nghiệm thu

| Mốc | Tuần | Demo bắt buộc | Gate |
|---|---|---|---|
| M1 — Dart | 01–03 | CLI thêm/lọc/sắp xếp và lưu/đọc JSON | Null/error xử lý rõ, unit test logic, không nuốt exception |
| M2 — Flutter | 04–07 | Bốn màn hình, form, điều hướng và danh sách | Lifecycle đúng, ID làm key, chữ lớn/màn hình nhỏ dùng được |
| M3 — Dữ liệu | 08–12 | Đăng nhập, tìm kiếm, phân trang và dữ liệu tài khoản | Response cũ không ghi đè, quyền backend đúng, lỗi phục hồi được |
| M4 — Kiến trúc | 13–16 | Thay repository fake/HTTP và đổi quy tắc nghiệp vụ | UI không phụ thuộc HTTP trực tiếp; ADR giải thích lựa chọn |
| M5 — Chất lượng | 17–20 | Test quan trọng và CI chạy trên commit mới | Có regression test, không cần API thật cho unit/widget tests |
| M6 — Độ bền | 21–24 | Offline, retry, conflict và phép đo hiệu năng | Không mất/nhân bản dữ liệu; số đo có điều kiện và bằng chứng |
| M7 — Phát hành | 25–28 | Bản beta, deep link, crash drill và nâng cấp | Cài được trên máy khác, truy lỗi được, migration kiểm chứng |
| M8 — Sản phẩm | 29–32 | Hai vòng phản hồi, sửa lỗi, bảo trì và bảo vệ capstone | Hồ sơ đầy đủ, ưu tiên có lý do, review ngoài hoặc ghi rõ hạn chế |

Mỗi demo tối đa 10 phút: 2 phút bài toán, 4 phút hành vi bình thường và lỗi, 2 phút test/bằng chứng, 2 phút quyết định và hạn chế. Chưa đạt một gate quan trọng thì tạo ticket sửa trước khi bắt đầu milestone phụ thuộc.

Tuần 29 có bài thiết kế tính năng nhóm. Mock API chỉ hỗ trợ công việc riêng từng chủ sở hữu; dùng fake và hợp đồng đề xuất để luyện thiết kế. Triển khai phân quyền nhóm thật là bài mở rộng, không giả định backend mẫu đã hỗ trợ.
