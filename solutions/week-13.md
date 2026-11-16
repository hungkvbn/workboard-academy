# Gợi ý tuần 13

## Đáp án tự kiểm tra

1. HTTP client xử lý request/response ở mức giao thức. Repository cung cấp khả năng dữ liệu có ý nghĩa cho ứng dụng, có thể phối hợp remote/local và che chi tiết transport. Một app nhỏ có thể có implementation mỏng; đừng thêm chính sách chưa cần.
2. Khi API model có cấu trúc, trường, nullability hoặc vòng đời khác với domain; hoặc khi muốn cô lập thay đổi transport. Nếu giống hệt và không có nhu cầu độc lập, cân nhắc chi phí mapping trước khi tách.
3. Layer chỉ chuyển nguyên tham số và kết quả, không giữ chính sách hay ranh giới cần thiết, trong khi buộc tạo nhiều file cho mỗi thay đổi. Không xóa chỉ vì ít code; đánh giá trách nhiệm và khả năng cô lập dependency.

## Gợi ý lab

- **W13-L1:** lần theo một request thật từ nút đến response. Sơ đồ phải khớp code, không chỉ vẽ kiến trúc mong muốn.
- **W13-L2:** giữ test hành vi bên ngoài controller ổn định. Nếu refactor làm mất xử lý response cũ, đó là regression thật cần sửa, không xóa test để phù hợp cấu trúc mới.
- **W13-L3:** fake phải có cùng quy tắc quan trọng như remote: ID ổn định, lỗi có ý nghĩa và update trả kết quả server. Ghi rõ những gì fake chưa mô phỏng.

## Ví dụ sửa lỗi

```dart
// Sai: controller tự quyết định nguồn dữ liệu và không thay được khi test.
// final repository = RemoteTaskRepository(HttpClient());

// Đúng: nhận dependency; ghép implementation tại điểm cấu hình.
final class RenameTask {
  RenameTask(this.repository);
  final TaskRepository repository;

  Future<WorkTask> call(WorkTask task, String title) {
    final trimmed = title.trim();
    if (trimmed.isEmpty) throw ArgumentError('Tiêu đề không được rỗng');
    return repository.update(task.copyWith(title: trimmed));
  }
}
```

Đoạn minh họa giả định model của bạn có `copyWith`. `RenameTask` không bắt buộc tồn tại như class riêng; hàm trong controller có thể đủ ở giai đoạn này. Điểm cần học là nhận dependency và giữ quy tắc ở vị trí có thể kiểm thử, không phải tạo use case cho mọi nút.
