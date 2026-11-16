# Tuần 13 — Kiến trúc theo trách nhiệm và chiều phụ thuộc

**Đích đến:** sửa một tính năng mà không phải lần theo API, SQL và widget trong cùng một file. **Tiên quyết:** WorkBoard có UI, provider, HTTP và local data source; chưa cần viết lại toàn bộ ứng dụng.

## 1. Bài giảng

### Chia theo lý do thay đổi

Widget thay đổi khi cách trình bày đổi. Logic tương tác thay đổi khi luồng sử dụng đổi. Data source thay đổi khi giao thức API hoặc database đổi. Đặt chúng cạnh nhau trong cùng class làm một thay đổi kéo theo nhiều rủi ro. Tách trách nhiệm dựa trên những lý do này, không theo mong muốn có thật nhiều thư mục.

Một feature có thể gồm `presentation/`, `application/`, `data/`; tên thư mục chỉ là gợi ý. Điều quan trọng là widget không biết endpoint, JSON key hoặc câu SQL. Controller biết hành động người dùng và state cần hiển thị. Repository cung cấp khả năng đọc/ghi task với chính sách phối hợp nguồn dữ liệu đã thống nhất.

### Repository là hợp đồng hành vi

Repository không chỉ đổi tên một HTTP client. Nó giúp phần dùng dữ liệu không bị buộc vào HTTP hay SQLite và là nơi thích hợp cho chính sách cache khi dự án cần. Interface phải nói rõ kết quả và lỗi. Ví dụ rút gọn, đặt trong thư viện nơi `WorkTask` đã được khai báo/import:

```dart
abstract interface class TaskRepository {
  Future<WorkTask> create(TaskDraft draft);
  Future<WorkTask> update(WorkTask task);
}

final class TaskDraft {
  const TaskDraft({required this.id, required this.title});
  final String id;
  final String title;
}
```

Interface này chỉ minh họa hai thao tác, chưa là toàn bộ contract của dự án. Tách draft tạo mới khỏi task server giúp tránh giả định client tự cấp `ownerId`, `updatedAt` hoặc version authoritative. Một thiết kế khác vẫn hợp lệ nếu trách nhiệm rõ và test bảo vệ được.

### Chiều phụ thuộc và đường đi của dữ liệu

Hành động lưu đi từ UI đến controller rồi repository, sau đó đến data source. Kết quả đi ngược về để cập nhật state và UI. Widget không được lách qua repository để gọi thẳng API khi gặp tình huống khó; đó thường là tín hiệu contract thiếu khả năng cần thiết.

Không để model nghiệp vụ phụ thuộc `BuildContext`, widget hoặc HTTP response. Đặc điểm này cho phép kiểm thử logic bằng Dart thuần. DTO là biểu diễn giao thức; domain model là biểu diễn ý nghĩa ứng dụng. Chỉ tách hai loại khi có khác biệt hoặc lợi ích rõ ràng; sao chép hai class giống hệt nhau cũng có chi phí bảo trì.

### Kiến trúc được kiểm chứng bằng thay đổi

Tên “Clean Architecture” không chứng minh code dễ thay đổi. Hãy thử đổi nguồn dữ liệu hoặc thêm một yêu cầu nhỏ, đếm phần nào bị ảnh hưởng và xem test nào bảo vệ nó. Domain layer là tùy chọn khi có quy tắc nghiệp vụ phức tạp hoặc tái sử dụng thực sự; một hàm chuyển tiếp không tạo thêm ý nghĩa chỉ để đủ tầng có thể làm đọc code khó hơn.

## 2. Ba bài thực hành

### W13-L1 — Vẽ hiện trạng và tìm ranh giới

Vẽ đường đi của thao tác “sửa tiêu đề” trong code hiện tại. Ghi rõ file chứa validation, HTTP, JSON mapping và UI. Chọn đúng một feature để refactor, ưu tiên danh sách hoặc sửa công việc. Đầu ra là sơ đồ trước/sau và danh sách file dự kiến thay đổi, chưa bắt đầu di chuyển hàng loạt.

### W13-L2 — Chuyển một feature có bảo vệ

Viết test hành vi cho feature đã chọn rồi tạo repository interface và implementation. Chuyển widget sang gọi controller; controller nhận repository từ bên ngoài. Đầu vào fixture vẫn là các task tuần trước. Đầu ra UI và các trường hợp lỗi giữ đúng hành vi đã ghi, kể cả retry và response cũ.

### W13-L3 — Đổi nguồn mà giữ UI

Tạo in-memory implementation và remote implementation cùng contract. Chạy màn hình bằng mỗi implementation thông qua cấu hình dependency. Không thêm `if (useFake)` vào widget. Dùng một fake trả lỗi để chứng minh UI vẫn hiển thị đúng trạng thái lỗi mà không biết nguồn nào đang chạy.

## 3. Nghiệm thu và tự kiểm tra

- [ ] Widget của feature không chứa endpoint, SQL hoặc JSON parsing.
- [ ] Controller không nhận `BuildContext` để thực hiện nghiệp vụ.
- [ ] Repository có hợp đồng rõ cho dữ liệu và lỗi.
- [ ] Fake và remote thay được ở điểm cấu hình dependency.
- [ ] Test trước refactor vẫn qua mà không đổi kỳ vọng tùy tiện.
- [ ] PR chỉ refactor phạm vi đã chọn, có sơ đồ và lý do.
- [ ] Mỗi abstraction mới có ít nhất một trách nhiệm có thể giải thích.

**Ba câu hỏi:** Repository khác HTTP client thế nào? Khi nào nên tách DTO và domain model? Dấu hiệu nào cho thấy một layer đang chỉ làm code dài thêm?

**15 giờ:** 3 giờ đọc và vẽ; 8 giờ ba lab; 3 giờ regression test; 1 giờ walkthrough PR. **Nộp:** PR nhỏ, sơ đồ, test và ghi chú điểm chưa refactor.

Đọc [Flutter architecture guide](https://docs.flutter.dev/app-architecture/guide), [architecture recommendations](https://docs.flutter.dev/app-architecture/recommendations), [gợi ý](../solutions/week-13.md).
