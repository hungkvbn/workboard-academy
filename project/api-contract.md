# Hợp đồng API WorkBoard — phiên bản học tập 1

Hợp đồng này khớp `mock_api/server.py`. Base URL mặc định `http://127.0.0.1:8765`; mã Flutter nên nhận base URL qua cấu hình. Backend dành cho **lab cục bộ**, chỉ hỗ trợ công việc riêng của từng người. Chia sẻ công việc/nhóm ở tuần 29 là thiết kế mở rộng hoặc implementation riêng, chưa có trong mock.

## Quy tắc chung

- Request POST/PUT dùng `Content-Type: application/json`, body là một JSON object, tối đa 1 MiB.
- Endpoint `/tasks` và `/tasks/{id}` yêu cầu `Authorization: Bearer <accessToken>`.
- JSON dùng camelCase; model Dart có thể tên `WorkTask`.
- Error body nhất quán: `{ "error": { "code": "...", "message": "..." } }`. UI quyết định thông báo tiếng Việt theo code; không phụ thuộc toàn bộ chuỗi message.
- HTTP 204 có body rỗng. Không gọi JSON decode với body này.
- Không có endpoint đăng ký, quên mật khẩu, chia sẻ nhóm, upload, push hay logout từ xa. Logout trong lab xóa phiên phía client theo chính sách dữ liệu đã thiết kế.

## Mô hình công việc

```json
{
  "id": "task-001",
  "title": "Học Dart",
  "description": "Hoàn thành lab tuần 1",
  "status": "todo",
  "dueAt": "2026-12-01T09:00:00.000Z",
  "updatedAt": "2026-11-16T10:00:00.000Z",
  "version": 1,
  "ownerId": "user-1"
}
```

Các ngày trong ví dụ là dữ liệu minh họa, không phải hạn học bắt buộc.

| Trường | Quy tắc |
|---|---|
| `id` | Client tạo trước khi gửi; 1–100 ký tự ASCII chữ, số, `_`, `-`; nên dùng UUID. Duy nhất trong phạm vi owner. Không đổi khi retry. |
| `title` | Chuỗi; trim hai đầu; dài 1–120 **UTF-16 code units**, tương đương Dart `String.length`. Đây không phải số grapheme người dùng nhìn thấy. |
| `description` | Chuỗi, mặc định `""` khi tạo; tối đa 10.000 Unicode code points theo mock. |
| `status` | `todo`, `doing`, `done`; mặc định `todo` khi tạo. |
| `dueAt` | `null` hoặc ISO 8601 có UTC `Z`/`+00:00`; server chuẩn hóa về milliseconds và `Z`. Client chuyển giờ địa phương sang UTC trước khi gửi. |
| `updatedAt` | Server tạo/cập nhật, UTC. Không dùng timestamp client làm cơ chế phát hiện xung đột. |
| `version` | Server đặt 1 khi tạo và tăng 1 mỗi PUT thành công. PUT gửi version đang biết để so sánh. |
| `ownerId` | Server lấy từ token; gửi giá trị này từ client không thể chuyển ownership. |

Các thao tác hợp lệ trên status hiện cho phép mọi chuyển đổi giữa ba giá trị. Nếu thêm quy tắc nghiệp vụ ở bài sau, cập nhật rõ hợp đồng và fake/test; đừng giả định server cũ đã thực thi quy tắc mới.

## Xác thực demo

### `POST /auth/login` → 200

```json
{"email":"learner1@example.test","password":"learn1234"}
```

```json
{
  "accessToken": "random-access-token",
  "refreshToken": "random-refresh-token",
  "expiresIn": 300,
  "user": {"id":"user-1","email":"learner1@example.test"}
}
```

Tài khoản thứ hai là `learner2@example.test`, cùng mật khẩu `learn1234`, ID `user-2`. Sai thông tin trả 401 `invalid_credentials`. Hai tài khoản có cùng quyền trong không gian riêng, không có vai trò admin.

### `POST /auth/refresh` → 200

```json
{"refreshToken":"refresh-token-hien-tai"}
```

Response cùng cấu trúc login. Refresh xoay access và refresh token; cả refresh cũ và access đi kèm đều không còn dùng được. Refresh token không có TTL riêng trong mock nhưng mất khi server restart. Access token hết hạn mặc định sau 300 giây; có thể chạy server với `--token-ttl 5` cho lab. Không dùng cơ chế này để suy luận thiết kế auth production.

**Tình huống cần xử lý ở client:** nhiều request đồng thời nhận 401 chỉ nên kích hoạt một lần refresh đang chạy; request còn lại chờ kết quả. Refresh thất bại chuyển về đăng nhập và giữ/xóa dữ liệu cục bộ theo chính sách account isolation, không retry vô hạn.

## Đọc dữ liệu

### `GET /tasks?q=&status=&cursor=&limit=` → 200

```json
{"items":[{"id":"task-001","title":"Học Dart","description":"","status":"todo","dueAt":null,"updatedAt":"2026-11-16T10:00:00.000Z","version":1,"ownerId":"user-1"}],"nextCursor":null}
```

- `q`: tìm substring trong title. Mock dùng SQLite `lower`, không phân biệt hoa/thường ASCII; không cung cấp tìm kiếm tiếng Việt bỏ dấu hoặc full Unicode case folding.
- `status`: bỏ trống hoặc một trong ba status.
- `limit`: số nguyên 1–100, mặc định 20.
- `cursor`: chuỗi opaque server trả. Client không tự sửa hoặc dựa vào cấu trúc bên trong.
- Sắp xếp **ID tăng dần**, không theo ngày cập nhật. Cursor dùng keyset theo ID và gắn với bộ lọc. Đổi `q`/`status` phải xóa danh sách/cursor cũ hoặc thay thế chúng theo chiến lược UI đã định.
- `nextCursor: null` nghĩa là hết trang hiện tại. Nếu dữ liệu thay đổi giữa các lần tải, đây không phải một snapshot bất biến. Task mới có ID đứng trước cursor có thể chỉ xuất hiện khi refresh từ đầu.
- Trả về chỉ task thuộc user của token. Empty list là 200 với `items: []`, không phải 404.

### `GET /tasks/{id}` → 200

Trả về một object task. Task không tồn tại hoặc thuộc user khác đều trả 404 `not_found`, tránh lộ thông tin sở hữu.

## Ghi dữ liệu

### `POST /tasks` → 201

Header bắt buộc: `Idempotency-Key: <operation-id>` (1–128 ký tự ASCII).

```json
{"id":"task-001","title":"Học Dart","description":"","status":"todo","dueAt":null}
```

Response là task. Trong bài offline, ghi **cả task cục bộ lẫn outbox operation** trong một transaction; giữ nguyên ID, operation key và body cho mọi lần retry của thao tác đó.

Quy tắc replay:

1. Cùng owner, key và body JSON tương đương về thứ tự key → 201 với **response đã lưu của thao tác ban đầu**, không tạo thêm task.
2. Cùng owner/key nhưng body khác → 409 `idempotency_conflict`.
3. ID đã tồn tại, key mới → 409 `duplicate_id`.
4. Key được phân vùng theo user, nên user khác dùng cùng key không truy cập response của nhau.

Replay trả kết quả cũ của operation, không nhất thiết trạng thái mới nhất của task sau các cập nhật/xóa khác. Nếu cần dữ liệu hiện tại, GET lại. Bản ghi idempotency tồn tại cùng database, không tự hết hạn trong mock.

### `PUT /tasks/{id}` → 200

Body bắt buộc đủ `title`, `description`, `status`, `dueAt`, `version`:

```json
{"title":"Học Dart","description":"Xong phần async","status":"done","dueAt":null,"version":1}
```

Server so version **trong transaction**, cập nhật và tăng version thành 2. Nếu version cũ trả 409 `version_conflict`; dữ liệu hiện tại không bị thay đổi. `id`, `ownerId`, `updatedAt` do server kiểm soát.

PUT trong mock **không dùng Idempotency-Key**. Nếu server đã lưu nhưng client mất response, retry với version cũ có thể nhận 409. Hãy GET phiên bản mới và đối chiếu nội dung/ý định, rồi hòa giải hoặc hỏi người dùng theo thiết kế. Không đổi version tự động để ghi đè mọi xung đột.

### `DELETE /tasks/{id}` → 204

Header `If-Match: 2` chứa version nguyên dương hiện tại, **không dấu ngoặc kép**. Đây là quy ước version đơn giản của API học tập; không phải implementation tổng quát của HTTP ETag.

Version cũ trả 409. Không tìm thấy trả 404. Nếu retry thao tác xóa sau khi mất response, 404 có thể nghĩa mục tiêu đã bị xóa; cần xử lý theo ý định và dữ liệu local, không coi mọi 404 ở mọi endpoint là thành công.

## Mã lỗi cần phân biệt

| HTTP | `error.code` | Hành vi client nên thiết kế |
|---|---|---|
| 400 | `validation` | Sửa đầu vào hoặc request; không tự retry cùng dữ liệu vô hạn. |
| 401 | `invalid_credentials` | Báo thông tin đăng nhập không đúng. |
| 401 | `unauthorized` | Refresh có giới hạn; nếu không được, yêu cầu đăng nhập lại. |
| 401 | `invalid_refresh` | Kết thúc phiên hiện tại theo chính sách đã định. |
| 404 | `not_found` | Bản ghi không còn có thể truy cập; xử lý tình huống cụ thể. |
| 409 | `version_conflict` | Tải bản mới, giữ ý định người dùng và giải quyết xung đột. |
| 409 | `idempotency_conflict` | Lỗi quản lý operation key/body; kiểm tra outbox. |
| 409 | `duplicate_id` | Kiểm tra ID và trạng thái operation, không tùy tiện tạo ID mới mỗi retry. |
| 413 | `body_too_large` | Giảm body; mock không phải endpoint upload tệp. |
| 503 | `debug_failure` | Lỗi được cố ý tạo; thử lại có giới hạn sau khi bỏ debug header. |
| 500 | `storage_error` | Ghi nhận lỗi hệ thống; kiểm tra database cục bộ/server. |

Mất mạng, DNS, kết nối bị từ chối và timeout là lỗi transport; có thể không có HTTP response hoặc error JSON. UI/repository cần phân biệt chúng với lỗi nghiệp vụ HTTP.

## Kiểm tra tích hợp cần tự thực hiện

1. User 1 tạo task; user 2 GET/PUT/DELETE cùng ID phải 404, list không lộ task đó.
2. POST giống hệt hai lần cùng key chỉ tạo một row.
3. Hai PUT cùng version chạy đồng thời: chính xác một lần thành công, lần còn lại 409.
4. Đổi bộ lọc trong lúc trang cũ đang tải: response cũ không chen vào danh sách mới.
5. Token hết hạn khi nhiều request đang chờ: không tạo vòng refresh vô hạn.
6. Offline tạo task → đóng app → mở lại → có mạng: operation còn, task chỉ tạo một lần.
7. Response PUT bị mất: retry gây 409 được hòa giải, không âm thầm mất chỉnh sửa.
8. HTTP 204 được coi là thành công mà không JSON decode.

Header debug và cách chạy server: [mock_api/README.md](../mock_api/README.md). Header `X-Debug-Delay-Ms` chỉ cho 0–3000; `X-Debug-Fail` chỉ hỗ trợ giá trị `503`. Cả hai đều được áp dụng trước thao tác chính.
