# Gợi ý và đáp án — Tuần 22

## Đáp án tự kiểm tra

1. Server có thể đã commit trước khi đường truyền response gặp lỗi. Client chỉ biết nó chưa nhận được xác nhận. Cần idempotency hoặc đối soát theo hợp đồng server để retry an toàn.
2. Version là điều kiện bảo vệ bản dữ liệu nền mà người dùng đã sửa. Tự thay version khiến request trông như dựa trên dữ liệu mới, dù nội dung local chưa được người dùng đối chiếu với thay đổi của người khác.
3. Nó bỏ sót chuyển đổi dữ liệu thật, giá trị null cũ, constraint mới, thứ tự migration và các thao tác pending. Tạo bảng mới thành công không chứng minh nâng cấp an toàn.

## Gợi ý lab

- **W22-L1:** không cần proxy phức tạp: trong bản thử nghiệm, nhận response server rồi mô phỏng ứng dụng dừng trước bước xác nhận local. Chạy lại worker từ outbox persisted. Ghi đây là mô phỏng mất xác nhận, không phải sự cố mạng thật đã đo.
- **W22-L2:** bắt đầu tuần tự. Cho mỗi task chỉ có một thao tác đang gửi; giữ chỉnh sửa sau đó riêng. Nếu gộp thao tác chưa gửi, phải giữ được ý định cuối và không thay payload của key đã từng gửi.
- **W22-L3:** kiểm tra cả đọc dữ liệu sau migration lẫn tiếp tục đồng bộ thao tác pending. Migration đúng schema nhưng làm sai owner hoặc version vẫn là lỗi.

## Ví dụ sửa lỗi

Sai:

```text
Gửi operation A của task X
Người dùng tạo operation B của task X
Nhận response A
DELETE FROM outbox WHERE task_id = X
```

Lệnh xóa làm mất B. Xác nhận đúng phải định danh thao tác:

```sql
DELETE FROM outbox
WHERE operation_id = ? AND owner_id = ?;
```

Cập nhật metadata local và xóa đúng operation trong transaction. Nếu đã có sửa đổi mới, không thay nội dung đang hiển thị bằng snapshot cũ; chỉ cập nhật phần xác nhận/version theo thiết kế hàng chờ. Test kiểm tra B vẫn pending sau response A và cuối cùng được gửi với điều kiện version hợp lệ.
