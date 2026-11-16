# Đặc tả WorkBoard

## Bài toán

Một người cần ghi công việc nhanh, tìm lại dễ và tiếp tục làm khi mạng chập chờn. Họ dùng nhiều thiết bị và cần biết thay đổi đã được lưu, đang chờ đồng bộ hay có xung đột. Sản phẩm cốt lõi là quản lý công việc cá nhân; chia sẻ theo nhóm là đề xuất mở rộng ở tuần 29.

## Người dùng và luồng chính

- Người mới mở ứng dụng, đăng nhập và nhìn thấy danh sách hoặc trạng thái trống có lời hướng dẫn.
- Người dùng tạo công việc, đặt hạn, cập nhật trạng thái và tìm/lọc danh sách.
- Người dùng mất mạng vẫn đọc dữ liệu đã tải, tạo/sửa công việc và nhìn thấy trạng thái chờ đồng bộ.
- Khi mạng trở lại, hệ thống đồng bộ an toàn và yêu cầu giải quyết nếu dữ liệu đã thay đổi ở nơi khác.
- Người dùng đăng xuất rồi đổi tài khoản; dữ liệu của tài khoản trước không hiển thị cho tài khoản mới.

## Phạm vi bắt buộc

1. Danh sách, chi tiết, tạo/sửa, xóa có xác nhận, lọc trạng thái và tìm kiếm tiêu đề.
2. Session đăng nhập, lỗi mạng/phiên hết hạn, phân trang.
3. Dữ liệu cục bộ, hàng đợi thao tác offline, retry có kiểm soát, xung đột phiên bản.
4. UI cho loading, empty, success, error, offline, pending sync và conflict.
5. Test các luồng quan trọng, CI, bản beta và chẩn đoán lỗi.
6. Khả năng sử dụng với cỡ chữ lớn, màn hình nhỏ và công cụ đọc màn hình cho luồng chính.

Ngoài phạm vi cốt lõi: thanh toán, chat thời gian thực, mạng xã hội, rich-text editor, AI và tự viết toàn bộ backend production. Chỉ chọn bài mở rộng sau khi các chức năng bắt buộc đạt tiêu chí.

## Mô hình dữ liệu

| Trường | Ý nghĩa | Quy tắc |
|---|---|---|
| id | ID ổn định của công việc | Client tạo trước khi gửi; không dùng vị trí trong danh sách |
| title | Tiêu đề | Trim, 1–120 đơn vị UTF-16 như `String.length` của Dart |
| description | Nội dung | Chuỗi, mặc định rỗng |
| status | Trạng thái | `todo`, `doing`, `done` |
| dueAt | Hạn hoàn thành | Null hoặc thời điểm ISO 8601 UTC; UI hiển thị múi giờ người dùng |
| updatedAt | Lần sửa trên server | Server cung cấp, ISO 8601 UTC |
| version | Phiên bản đồng bộ | Server bắt đầu từ 1, tăng sau mỗi cập nhật |
| ownerId | Chủ sở hữu | Server lấy từ phiên đăng nhập; client không tự quyết định |

Trong Dart đặt tên model `WorkTask`. Trạng thái đồng bộ như pending/failed/conflict là dữ liệu của client, tách khỏi `status` nghiệp vụ. Trường local có thể gồm `localUpdatedAt`, `syncState` và `lastError`; không gửi nguyên object của DB lên server.

Title 120 là quy ước kỹ thuật của bài học. Với sản phẩm thật cần thảo luận giới hạn theo ký tự người dùng nhìn thấy, đặc biệt emoji. Một công việc được phép có hạn trong quá khứ; UI hiển thị quá hạn nếu `dueAt < now` và chưa done. Inject đồng hồ khi test để không phụ thuộc giờ chạy.

## Quy tắc thao tác

- Tạo: ID ổn định và idempotency key riêng cho một ý định tạo; retry cùng ý định giữ nguyên key và payload.
- Sửa: gửi version đã đọc. Server từ chối version cũ bằng 409; UI không âm thầm ghi đè.
- Xóa: yêu cầu version hiện tại, tránh xóa mất thay đổi mới của thiết bị khác.
- Tìm kiếm: kết quả của truy vấn cũ không được ghi đè truy vấn mới; khi filter thay đổi phải reset trang.
- Logout: dừng request/subscription, xóa trạng thái hiển thị. Dữ liệu local và outbox phải được phân vùng theo tài khoản; xử lý thao tác chưa sync bằng chính sách rõ ràng.
- Offline: phân biệt không có kết nối với request server thất bại. Cờ kết nối không bảo đảm API đang hoạt động.

## Màn hình cần thiết

Đăng nhập; danh sách công việc; chi tiết; form tạo/sửa; cài đặt; giao diện xử lý xung đột. Trên mỗi màn hình, thiết kế trạng thái lỗi và cách phục hồi trước khi viết code.

## Sản phẩm nộp cuối

Repository dễ chạy; bản beta Android; các luồng test; 3–5 ADR; báo cáo hiệu năng trước/sau; một postmortem; release notes; bằng chứng review; backlog ưu tiên từ phản hồi người dùng. iOS là bằng chứng bổ sung khi có môi trường. Không cần hoàn thành tính năng nhóm để đạt capstone cốt lõi.
