# Tuần 22 — Đồng bộ, xung đột và nâng cấp dữ liệu

**Đầu ra:** worker đồng bộ có retry an toàn; cách xử lý xung đột rõ ràng; kiểm thử migration giữ dữ liệu. **Tiên quyết:** outbox tuần 21, [hợp đồng API](../project/api-contract.md) và hai phiên đăng nhập để mô phỏng hai thiết bị.

**Lịch 15 giờ:** 3 giờ học, 8 giờ lab, 3 giờ chạy các tình huống lỗi, 1 giờ demo. Tập trung vào một hàng chờ tuần tự trước khi nghĩ tới gửi nhiều thao tác song song.

## Bài giảng

### Không nhận response không có nghĩa server chưa ghi

Request tạo công việc có thể đã thành công trên server nhưng response bị mất. Retry bằng ID mới sẽ tạo công việc trùng. Giữ `taskId` và `operationId` ổn định trong database. Với POST, gửi cùng `Idempotency-Key` cho những lần thử lại cùng ý định; server phải thực thi hợp đồng idempotency tương ứng. Header ở client một mình không tạo ra bảo đảm.

Retry nên có giới hạn và khoảng chờ tăng dần, có thể thêm jitter để tránh nhiều client gửi cùng lúc. Timeout và một số lỗi tạm thời là ứng viên retry; dữ liệu không hợp lệ hoặc thiếu quyền không được chữa bằng gửi lại vô hạn. Sau khi dừng tự động, giữ thao tác và cung cấp hướng xử lý.

### Version ngăn ghi đè âm thầm

Giả sử hai thiết bị đọc task version 3. Thiết bị A sửa thành version 4. Thiết bị B gửi thay đổi dựa trên version 3; server trả 409 theo contract WorkBoard. Đây là tín hiệu dữ liệu nền đã đổi. Không tự lấy version mới rồi ghi đè lại, vì thao tác đó bỏ qua xung đột mà người dùng cần biết.

```text
Local: title = "Soạn báo cáo", baseVersion = 3
Server: title = "Báo cáo đã rà soát", version = 4
PUT với version 3 → 409
→ giữ bản local, tải bản server, hiển thị lựa chọn
```

Trong bài này, cho người dùng chọn dùng bản server hoặc giữ thay đổi của mình sau khi xem cả hai. Lựa chọn giữ bản local tạo một ý định mới dựa trên version server vừa đọc; vẫn phải xử lý nếu lại có xung đột.

### Xác nhận cũ không được xóa thay đổi mới

Trong lúc worker gửi bản chỉnh sửa A, người dùng có thể tiếp tục tạo chỉnh sửa B. Response của A chỉ xác nhận A, không chứng minh B đã được lưu. Outbox cần payload chụp tại thời điểm tạo thao tác và thứ tự xử lý rõ ràng. Khi nhận response, chỉ xóa thao tác đã được xác nhận; không xóa toàn bộ hàng chờ của task hoặc ghi đè nội dung mới đang hiển thị.

### Migration là thay đổi dữ liệu đang sống

Đổi schema không chỉ là tạo database mới. Người dùng đã có dữ liệu, kể cả outbox chưa gửi. Migration cần biến đổi từ schema cũ sang mới mà giữ đúng ý nghĩa. Test phải bắt đầu bằng database phiên bản cũ có dữ liệu đại diện, chạy nâng cấp rồi kiểm tra công việc và thao tác chờ. Xóa database để “sửa” lỗi nâng cấp sẽ phá yêu cầu offline.

## Thực hành

### W22-L1 — Retry không tạo trùng (3 giờ)

Cho worker gửi một POST thành công nhưng chủ động bỏ qua response trước khi cập nhật local. Khởi động lại worker và gửi lại cùng payload, ID và idempotency key. Server chỉ có một công việc. Thêm lỗi 503 có kiểm soát, chứng minh worker dừng đúng chính sách và UI vẫn giữ nội dung đang chờ.

### W22-L2 — Hai thiết bị sửa cùng dữ liệu (3 giờ)

Hai client đọc cùng version. A sửa online; B sửa bản cũ offline rồi kết nối. B phải hiển thị xung đột với hai nội dung, không âm thầm thắng A. Thử cả chọn bản server và giữ bản local. Thêm tình huống người dùng sửa tiếp trong khi một request đang gửi; xác nhận cũ không được xóa chỉnh sửa mới.

### W22-L3 — Migration có outbox (2 giờ)

Thêm một trường local có giá trị mặc định hợp lý, chẳng hạn số lần thử đồng bộ. Tạo fixture database schema cũ có hai công việc và một thao tác pending. Chạy migration và kiểm tra nội dung, owner, operation ID, base version vẫn đúng. Ghi quy trình xử lý lỗi nâng cấp trong [mẫu sự cố](../templates/incident.md).

## Nghiệm thu

- [ ] Mất response rồi retry không tạo bản ghi trùng.
- [ ] Retry giữ nguyên ý định và key; chỉnh sửa mới có ý định mới.
- [ ] 409 tạo đường xử lý xung đột, không tự ghi đè.
- [ ] Xác nhận request cũ không xóa hoặc thay thế sửa đổi mới.
- [ ] Worker chỉ gửi thao tác của tài khoản đang phù hợp.
- [ ] Migration bảo toàn dữ liệu và outbox từ fixture phiên bản cũ.

## Tự kiểm tra

1. Vì sao timeout không đủ để kết luận POST thất bại?
2. Vì sao lấy version mới rồi gửi lại tự động có thể gây mất dữ liệu?
3. Một migration chỉ được test với database rỗng bỏ sót điều gì?

Đọc [Drift migration testing](https://drift.simonbinder.eu/migrations/tests/) và [HTTP idempotent methods](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2). Đối chiếu [đáp án](../solutions/week-22.md).
