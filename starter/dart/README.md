# Dart starter — tuần 01 đến 03

Đây là bộ khởi đầu để bạn **đọc một ví dụ đúng, rồi tự làm bài tập**. Nó chưa phải CLI hoàn chỉnh. Model `WorkTask` và demo đã có; năm hàm trong `lib/src/exercises.dart` cố ý ném `UnimplementedError`.

## Chạy lần đầu

Cần Dart SDK 3.4 trở lên, dưới 4. Flutter SDK có kèm Dart; mở terminal mới sau khi thiết lập PATH. Từ thư mục này:

```bash
dart --version
dart pub get
dart run bin/main.dart
dart analyze
dart test test/work_task_test.dart
```

Demo in hai phiên bản của cùng công việc: bản gốc `todo`, bản sao `done`, rồi JSON. ID và mốc thời gian trong demo được cố định để dễ so sánh. Các giá trị `learner-1` trong demo model không phải credential của API.

## Phần nào đã làm, phần nào bạn cần làm?

| Phần | Trạng thái |
|---|---|
| Model bất biến, enum, trim title, UTC, JSON, copyWith | Ví dụ đã triển khai |
| 8 test cho model | Test nền tảng cần chạy xanh |
| normalizeTitle, titleError, isOverdue, filterTasks, sortTasks | Bài tập chưa triển khai |
| 4 test bài tập | Cố ý bị skip cho tới khi bạn bắt đầu bài tập |
| Menu CLI, lưu file, repository async, xử lý lỗi file | Bạn xây trong tuần 01–03 |

Chạy `dart test` có thể báo thành công dù 4 bài tập bị skip. **Điều đó không chứng minh bạn hoàn thành bài tập.** Mở `test/exercises_test.dart`, xóa tham số `skip: '...'` ở cuối `group`, rồi chạy:

```bash
dart test test/exercises_test.dart
```

Lần đầu test sẽ thất bại vì `UnimplementedError`. Viết phần thân các hàm để test xanh, sau đó bổ sung trường hợp mà bộ test còn thiếu. Không sửa assertion để khớp với kết quả sai.

## Hợp đồng bài tập

- `normalizeTitle`: chỉ trim đầu/cuối, không ném lỗi validation. `titleError`: trả null khi độ dài sau trim từ 1 đến 120, ngược lại trả thông báo. `String.length` đếm UTF-16 code units, không phải số ký tự người dùng nhìn thấy. Trong giáo trình dùng quy ước này nhất quán; hỗ trợ grapheme là bài mở rộng có chủ đích.
- `filterTasks`: tìm trong tiêu đề, không phân biệt hoa thường, trim query; query và status kết hợp bằng AND. Không có status nghĩa là mọi trạng thái; query rỗng khớp mọi tiêu đề. Giữ thứ tự đầu vào.
- `sortTasks`: hạn gần nhất trước, chưa có hạn ở cuối; cùng hạn (kể cả cùng null) thì `id` tăng dần. Không sửa list đầu vào.

Ví dụ: `[b(hạn 01/02), z(không hạn), a(hạn 01/02)]` phải thành `[a, b, z]`; nguồn ban đầu vẫn có thứ tự `[b, z, a]`.

## Gợi ý mở rộng theo tuần

1. Tuần 01: validation, menu nhập liệu và báo lỗi rõ ràng.
2. Tuần 02: thêm/sửa/xóa trong store, lọc và sắp xếp, giữ model bất biến.
3. Tuần 03: đọc/ghi file JSON bằng API bất đồng bộ; phân biệt file không tồn tại với JSON hỏng; test với thư mục tạm. Tự định nghĩa interface repository, chưa cần framework DI.

`WorkTask.fromJson` là ví dụ đọc schema đúng kiểu; kiểu sai có thể gây lỗi cast hoặc parse. Hãy thêm bài tập chuyển lỗi kỹ thuật thành thông báo phù hợp tại ranh giới nhập dữ liệu. Không nuốt lỗi và trả danh sách rỗng trong mọi trường hợp.

Model chưa override `==`: hai instance khác nhau chưa có value equality. Hãy đọc yêu cầu tuần 02 trước khi bổ sung, và test cùng lúc cả `==` lẫn `hashCode` nếu quyết định làm.

Tài liệu: [Dart language](https://dart.dev/language), [package:test](https://pub.dev/packages/test).

## W01-L2 — Kiểm tra quá hạn

Khung `isOverdue` nằm trong `lib/src/exercises.dart`. Triển khai theo bài giảng,
không gọi đồng hồ thật bên trong hàm. Mở `test/overdue_test.dart`, bỏ tham số
`skip` của group rồi chạy riêng sáu test của lab:

```bash
dart test test/overdue_test.dart
```

Test phải thất bại với `UnimplementedError` trước khi bạn viết phần thân hàm.
Sau khi hoàn thành, cả sáu trường hợp phải vượt qua. Các test lọc/sắp xếp W02
trong `exercises_test.dart` có thể tiếp tục skip cho tới tuần 02.
