# Tuần 21 — Lưu offline và hàng đợi thao tác

**Đầu ra:** thêm, sửa và xem công việc khi không có mạng; thao tác vẫn tồn tại sau khi đóng ứng dụng. **Tiên quyết:** tuần 20; nắm SQL căn bản và repository. Tuần này xây lưu cục bộ; đồng bộ server hoàn chỉnh ở tuần 22.

**Lịch 15 giờ:** 3 giờ học, 8 giờ lab, 3 giờ thử mất mạng/khởi động lại, 1 giờ demo. Giới hạn phạm vi trước: một người dùng đăng nhập và một nguồn dữ liệu local; sau đó kiểm tra đổi tài khoản.

## Bài giảng

### Cache khác dữ liệu chưa được đồng bộ

Cache là bản sao có thể tải lại từ nguồn khác. Một chỉnh sửa offline chưa lên server không phải cache có thể xóa tùy ý: đó có thể là bản duy nhất của dữ liệu người dùng vừa tạo. Vì vậy phải phân biệt bản sao server, thay đổi đang chờ và trạng thái lỗi.

Chọn database cục bộ làm nguồn đọc của UI. Repository ghi dữ liệu server vào database; UI quan sát database thay vì ghép hai danh sách độc lập. Cách này giúp màn hình không đổi cấu trúc giữa online và offline. SQLite/Drift giúp lưu và truy vấn, nhưng không tự thiết kế chính sách đồng bộ cho ứng dụng.

### Outbox lưu ý định cùng với dữ liệu

Outbox là bảng các thao tác cần gửi lên server. Một bản ghi có thể chứa `operationId`, `ownerId`, `taskId`, `kind`, `payload`, `baseVersion`, `createdAt` và trạng thái xử lý. `operationId` xác định lần thao tác, còn `taskId` xác định công việc. Một công việc có thể có nhiều lần chỉnh sửa khác nhau.

```text
Transaction cục bộ:
  1. Ghi phiên bản công việc mà UI cần hiển thị.
  2. Ghi thao tác tương ứng vào outbox.
  3. Commit cả hai hoặc hủy cả hai.
```

Nếu ghi công việc xong nhưng ứng dụng dừng trước khi ghi outbox, UI cho thấy dữ liệu mới nhưng hệ thống không biết phải đồng bộ. Transaction giúp tránh trạng thái đó. Tương tự, xóa công việc offline cần giữ một dấu xóa hoặc thao tác delete đủ thông tin; xóa sạch mọi dấu vết sẽ khiến lần tải server sau làm công việc xuất hiện lại.

### Vòng đời thao tác và tài khoản

Một thao tác có thể chờ gửi, đang gửi, đã được xác nhận hoặc cần người dùng xử lý. Trạng thái “đang gửi” trong bộ nhớ không có nghĩa server đã nhận. Khi khởi động lại, cần có cách đưa thao tác chưa xác nhận về hàng chờ; tuần sau sẽ làm retry an toàn.

Mọi truy vấn và outbox phải gắn với chủ sở hữu. Logout không được khiến thao tác của A gửi bằng token B. Bạn cần chính sách rõ: ngăn logout khi còn dữ liệu chưa đồng bộ, hoặc giữ dữ liệu trong vùng riêng của A và tiếp tục khi A đăng nhập lại. Chọn phương án sau cho bài này; thông báo rõ dữ liệu đang chờ và không hiển thị nó trong phiên B.

## Thực hành

### W21-L1 — Database và nguồn đọc duy nhất (3 giờ)

Tạo bảng công việc và bảng outbox bằng Drift. Thêm thông tin local như `syncState` tách khỏi contract server. Seed ba công việc của tài khoản A và một công việc của B. UI phiên A chỉ quan sát dữ liệu A. Đóng/mở ứng dụng: dữ liệu vẫn còn, không cần gọi mạng để thấy danh sách đã lưu. Đầu ra là schema, repository và test truy vấn theo tài khoản.

### W21-L2 — Ghi nguyên tử (3 giờ)

Cho thiết bị mất mạng. Tạo công việc có ID được sinh ở client; sửa tiêu đề; xóa một công việc khác bằng dấu xóa hoặc thao tác delete. Mỗi lần ghi phải cập nhật dữ liệu và outbox trong một transaction. Cố ý ném lỗi giữa hai bước để chứng minh database không giữ một nửa thay đổi. UI hiển thị nhãn “Chờ đồng bộ”.

### W21-L3 — Thử dừng và đổi phiên (2 giờ)

Tạo công việc offline, đóng hẳn ứng dụng, mở lại rồi kiểm tra nội dung và outbox. Đăng xuất A, đăng nhập B: B không thấy dữ liệu hoặc hàng chờ của A. Đăng nhập A lại: thao tác vẫn tồn tại. Ghi chính sách dữ liệu trong README và một bảng trạng thái, không chỉ dựa vào hành vi ngẫu nhiên của cache.

## Nghiệm thu

- [ ] UI đọc từ database local và vẫn hiển thị khi mạng tắt.
- [ ] ID client và operation ID giữ nguyên sau khi mở lại ứng dụng.
- [ ] Lỗi giữa transaction không tạo bản ghi công việc/outbox lệch nhau.
- [ ] Xóa offline không mất thông tin cần gửi lên server.
- [ ] Dữ liệu và outbox được truy vấn theo đúng tài khoản.
- [ ] Người dùng nhận biết thao tác đang chờ, chưa bị báo thành công trên server.

## Tự kiểm tra

1. Vì sao không nên xóa tất cả dữ liệu local dưới tên gọi “xóa cache”?
2. Transaction bảo vệ lỗi nào giữa bảng công việc và outbox?
3. `taskId` và `operationId` khác nhau thế nào?

Đọc [Drift transactions](https://drift.simonbinder.eu/dart_api/transactions/) và [offline-first architecture](https://docs.flutter.dev/app-architecture/design-patterns/offline-first). Mở [gợi ý](../solutions/week-21.md) sau khi đã thử dừng ứng dụng.
