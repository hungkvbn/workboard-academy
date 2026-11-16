# Tuần 01 — Dart: kiểu dữ liệu, null safety và hàm

**Mục tiêu:** viết được các hàm nền tảng của WorkBoard và giải thích cách Dart phát hiện lỗi trước khi chạy. **Tiên quyết:** đã viết biến, điều kiện, vòng lặp và hàm bằng một ngôn ngữ khác. Dùng [starter Dart](../starter/dart/README.md); chưa cần giao diện Flutter.

**Ngân sách 15 giờ:** 3 giờ đọc và chạy ví dụ; 8 giờ làm ba lab; 3 giờ kiểm thử và sửa lỗi; 1 giờ demo. Nếu có thêm thời gian, tự viết lại bài từ file trống. Đầu tuần chạy `dart --version`, tạo nhánh `week-01`, cuối tuần lưu bằng chứng trong `evidence/week-01/` của bản sao dự án.

## Bài giảng

### 1. Kiểu tĩnh giúp mô tả điều chương trình được phép làm

`var` yêu cầu Dart suy luận kiểu; nó không biến một biến thành kiểu tùy ý. Sau `var title = 'Đọc Dart';`, gán số vào `title` sẽ bị analyzer báo lỗi. `dynamic` trì hoãn nhiều kiểm tra đến lúc chạy, vì vậy không nên dùng để né lỗi kiểu. `Object?` diễn tả giá trị chưa biết nhưng yêu cầu kiểm tra trước khi sử dụng.

```dart
String normalizeTitle(String raw) => raw.trim();

String? titleError(String raw) {
  final title = normalizeTitle(raw);
  if (title.isEmpty) return 'Tiêu đề không được để trống';
  if (title.length > 120) return 'Tiêu đề tối đa 120 ký tự';
  return null;
}
```

Hàm trên trả `null` khi hợp lệ, trả thông báo khi không hợp lệ. Trong bộ bài tập, giới hạn độ dài được tính bằng `String.length`; chuỗi có emoji có thể không tương ứng một-một với số ký tự người dùng nhìn thấy. Ghi rõ quy ước này thay vì vô tình thay đổi nó giữa các màn hình.

### 2. Null là một khả năng cần xử lý

`DateTime` bắt buộc chứa ngày; `DateTime?` có thể không có ngày. Không đặt hạn hoàn thành khác với đặt hạn hôm nay. Toán tử `?.` chỉ thực hiện thao tác khi có giá trị, còn `??` cung cấp giá trị thay thế. Dấu `!` khẳng định một điều với trình biên dịch; nếu khẳng định sai, ứng dụng vẫn lỗi khi chạy.

```dart
String deadlineLabel(DateTime? dueAt) {
  if (dueAt == null) return 'Chưa đặt hạn';
  return dueAt.toUtc().toIso8601String();
}
```

Sau nhánh kiểm tra, Dart biết `dueAt` không còn null tại dòng sử dụng. Đây là type promotion. Hãy ưu tiên diễn tả điều kiện thật thay vì thêm `!` để làm lỗi biến mất.

### 3. `final`, `const` và tính bất biến

`final` chỉ cho gán biến một lần; `const` yêu cầu giá trị hằng có thể xác định lúc biên dịch. `final titles = <String>[]` vẫn cho phép thêm phần tử: biến không đổi tham chiếu, nhưng đối tượng được tham chiếu vẫn thay đổi. Tuần sau bạn sẽ thiết kế model để tránh thay đổi ngầm.

### 4. Hàm nhỏ tạo ranh giới kiểm thử

Hàm chuẩn hóa tiêu đề chỉ cần chuỗi, không cần đọc bàn phím hay mở file. Tách logic thuần khỏi nhập/xuất giúp thử hàng chục trường hợp nhanh chóng. Named parameters làm lời gọi dễ đọc, chẳng hạn `isOverdue(dueAt: deadline, now: fixedTime)`. Truyền `now` từ ngoài giúp test không phụ thuộc giờ máy tính.

## Thực hành

### W01-L1 — Bộ xử lý tiêu đề

Viết `normalizeTitle` và `titleError` trong thư mục `lib/`. Đầu vào gồm `"  Học Dart  "`, `"   "`, chuỗi 120 và 121 chữ `a`. Đầu ra tương ứng là tiêu đề đã trim, lỗi rỗng, hợp lệ và lỗi quá dài. Viết chương trình nhỏ in kết quả; không trộn `print` vào hàm validation.

### W01-L2 — Hạn hoàn thành

Viết `isOverdue({DateTime? dueAt, required DateTime now, required bool isDone})`. Quy tắc: không có hạn hoặc đã hoàn thành thì không quá hạn; hạn phải nhỏ hơn `now` mới quá hạn. Dùng mốc cố định `2026-01-10T12:00:00Z`; thử trước, đúng và sau mốc đó. Chuyển các giá trị về cách so sánh thời điểm nhất quán.

### W01-L3 — Chương trình CLI đầu tiên

Nhận tiêu đề và hạn tùy chọn từ người dùng; gọi các hàm đã viết; in bản tóm tắt hoặc lỗi dễ hiểu. Người dùng nhập ngày sai phải có cơ hội sửa. Thêm README gồm lệnh chạy và ba ví dụ đầu vào/đầu ra. Có thể dùng dữ liệu truyền trực tiếp trong `main` trước khi thêm đọc bàn phím.

## Nghiệm thu

- [ ] Analyzer không báo lỗi; không dùng `dynamic` hoặc `!` để bỏ qua lỗi đang gặp.
- [ ] Tiêu đề chỉ chứa khoảng trắng bị từ chối.
- [ ] Ranh giới 120/121 được kiểm tra sau khi trim.
- [ ] Hạn bằng đúng `now` không bị coi là quá hạn.
- [ ] Công việc đã hoàn thành không hiện quá hạn.
- [ ] Logic kiểm tra chạy được mà không đọc stdin hoặc đồng hồ thật.
- [ ] Có README và kết quả chạy các trường hợp lỗi.

## Tự kiểm tra

1. Vì sao `var name = 'Lan'; name = 3;` không hợp lệ?
2. `final list = <String>[]` có đảm bảo nội dung list bất biến không?
3. Vì sao truyền `now` vào hàm tốt hơn gọi `DateTime.now()` bên trong khi kiểm thử?

Đọc [Variables](https://dart.dev/language/variables), [Null safety](https://dart.dev/null-safety/understanding-null-safety), [Functions](https://dart.dev/language/functions). Làm trước rồi mới mở [gợi ý và đáp án](../solutions/week-01.md).
