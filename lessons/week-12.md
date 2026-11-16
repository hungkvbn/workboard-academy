# Tuần 12 — Mô hình dữ liệu, SQL và cache có ranh giới

**Đích đến:** thiết kế bảng công việc và thực hành lưu/đọc dữ liệu có kiểm tra tính đúng đắn. Đây là nền tảng cho tuần offline 21–22; tuần này chưa xây đồng bộ tự động. **Tiên quyết:** `WorkTask`, JSON và phân vùng dữ liệu theo người dùng.

## 1. Bài giảng

### Một dữ liệu, nhiều cách biểu diễn

API truyền `dueAt` bằng chuỗi ISO UTC hoặc `null`; Dart có thể dùng `DateTime?`; SQLite có thể lưu số milliseconds kể từ epoch. Chuyển đổi tại ranh giới thay vì để từng widget tự đoán. Quy ước của bài: `due_at_ms` là epoch milliseconds UTC, `null` nghĩa chưa đặt hạn. Chỉ đổi múi giờ khi hiển thị. Dữ liệu thiếu hạn không đồng nghĩa hạn bằng thời điểm hiện tại.

`version` là phiên bản một task dùng phát hiện sửa trên dữ liệu cũ; nó khác phiên bản schema của database. `updatedAt` mô tả thời gian server cập nhật, không tự thay thế version để giải quyết xung đột. Đồng hồ của hai thiết bị có thể lệch.

### Ràng buộc giữ dữ liệu hợp lệ

Database nên bảo vệ các bất biến đơn giản. Ví dụ schema dùng cho bài SQL độc lập:

```sql
CREATE TABLE tasks (
  id TEXT PRIMARY KEY,
  owner_id TEXT NOT NULL,
  title TEXT NOT NULL CHECK(length(trim(title)) > 0),
  description TEXT NOT NULL DEFAULT '',
  status TEXT NOT NULL CHECK(status IN ('todo', 'doing', 'done')),
  due_at_ms INTEGER,
  updated_at_ms INTEGER NOT NULL,
  version INTEGER NOT NULL CHECK(version >= 1)
);
CREATE INDEX tasks_owner_status ON tasks(owner_id, status);
```

`PRIMARY KEY` chặn ID trùng trong bảng. `CHECK` chặn trạng thái không hợp lệ dù dữ liệu đi qua đường code khác. Constraint không thay thế validation có thông báo thân thiện trên UI; hai lớp phục vụ mục đích khác nhau.

### Query có tham số và index có mục tiêu

Không nối nội dung nhập của người dùng trực tiếp vào SQL. Dùng placeholder và binding do thư viện cung cấp. Query như `WHERE owner_id = ? AND status = ?` cần cả quyền sở hữu và bộ lọc. Index `(owner_id, status)` có thể giúp truy vấn này, nhưng cũng làm ghi tốn thêm chi phí. Dùng `EXPLAIN QUERY PLAN` để xem thay vì tạo index cho mọi cột.

### Transaction, migration và cache

Transaction nhóm nhiều thay đổi để cùng thành công hoặc cùng thất bại. Nếu lưu bản ghi task nhưng quên lưu metadata liên quan do ứng dụng bị đóng, trạng thái có thể không nhất quán. Migration là biến đổi schema và dữ liệu của người đã cài bản trước; xóa database để hết lỗi chỉ phù hợp dữ liệu thử có thể bỏ, không phải chiến lược nâng cấp sản phẩm.

Cache là bản sao để đọc nhanh hoặc đọc khi mạng lỗi. Nó cần biết thuộc tài khoản nào, được cập nhật lúc nào và khi nào nên tải lại. SQLite/Drift không tự cung cấp đồng bộ với API. Tuần này chọn chính sách đơn giản: tải server thành công thì cập nhật cache của user hiện tại; khi mở lại có thể đọc cache kèm nhãn chưa được làm mới.

## 2. Ba bài thực hành

### W12-L1 — Bộ dữ liệu có quy tắc

Tạo SQLite scratch database qua công cụ bạn có; nhập ít nhất 12 task thuộc hai owner, có đủ ba trạng thái và ít nhất hai task không hạn. Viết query lọc theo owner/status, đếm hoàn thành và sắp xếp hạn với quy tắc `null` rõ ràng. Thử chèn status `closed`; đầu ra mong đợi là bị constraint từ chối.

### W12-L2 — Adapter local có tham số

Tạo local data source dùng Drift hoặc SQLite adapter bạn chọn. Viết mapping JSON → `WorkTask` → database → `WorkTask`. Chuỗi tiêu đề `O'Brien` phải lưu/đọc nguyên vẹn. Đọc task của A không bao gồm B. Test round-trip cho `dueAt=null` và một thời điểm UTC xác định.

### W12-L3 — Nâng schema mà giữ dữ liệu

Tạo schema v2 thêm `is_pinned` chỉ dùng cục bộ, mặc định false. Giữ một file database v1 làm fixture, chạy migration rồi kiểm tra các task cũ vẫn tồn tại với trạng thái và hạn không đổi. Không thêm `is_pinned` vào request API vì contract chưa hỗ trợ trường này.

## 3. Nghiệm thu và tự kiểm tra

- [ ] Có schema, seed và query tái chạy được.
- [ ] Status sai và ID trùng bị xử lý rõ ràng.
- [ ] Query sử dụng parameter binding.
- [ ] Mọi đọc cache có phạm vi owner đúng.
- [ ] `null` và UTC round-trip không mất ý nghĩa.
- [ ] Migration v1 → v2 giữ bản ghi cũ và có test.
- [ ] README nói rõ cache hiện chưa có đồng bộ offline.

**Ba câu hỏi:** Task version khác schema version thế nào? Vì sao không dùng thời gian thiết bị để quyết định bản mới nhất? Database local có tự đồng bộ server không?

**15 giờ:** 3 giờ SQL và mô hình; 8 giờ lab; 3 giờ mapping/migration test; 1 giờ giải thích query plan. **Nộp:** schema, fixture v1, migration, test và chính sách cache ngắn.

Đọc [SQLite transactions](https://www.sqlite.org/lang_transaction.html), [Drift migrations](https://drift.simonbinder.eu/migrations/), [gợi ý](../solutions/week-12.md).
