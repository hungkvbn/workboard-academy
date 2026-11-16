# Tuần 02 — Collections, model bất biến và generics

**Mục tiêu:** chuyển các hàm rời thành mô hình công việc dễ hiểu và có thể kiểm thử. **Tiên quyết:** hoàn thành tuần 01, biết tiêu đề hợp lệ và cách so sánh thời điểm. Tiếp tục dùng [starter Dart](../starter/dart/README.md).

**Ngân sách 15 giờ:** 3 giờ lý thuyết; 8 giờ cho ba lab; 3 giờ kiểm thử và refactor; 1 giờ demo. Đầu ra là một thư viện Dart quản lý công việc trong bộ nhớ. Chưa cần database hoặc backend; lưu bằng chứng tại `evidence/week-02/`.

## Bài giảng

### 1. Chọn collection theo câu hỏi cần trả lời

`List` giữ thứ tự và cho phép phần tử trùng. `Set` biểu diễn các giá trị duy nhất. `Map` ánh xạ khóa đến giá trị; phù hợp để tìm công việc theo ID. Một danh sách vẫn hữu ích để hiển thị kết quả có thứ tự, nhưng không phải mọi thao tác đều cần duyệt toàn bộ danh sách.

```dart
final tasksById = <String, String>{'t-1': 'Học Dart'};
tasksById['t-2'] = 'Viết test';
final title = tasksById['missing']; // String?
```

Kết quả truy cập Map có thể null vì khóa không tồn tại. Đừng dùng `!` trừ khi bất biến của chương trình thực sự bảo đảm khóa có mặt. Hãy xác định rõ khi tìm không thấy thì trả null hay báo lỗi nghiệp vụ.

### 2. Model diễn tả quy tắc của sản phẩm

WorkBoard sử dụng `WorkTask` với các trường: `id`, `title`, `description`, `status`, `dueAt`, `updatedAt`, `version`, `ownerId`. `status` có ba giá trị `todo`, `doing`, `done`. Dùng enum giới hạn tập giá trị hợp lệ; chuỗi tùy ý như `'finished'` không nên len vào phần logic.

```dart
enum TaskStatus { todo, doing, done }

class TaskSummary {
  const TaskSummary({required this.id, required this.title});
  final String id;
  final String title;

  TaskSummary rename(String value) =>
      TaskSummary(id: id, title: value.trim());
}
```

Đây là ví dụ nhỏ về bất biến, chưa phải model đầy đủ. `rename` trả đối tượng mới; người giữ đối tượng cũ vẫn thấy giá trị cũ. Khi cập nhật UI hoặc ghi lại lịch sử, cách này giúp biết điều gì đã thay đổi. Validation phải được áp dụng ở ranh giới tạo hoặc sửa dữ liệu.

### 3. Lọc, sắp xếp và tác dụng phụ

`where` trả một iterable; `toList` tạo danh sách kết quả. `sort` thay đổi chính danh sách được gọi. Nếu muốn giữ nguyên nguồn, hãy sao chép trước khi sort.

```dart
final source = [3, 1, 2];
final sorted = [...source]..sort();
// source vẫn là [3, 1, 2]; sorted là [1, 2, 3].
```

Quy tắc thứ tự cần đủ rõ: tuần này, hạn sớm đứng trước, công việc không có hạn đứng cuối, bằng hạn thì so ID để kết quả ổn định. Việc dựa vào thứ tự ngẫu nhiên của nguồn sẽ làm kiểm thử và giao diện khó đoán.

### 4. Generics giữ thông tin kiểu khi tái sử dụng

`List<WorkTask>` cho phép analyzer biết mỗi phần tử là công việc. Một hàm `T? firstOrNull<T>(Iterable<T> values)` có thể dùng cho nhiều kiểu mà không trả `dynamic`. Chỉ trừu tượng hóa phần thực sự giống nhau; chưa cần dựng hệ thống base repository nhiều tầng.

## Thực hành

### W02-L1 — Model và thao tác đổi trạng thái

Tạo `WorkTask` với đầy đủ trường; bắt đầu bằng dữ liệu mẫu cố định. Viết phương thức tạo bản sao khi đổi tiêu đề hoặc trạng thái. Đầu vào là task `t-1`, tiêu đề `Học Dart`, trạng thái todo; sau thao tác đổi sang doing, bản mới phải mang doing và bản cũ vẫn todo. Quy định rõ cách xóa hạn: một tham số null mặc định không thể đồng thời có nghĩa “giữ nguyên” và “xóa”.

### W02-L2 — Bộ lọc và thứ tự

Chuẩn bị sáu công việc gồm hạn trùng, không hạn, ba trạng thái và tiêu đề khác nhau. Tạo hàm lọc theo trạng thái và từ khóa không phân biệt hoa/thường. Sắp xếp theo quy tắc trên. Đầu ra phải giữ nguyên dữ liệu nguồn và cho cùng thứ tự qua nhiều lần chạy.

### W02-L3 — Kho dữ liệu trong bộ nhớ

Tạo `TaskStore` với thêm, lấy theo ID, sửa và xóa. Thêm trùng ID phải bị từ chối; sửa ID không tồn tại phải báo lỗi rõ ràng. Trả danh sách sao chép hoặc không cho sửa từ bên ngoài. Nối kho dữ liệu vào CLI tuần 01 và viết test cho từng quy tắc.

## Nghiệm thu

- [ ] Model không dùng chuỗi tùy ý cho trạng thái nội bộ.
- [ ] Sửa một task không làm đối tượng cũ thay đổi ngầm.
- [ ] Có cách phân biệt giữ hạn và xóa hạn.
- [ ] Sort không thay đổi danh sách nguồn.
- [ ] Hạn null đứng cuối; trường hợp bằng hạn có thứ tự xác định.
- [ ] Thêm trùng ID và sửa ID thiếu được xử lý.
- [ ] Người gọi không thể sửa kho dữ liệu bằng list được trả về.

## Tự kiểm tra

1. Khi nào dùng Map thay cho List để lưu công việc?
2. Vì sao `copyWith({DateTime? dueAt})` với `dueAt ?? this.dueAt` không xóa được hạn?
3. Generics giúp gì so với trả về `dynamic`?

Đọc [Collections](https://dart.dev/language/collections), [Classes](https://dart.dev/language/classes), [Generics](https://dart.dev/language/generics). Sau khi làm, xem [gợi ý](../solutions/week-02.md).
