# WorkBoard Mock API — phòng thí nghiệm mạng cục bộ

Backend này giúp bạn học Flutter mà chưa phải tự xây backend. Nó chạy bằng **Python 3.10 trở lên, chỉ dùng thư viện chuẩn**, lưu công việc trong SQLite và có hai người dùng giả để kiểm tra phân quyền. Bộ test đã kiểm tra server HTTP thật, không chỉ gọi hàm bên trong.

**Chỉ dùng trên máy học hoặc mạng thử nghiệm bạn kiểm soát.** Mật khẩu demo cố định, không có TLS, cơ chế token giản lược và có header cố ý gây lỗi. Đây không phải backend production và không được đưa lên Internet để phục vụ người dùng thật. Từ tuần phát hành, hãy dùng backend được cấu hình phù hợp hoặc chỉ phân phối bản demo trong phạm vi thử nghiệm với dữ liệu giả.

## 1. Khởi động

Mở terminal tại thư mục gốc của bộ học:

```bash
python3 mock_api/server.py
```

Trên Windows có thể dùng `py -3` thay `python3`. Giữ terminal mở. Trong terminal thứ hai:

```bash
curl http://127.0.0.1:8765/health
```

Kết quả:

```json
{"mode":"local-learning-only","status":"ok"}
```

Mặc định database mới **không có task**. Bạn tự tạo task qua lab/API. Dữ liệu được lưu tại `mock_api/workboard.sqlite3`; dừng rồi chạy lại vẫn còn task. Token chỉ ở bộ nhớ, nên chạy lại server phải đăng nhập lại. File database và token không cần commit vào Git.

Đổi cổng hoặc nơi lưu dữ liệu:

```bash
python3 mock_api/server.py --port 8766 --db ./work/local-lab.sqlite3
```

Không chạy hai server cùng cổng. `Ctrl+C` dừng server.

## 2. Đăng nhập bằng tài khoản giả

| Email | Mật khẩu | ID server cấp |
|---|---|---|
| `learner1@example.test` | `learn1234` | `user-1` |
| `learner2@example.test` | `learn1234` | `user-2` |

```bash
curl -X POST http://127.0.0.1:8765/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"learner1@example.test","password":"learn1234"}'
```

Response có `accessToken`, `refreshToken`, `expiresIn` và `user`. Sao chép **accessToken** vào biến dành riêng cho buổi thực hành:

```bash
WB_TOKEN='DAN_ACCESS_TOKEN_VUA_NHAN_VAO_DAY'
```

Các ví dụ shell dùng Bash/zsh. Trong PowerShell dùng cú pháp biến và `curl.exe` tương ứng, hoặc thực hiện bằng HTTP client bạn quen. Token mặc định hết hạn sau 300 giây. Khi nhận 401, refresh theo hợp đồng API hoặc đăng nhập lại để tiếp tục lab.

## 3. Tạo, đọc, sửa và xóa

Tạo task với ID và khóa thao tác do client sinh. Khi retry **cùng một thao tác tạo**, giữ nguyên ID, khóa và body:

```bash
curl -X POST http://127.0.0.1:8765/tasks \
  -H "Authorization: Bearer $WB_TOKEN" \
  -H 'Content-Type: application/json' \
  -H 'Idempotency-Key: create-task-001-v1' \
  -d '{"id":"task-001","title":"Học Dart","description":"Hoàn thành lab tuần 1","status":"todo","dueAt":null}'
```

Response HTTP 201 chứa task `version: 1`, `ownerId: "user-1"`. Gửi lại đúng request vẫn nhận HTTP 201 và response ban đầu, không sinh bản ghi mới.

```bash
curl 'http://127.0.0.1:8765/tasks?limit=20&status=todo' \
  -H "Authorization: Bearer $WB_TOKEN"
```

Danh sách có dạng `{ "items": [...], "nextCursor": null }`. Khi có `nextCursor`, truyền cursor đó vào lần tải tiếp theo và giữ nguyên bộ lọc.

```bash
curl -X PUT http://127.0.0.1:8765/tasks/task-001 \
  -H "Authorization: Bearer $WB_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"title":"Học Dart","description":"Đã làm xong lab tuần 1","status":"done","dueAt":null,"version":1}'
```

Response mới có `version: 2`. Nếu gửi lại PUT với `version: 1`, server trả **409**, không ghi đè dữ liệu hiện tại. Đọc `GET /tasks/task-001`, rồi xử lý xung đột trong UI.

```bash
curl -X DELETE http://127.0.0.1:8765/tasks/task-001 \
  -H "Authorization: Bearer $WB_TOKEN" \
  -H 'If-Match: 2'
```

Xóa thành công trả HTTP 204, body rỗng. Client không được cố parse JSON cho response này.

## 4. Các bài cố ý gây lỗi

**Mạng chậm:** thêm `X-Debug-Delay-Ms: 1500`. Giới hạn hợp lệ là 0–3000 ms. Dùng hai request tìm kiếm với độ trễ khác nhau để tái hiện response cũ về sau response mới. Không cần làm chậm cả thiết bị.

```bash
curl 'http://127.0.0.1:8765/tasks?q=Dart' \
  -H "Authorization: Bearer $WB_TOKEN" \
  -H 'X-Debug-Delay-Ms: 1500'
```

**Lỗi tạm thời:** thêm `X-Debug-Fail: 503`. Header sẽ tiếp tục làm lỗi mọi request có nó; bỏ header để phục hồi. Lỗi này xảy ra **trước mutation**, không mô phỏng tình huống server đã ghi nhưng response bị mất. Với tình huống mất response, client có thể bỏ response đầu tiên trong test rồi gửi lại cùng request/khóa.

```bash
curl http://127.0.0.1:8765/tasks \
  -H "Authorization: Bearer $WB_TOKEN" \
  -H 'X-Debug-Fail: 503'
```

**Hết token:** dừng server rồi chạy `python3 mock_api/server.py --token-ttl 5`. Đăng nhập, chờ hơn 5 giây và tải task; phải nhận 401. Dùng `refreshToken` gọi `POST /auth/refresh`. Refresh thành công xoay cả hai token; refresh token cũ không dùng lại được. Client cần tránh để nhiều request tự refresh đồng thời.

**Xung đột:** hai màn hình đọc cùng task version 1. Màn hình A lưu thành version 2, màn hình B lưu với version 1 phải nhận 409. Đừng âm thầm đổi version của B rồi retry; người dùng cần biết lựa chọn hòa giải dữ liệu.

**Phân quyền:** đăng nhập user 2, thử đọc/sửa/xóa ID của user 1. Server phải trả 404 như task không tồn tại. Lọc UI không thay thế được kiểm tra phía server.

## 5. Kết nối từ Flutter

| Nơi chạy ứng dụng | Base URL khi server ở máy phát triển |
|---|---|
| Desktop hoặc Flutter web trên máy đó | `http://127.0.0.1:8765` |
| Android Emulator chuẩn | `http://10.0.2.2:8765` |
| iOS Simulator trên cùng Mac | `http://127.0.0.1:8765` |
| Điện thoại thật | IP LAN của máy phát triển; cần bind và quyền mạng phù hợp |

Ví dụ truyền cấu hình ở thời điểm chạy nếu ứng dụng đọc `API_BASE_URL`:

```bash
flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8765
```

Android Emulator: `localhost` bên trong app là emulator, không phải máy host. Nếu Android chặn HTTP, chỉ thêm cấu hình phục vụ debug vào `android/app/src/debug/AndroidManifest.xml` (ghép vào manifest debug hiện có):

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET" />
    <application android:usesCleartextTraffic="true" />
</manifest>
```

Không chuyển cấu hình cho phép HTTP này sang release để giải quyết vấn đề production. Trên iOS, nếu gặp chính sách ATS/local network, cấu hình ngoại lệ **chỉ cho môi trường debug/local** theo tài liệu nền tảng; backend release cần HTTPS phù hợp.

Với điện thoại thật, có thể chạy `--host 0.0.0.0` trên mạng thử nghiệm tin cậy và dùng IP LAN của máy. Điều đó làm server có thể truy cập từ máy khác trong mạng; dừng khi kết thúc lab, không mở cổng ra Internet. Flutter web được CORS cho origin `localhost`, `127.0.0.1`, `::1`; origin domain/IP khác không được cho phép. CORS là chính sách trình duyệt, không phải cơ chế phân quyền dữ liệu.

## 6. Chạy kiểm thử và reset

Tại thư mục gốc của bộ học:

```bash
python3 -m unittest discover -s mock_api -v
```

Test tạo database tạm và server ở cổng trống, không sửa database đang học. Bộ test bao phủ tạo task, retry đồng thời, version conflict, quyền theo user, phân trang, refresh, UTF-16 title length, dữ liệu lỗi, độ trễ, CORS và body limit.

Để bắt đầu một bộ dữ liệu mới, cách dễ nhất là dừng server và chọn file khác:

```bash
python3 mock_api/server.py --db ./work/lab-clean.sqlite3
```

Muốn xóa hẳn dữ liệu cũ, dừng server trước rồi tự xóa đúng file `workboard.sqlite3` cùng file `-wal`/`-shm` liên quan nếu còn. Không xóa thư mục dự án.

Đọc [hợp đồng API](../project/api-contract.md) trước khi viết HTTP repository. Các lỗi cấu hình và giới hạn của mock cần được phân biệt với lỗi Flutter của bạn.
