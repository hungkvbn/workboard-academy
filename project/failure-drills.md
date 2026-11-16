# Bộ tình huống lỗi để tự kiểm tra

Chạy trên dữ liệu thử. Với mỗi tình huống, ghi cách tạo lỗi, hành vi mong đợi, quan sát thực tế và test phòng tái phát. Header debug chỉ có trong mock API cục bộ.

| ID | Cách tạo | Hành vi phải đạt |
|---|---|---|
| F01 | Gửi title toàn khoảng trắng | Form báo lỗi; API từ chối nếu bỏ qua UI |
| F02 | Gõ tìm kiếm `a`, rồi `abc`; cố ý cho `a` trả về chậm hơn | Danh sách cuối thuộc `abc` |
| F03 | Nhấn lưu liên tục | Một ý định tạo chỉ sinh một công việc |
| F04 | API trả 503 | Có lỗi và retry; không loop vô hạn |
| F05 | Access token hết hạn | Refresh theo chính sách hoặc đăng nhập lại; không mất nội dung đang sửa |
| F06 | Dùng tài khoản B truy ID của A | Không đọc/sửa/xóa được dữ liệu A |
| F07 | Logout khi request đang chạy rồi login B | Response của A không cập nhật UI/cache B |
| F08 | Đóng ứng dụng sau khi ghi offline | Mở lại vẫn thấy dữ liệu và thao tác chờ |
| F09 | Server nhận create nhưng response không đến client | Retry cùng key không tạo bản thứ hai |
| F10 | Hai thiết bị sửa từ cùng version | Bản thứ hai nhận conflict; không ghi đè âm thầm |
| F11 | App cũ có dữ liệu, nâng cấp schema | Dữ liệu còn và tính năng mới chạy; migration test chứng minh |
| F12 | Đổi filter khi đang tải trang sau | Cursor và kết quả cũ không trộn vào bộ lọc mới |
| F13 | Text scale lớn và màn hình hẹp | Nội dung quan trọng/nút vẫn truy cập được |
| F14 | Rời màn hình trước khi await hoàn thành | Không dùng context/state đã dispose |
| F15 | Mở/đóng màn hình nhiều lần | Controller/subscription được giải phóng; bộ nhớ không tăng vô hạn vì tham chiếu giữ lại |
| F16 | Mở deep link khi app đóng và chưa login | Login xong đến đúng đích nếu còn quyền; nếu không thì báo rõ |
| F17 | Từ chối quyền hoặc thu hồi trong settings | Tính năng suy giảm có giải thích, app không crash |
| F18 | API đáp ứng chậm, người dùng chuyển tab | UI vẫn phản hồi và trạng thái đúng khi quay lại |
| F19 | Xóa bằng version đã cũ | Không xóa thay đổi mới mà người dùng chưa biết |
| F20 | Bản beta mới có lỗi nghiêm trọng | Dừng rollout hoặc vô hiệu hóa tính năng phù hợp, chuẩn bị bản sửa; không giả định mọi thiết bị có thể downgrade |

F09 cần mô phỏng response bị mất sau khi server đã commit, hoặc gửi cùng POST hai lần với key giống nhau. Chỉ tắt mạng trước khi gửi chưa đủ chứng minh tình huống này. F05 dùng cấu hình thời hạn token của mock theo README, không chờ hàng giờ.
