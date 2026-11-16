# Gợi ý và đáp án tuần 28

## Đáp án tự kiểm tra

1. Không mặc định. Phân loại theo mức tác động: lỗi đã được xử lý có thể là event/metric, còn exception bất ngờ cần báo cáo phù hợp. Tránh lượng log lớn che mất vấn đề cần hành động.
2. Dữ liệu chưa sync có thể là bản duy nhất. Xóa database làm mất dữ liệu và bằng chứng điều tra; crash hết không có nghĩa hệ thống đúng.
3. Không bảo đảm tất cả thiết bị nhận hoặc cài ngay một phiên bản. Dừng rollout không sửa máy đã cập nhật. Cờ remote và fix-forward chỉ hiệu quả khi đường thực thi tương ứng còn hoạt động.

## Gợi ý lab

- **W28-L1:** viết một allowlist trường log. Test adapter nhận error code và metadata, không nhận nguyên request có header Authorization.
- **W28-L2:** fixture phải tạo bằng schema cũ hoặc database snapshot thực sự. Chỉ chạy create schema mới rồi đổi số version không kiểm tra đúng migration.
- **W28-L3:** đặt sẵn tiêu chí kết thúc diễn tập: ngừng tăng dữ liệu trùng, regression test đỏ trước sửa/xanh sau sửa, có kế hoạch xử lý bản ghi đã trùng. Không xóa dữ liệu production trong bài tập.

## Ví dụ sửa lỗi

Lỗi: retry tạo task dùng ID mới mỗi lần nên server nhận các thao tác khác nhau.

```dart
final operation = PendingCreate(
  taskId: stableTaskId,
  idempotencyKey: stableOperationId,
  payload: frozenPayload,
);
await outbox.persist(operation);
await syncQueue.trySend(operation);
```

Các lần retry dùng lại chính operation đã lưu, không sinh lại ID hoặc sửa payload dưới cùng idempotency key. Sau khi server xác nhận, transaction cập nhật dữ liệu cục bộ và trạng thái queue. Server phải hỗ trợ semantics idempotency đã thỏa thuận; chỉ sửa client không đủ nếu backend không thực thi giao kèo.
