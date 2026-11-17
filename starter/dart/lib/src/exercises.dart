import 'work_task.dart';

/// W01: chỉ trim hai đầu; validation do titleError phụ trách.
String normalizeTitle(String input) {
  // TODO(W01): tự viết từ đặc tả và test; không gọi hàm private của model.
  throw UnimplementedError('Bài tập W01: normalizeTitle');
}

/// W01: null nếu tiêu đề sau trim dài 1..120 UTF-16 code units,
/// ngược lại trả thông báo lỗi dễ hiểu. Khớp bài giảng tuần 01.
String? titleError(String input) {
  // TODO(W01): gọi normalizeTitle rồi kiểm tra rỗng và độ dài.
  throw UnimplementedError('Bài tập W01: titleError');
}

/// W01-L2: công việc quá hạn khi có hạn nhỏ hơn now và chưa hoàn thành.
/// Hạn bằng now không quá hạn. So sánh thời điểm, không so chuỗi ngày.
bool isOverdue({
  DateTime? dueAt,
  required DateTime now,
  required bool isDone,
}) {
  // TODO(W01-L2): xử lý null, trạng thái hoàn thành và ranh giới thời gian.
  throw UnimplementedError('Bài tập W01-L2: isOverdue');
}

/// W02: lọc theo status nếu được cung cấp; query trim, không phân biệt hoa
/// thường và tìm trong title. Query rỗng khớp mọi tiêu đề.
/// Giữ thứ tự đầu vào và trả về list mới.
List<WorkTask> filterTasks(
  Iterable<WorkTask> tasks, {
  TaskStatus? status,
  String query = '',
}) {
  // TODO(W02): kết hợp hai điều kiện bằng AND; không sửa list đầu vào.
  throw UnimplementedError('Bài tập W02: filterTasks');
}

/// W02: hạn gần nhất trước; dueAt null ở cuối; cùng hạn thì id tăng dần.
/// Trả về list mới và không sửa đầu vào.
List<WorkTask> sortTasks(Iterable<WorkTask> tasks) {
  // TODO(W02): viết comparator đầy đủ, kể cả trường hợp cả hai hạn null.
  throw UnimplementedError('Bài tập W02: sortTasks');
}
